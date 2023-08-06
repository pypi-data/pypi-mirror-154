from __future__ import annotations

import time
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from qulacs import Observable, PauliOperator, QuantumCircuit, QuantumState
from scipy.optimize import minimize

from .core import AbstractQAOARunner, decode_solutions


def generate_circuit(
    f_dict: Dict[Tuple[int, int], float],
    wires: int,
    parameters: List[float],
    reps: int,
) -> Tuple[QuantumCircuit, Observable]:
    op_f = Observable(wires)
    for key, value in f_dict.items():
        Paulistring = ""

        key = set(key)
        if len(key) > 0:
            for i in key:
                if Paulistring != "":
                    Paulistring += " "
                Paulistring += f"Z {i}"
        op_f.add_operator(PauliOperator(Paulistring, value))

    op_mixer = Observable(wires)
    for i in range(wires):
        Paulistring = f"X {i}"
        op_mixer.add_operator(PauliOperator(Paulistring, 1.0))

    circuit = QuantumCircuit(wires)
    for i in range(wires):
        circuit.add_H_gate(i)

    for idx in range(reps):
        circuit.add_observable_rotation_gate(op_f, parameters[idx], 1)
        circuit.add_observable_rotation_gate(op_mixer, parameters[idx + reps], 1)

    return circuit, op_f


class QulacsRunner(AbstractQAOARunner):
    def __init__(
        self,
        reps: int = 10,
        shots: Optional[int] = None,
    ) -> None:
        super().__init__(reps, shots)

    def tune(
        self,
        f_dict: Dict[Tuple[int, int], float],
        wires: int,
        optimizer: str = "COBYLA",
        initial_parameters: Optional[List[float]] = None,
    ) -> Dict[str, Any]:
        # Prepare parameters
        if initial_parameters is None:
            initial_parameters = np.random.rand(2 * self.reps).tolist()

        # Define cost function
        parameter_values_history = list()

        def cost_function(params_val):
            parameter_values_history.append(params_val)
            circuit, op_f = generate_circuit(f_dict, wires, params_val, self.reps)
            state = QuantumState(wires)
            circuit.update_quantum_state(state)
            return op_f.get_expectation_value(state)

        # Tune
        start = time.time()
        res = minimize(
            cost_function,
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

        start = time.time()
        circuit, _ = generate_circuit(f_dict, wires, parameters, self.reps)
        state = QuantumState(wires)
        circuit.update_quantum_state(state)
        probs = np.abs(state.get_vector()) ** 2
        z_basis = [format(i, "b").zfill(wires)[::-1] for i in range(probs.size)]
        counts = {
            z_basis[i]: int(probs[i] * (self.shots if self.shots is not None else 1e10))
            for i in range(probs.size)
            if int(probs[i] * (self.shots if self.shots is not None else 1e10)) >= 1
        }
        time_taken = time.time() - start

        return decode_solutions(counts), {"time_taken": time_taken}
