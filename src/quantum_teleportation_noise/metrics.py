import numpy as np


def fidelity(
    state1: np.ndarray,
    state2: np.ndarray
) -> float:
    overlap = np.vdot(state1, state2)

    return float(np.abs(overlap) ** 2)