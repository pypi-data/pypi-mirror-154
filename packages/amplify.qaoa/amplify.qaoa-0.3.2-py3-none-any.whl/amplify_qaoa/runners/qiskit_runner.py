from __future__ import annotations

import time
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from qiskit import IBMQ, transpile
from qiskit.circuit import Parameter
from qiskit.opflow import CircuitStateFn, EvolutionFactory, H, I, StateFn, X, Z
from qiskit.opflow.converters import CircuitSampler
from qiskit.opflow.expectations import PauliExpectation
from qiskit.providers.aer import AerSimulator
from qiskit.providers.ibmq import least_busy
from qiskit.utils.backend_utils import is_aer_provider
from scipy.optimize import minimize

from .core import AbstractQAOARunner, decode_solutions


def PauliZ(n_qubit, i):
    return (I ^ i) ^ Z ^ (I ^ (n_qubit - i - 1))


def PauliX(n_qubit, i):
    return (I ^ i) ^ X ^ (I ^ (n_qubit - i - 1))


Device_Type = ["CPU", "GPU", "QPU"]


class QiskitRunner(AbstractQAOARunner):

    __token: Optional[str] = None
    __provider: Any = None
    __device: str = "CPU"
    __backend_name: Optional[str] = None
    __backend: Any = None

    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self, value):
        if not self.__token == value:
            self.__provider = IBMQ.enable_account(value) if value is not None else None

            # Reset backend
            self.__backend = None

        self.__token = value

    @property
    def provider(self):
        return self.__provider

    @property
    def device(self):
        return self.__device

    @device.setter
    def device(self, value):
        if value not in Device_Type:
            raise RuntimeError("Specified device type is not supported.")

        if not self.__device == value:
            # Reset backend
            self.__backend = None

        self.__device = value

    @AbstractQAOARunner.shots.setter
    def shots(self, value):
        if self.__backend is not None and not self._shots == value:
            self.__backend.set_options(shots=value)

        self._shots = value

    @property
    def backend_name(self):
        return self.__backend_name

    @backend_name.setter
    def backend_name(self, value):
        if not self.__backend_name == value:
            # Reset backend
            self.__backend = None

        self.__backend_name = value

    @property
    def backend(self):
        return self.__backend

    def __init__(
        self,
        reps: int = 10,
        shots: Optional[int] = 1024,
        backend_name: Optional[str] = None,
        device: str = "CPU",
        token: Optional[str] = None,
    ) -> None:
        super().__init__(reps, shots)

        if device not in Device_Type:
            raise RuntimeError("Specified device type is not supported.")

        self.backend_name = backend_name
        self.device = device
        self.token = token

    def _load_backend(self, wires: int) -> None:
        # If backend is None, must load backend.
        # If wires is larger than the number of qubits of the current backend, the backend can't be applied to the problem.
        # If token is available or backend is not specified, must update the least busy backend.
        # Otherwise, the current backend is also available to the Ising model.
        if (
            self.__backend is not None
            and wires <= self.__backend.configuration().n_qubits
            and (self.__token is None or not self.__backend_name is None)
        ):
            return

        if self.__device in ["CPU", "GPU"]:
            if self.__backend_name is not None:
                # Simulation of ideal machine with specified backend
                if self.__provider is not None:
                    if self.__backend_name in AerSimulator().available_methods():
                        self.__backend = AerSimulator(method=self.backend_name)
                    else:
                        # Simulation of actual machine with specified backend
                        self.__backend = AerSimulator.from_backend(
                            self.provider.get_backend(self.backend_name)
                        )
                else:
                    # Simulation of ideal machine with specified backend
                    self.__backend = AerSimulator(method=self.backend_name)
            else:
                if self.provider is not None:
                    # Simulation of actual machine with least busy backend
                    backend_list = self.provider.backends(
                        filters=lambda x: x.configuration().n_qubits >= wires
                        and not x.configuration().simulator
                    )
                    if backend_list == []:
                        raise RuntimeError("Available backend is not found.")
                    self.__backend = AerSimulator.from_backend(
                        least_busy((backend_list))
                    )
                else:
                    # Simulation of ideal machine with default simulator
                    self.__backend = AerSimulator(
                        method="automatic", device=self.device
                    )
        elif self.device == "QPU":
            if self.provider is not None:
                if self.backend_name is not None:
                    # Run an actual machine with specified backend
                    self.__backend = self.__provider.get_backend(self.__backend_name)
                else:
                    # Run an actual machine with least busy backend
                    backend_list = self.provider.backends(
                        filters=lambda x: x.configuration().n_qubits >= wires
                        and not x.configuration().simulator
                    )
                    if backend_list == []:
                        raise RuntimeError("Available backend is not found.")
                    self.__backend = least_busy(backend_list)
            else:
                raise RuntimeError('Specified device is "QPU", but a token is not set.')
        else:
            raise NotImplementedError("Invalid device is specified.")

        self.__backend.set_options(shots=self.shots)

        if self.__device in ["CPU", "GPU"]:
            self.__backend.set_options(device=self.device)

    def _generate_circuit(
        self,
        f_dict: Dict[Tuple[int, int], float],
        wires: int,
        reps: int,
        parameters: List[Parameter],
    ):
        # Generate Hamiltonian
        op_f = 0 * (I ^ wires)
        for key, value in f_dict.items():
            op_tmp = I ^ wires

            key = set(key)
            if len(key) > 0:
                for i in key:
                    op_tmp = op_tmp.compose(PauliZ(wires, i))
            op_f += value * op_tmp

        # Generate mixer
        op_mixer = 0 * (I ^ wires)
        for i in range(wires):
            op_mixer += PauliX(wires, i)

        # Generate whole circuit
        op_circuit = H ^ wires
        for idx in range(reps):
            op_circuit = (op_f * parameters[idx]).exp_i().compose(op_circuit)
            op_circuit = (op_mixer * parameters[reps + idx]).exp_i().compose(op_circuit)
        evolution = EvolutionFactory.build(op_f)
        op_circuit = evolution.convert(op_circuit)

        return op_f, op_mixer, op_circuit.to_circuit()

    def tune(
        self,
        f_dict: Dict[Tuple[int, int], float],
        wires: int,
        optimizer: str,
        initial_parameters: Optional[List[float]] = None,
    ) -> Dict[str, Any]:
        # Set shots to backend engine
        self._load_backend(wires)

        # Prepare parameters
        parameter_names = [Parameter(f"$\\gamma{i}$") for i in range(self.reps)]
        parameter_names += [Parameter(f"$\\beta{i}$") for i in range(self.reps)]
        if initial_parameters is None:
            initial_parameters = np.random.rand(2 * self.reps).tolist()

        # Generate expectation operation
        op_f, op_mixer, op_circuit = self._generate_circuit(
            f_dict, wires, self.reps, parameter_names
        )
        observable_meas = PauliExpectation().convert(
            operator=StateFn(op_f, is_measurement=True)
        )
        expect_operation = observable_meas.compose(CircuitStateFn(op_circuit)).reduce()

        # Define cost function
        parameter_values_history = list()

        def cost_function(parameter_values, parameter_names, backend, expect_operation):
            parameter_sets = np.reshape(parameter_values, (-1, len(parameter_values)))
            parameter_bindings = dict(
                zip(parameter_names, parameter_sets.transpose().tolist())
            )
            parameter_values_history.append(parameter_bindings)

            sampled_expect_op = CircuitSampler(
                backend,
                param_qobj=is_aer_provider(backend),
            ).convert(expect_operation, params=parameter_bindings)
            means = np.real(sampled_expect_op.eval())

            return means if len(means) > 1 else means[0]

        # Tune
        start = time.time()
        res = minimize(
            cost_function,
            initial_parameters,
            args=(parameter_names, self.backend, expect_operation),
            method=optimizer,
        )
        eval_time = time.time() - start

        result = {
            "evals": res["nfev"],
            "eval_time": eval_time,
            "opt_val": res["fun"],
            "opt_params": res["x"],
            "params_history": parameter_values_history,
        }
        return result

    def run(
        self,
        f_dict: Dict[Tuple[int, int], float],
        wires: int,
        parameters: List[float],
    ) -> Tuple[List[Tuple[List[int], int]], Dict[str, float]]:
        self._load_backend(wires)

        _, _, qc = self._generate_circuit(f_dict, wires, self.reps, parameters)
        qc.measure_all()

        qc = transpile(qc, self.backend)
        result = self.__backend.run(qc).result()
        counts = result.get_counts()
        time_taken = result.to_dict()["time_taken"]

        return decode_solutions(counts), {"time_taken": time_taken}
