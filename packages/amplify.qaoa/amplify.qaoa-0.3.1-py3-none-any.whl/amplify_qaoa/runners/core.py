from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Any, Dict, List, Optional, Tuple


def decode_solutions(raw_solution: Dict[str, int]) -> List[Tuple[List[int], int]]:
    return [
        ([-1 if int(i) > 0 else 1 for i in assignments], frequency)
        for (assignments, frequency) in raw_solution.items()
    ]


class AbstractQAOARunner(metaclass=ABCMeta):
    _shots: Optional[int] = None

    @property
    def shots(self):
        return self._shots

    @shots.setter
    def shots(self, value):
        self._shots = value

    def __init__(
        self,
        reps: int = 10,
        shots: Optional[int] = None,
    ) -> None:
        super().__init__()
        self.reps = reps
        self.shots = shots

    @abstractmethod
    def run(
        self,
        f_dict: Dict[Tuple[int, int], float],
        wires: int,
        parameters: List[float],
    ) -> Tuple[List[Tuple[List[int], int]], Dict[str, float]]:
        pass

    @abstractmethod
    def tune(
        self,
        f_dict: Dict[Tuple[int, int], float],
        wires: int,
        optimizer: str,
        initial_parameters: Optional[List[float]],
    ) -> Dict[str, Any]:
        pass
