"""Noise channels for the teleportation simulator."""

from __future__ import annotations

import numpy as np

from quantum_utils import I2, X, Y, Z, apply_unitary, expand_single_qubit_gate


def depolarize_one_qubit(rho: np.ndarray, qubit: int, p: float, n_qubits: int = 3) -> np.ndarray:
    """
    Apply a single-qubit depolarizing channel:
    rho -> (1-p)rho + p/3 (XrhoX + YrhoY + ZrhoZ)
    """
    if not 0 <= p <= 1:
        raise ValueError("p must be between 0 and 1")

    x_full = expand_single_qubit_gate(X, qubit, n_qubits)
    y_full = expand_single_qubit_gate(Y, qubit, n_qubits)
    z_full = expand_single_qubit_gate(Z, qubit, n_qubits)

    return (
        (1 - p) * rho
        + (p / 3) * apply_unitary(rho, x_full)
        + (p / 3) * apply_unitary(rho, y_full)
        + (p / 3) * apply_unitary(rho, z_full)
    )


def depolarize_all_qubits(rho: np.ndarray, p: float, n_qubits: int = 3) -> np.ndarray:
    """Apply the same single-qubit depolarizing channel to every qubit."""
    noisy = rho
    for qubit in range(n_qubits):
        noisy = depolarize_one_qubit(noisy, qubit, p, n_qubits)
    return noisy
