from __future__ import annotations

import time
from typing import Dict, List, Optional, Tuple

import pennylane as qml
from pennylane import numpy as np
from pennylane import qaoa
from scipy.optimize import minimize

from .core import AbstractQAOARunner, decode_solutions


def generate_circuit(f_dict, wires, parameters, reps):
    coeffs = []
    obs = []
    for key, value in f_dict.items():
        key = set(key)
        if len(key) > 0:
            key = list(key)
            coeffs.append(value)
            tmp_obs = qml.PauliZ(key[0])
            if len(key) > 1:
                for i in key[1:]:
                    tmp_obs @= qml.PauliZ(i)
            obs.append(tmp_obs)
    op_f = qml.Hamiltonian(coeffs, obs)

    coeffs = []
    obs = []
    for i in range(wires):
        coeffs.append(1.0)
        obs.append(qml.PauliX(i))
    op_mixer = qml.Hamiltonian(coeffs, obs)

    def get_layer(gamma, alpha):
        qaoa.cost_layer(gamma, op_f)
        qaoa.mixer_layer(alpha, op_mixer)

    params_node = np.zeros((2, reps))
    for i in range(reps):
        params_node[0][i] = parameters[2 * i]
        params_node[1][i] = parameters[2 * i + 1]

    for i in range(wires):
        qml.Hadamard(wires=i)

    qml.layer(get_layer, reps, params_node[0], params_node[1])

    return op_f


class PennyLaneRunner(AbstractQAOARunner):
    def __init__(
        self,
        reps: int = 10,
        shots: Optional[int] = None,
        device: str = "default.qubit",
    ) -> None:
        super().__init__(reps, shots)
        self.device = device

    def tune(
        self,
        f_dict: Dict[Tuple[int, int], float],
        wires: int,
        optimizer: str = "COBYLA",
        initial_parameters: Optional[List[float]] = None,
    ):
        # Prepare parameters
        if initial_parameters is None:
            initial_parameters = np.random.rand(2 * self.reps).tolist()

        # Define cost function
        parameter_values_history = list()

        def cost_function(params_val):
            parameter_values_history.append(params_val)
            op_f = generate_circuit(f_dict, wires, params_val, self.reps)
            return qml.expval(op_f)

        # Tune
        qnode_cost_function = qml.QNode(
            cost_function, qml.device(self.device, wires=wires)
        )
        start = time.time()
        res = minimize(
            qnode_cost_function,
            initial_parameters,
            method=optimizer,
        )
        eval_time = time.time() - start

        # Form result
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
        def generate_prob_circuit(params_val):
            _ = generate_circuit(f_dict, wires, params_val, self.reps)
            return qml.probs(wires=range(wires))

        start = time.time()
        probs = qml.QNode(generate_prob_circuit, qml.device(self.device, wires=wires))(
            parameters
        )
        z_basis = [format(i, "b").zfill(wires) for i in range(probs.size)]
        counts = {
            z_basis[i]: int(probs[i] * (self.shots if self.shots is not None else 1e10))
            for i in range(probs.size)
            if int(probs[i] * (self.shots if self.shots is not None else 1e10)) >= 1
        }
        time_taken = time.time() - start

        return decode_solutions(counts), {"time_taken": time_taken}
