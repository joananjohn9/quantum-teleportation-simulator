"""Three-qubit quantum teleportation simulation using density matrices."""

from __future__ import annotations

import numpy as np

from noise import depolarize_all_qubits
from quantum_utils import (
    H,
    I2,
    X,
    Z,
    controlled_gate,
    density,
    expand_single_qubit_gate,
    ket0,
    partial_trace,
    state_fidelity_with_pure_state,
)


def _projector_for_measurement(m0: int, m1: int) -> np.ndarray:
    """Project qubits 0 and 1 onto computational-basis outcomes m0,m1."""
    p0 = np.array([[1, 0], [0, 0]], dtype=complex)
    p1 = np.array([[0, 0], [0, 1]], dtype=complex)
    return np.kron(np.kron(p1 if m0 else p0, p1 if m1 else p0), I2)


def teleport_state(input_state: np.ndarray, noise_probability: float = 0.0) -> tuple[np.ndarray, float]:
    """
    Teleport a one-qubit pure state from Alice to Bob.

    Qubit layout:
    q0 = message qubit
    q1 = Alice's entangled qubit
    q2 = Bob's entangled qubit

    Returns:
    output density matrix of Bob's qubit, fidelity with input state.
    """
    initial_state = np.kron(np.kron(input_state, ket0()), ket0())
    rho = density(initial_state)

    # Prepare Bell pair between q1 and q2.
    rho = _apply(rho, expand_single_qubit_gate(H, qubit=1, n_qubits=3), noise_probability)
    rho = _apply(rho, controlled_gate(control=1, target=2, gate=X, n_qubits=3), noise_probability)

    # Alice entangles the message with her half of the Bell pair.
    rho = _apply(rho, controlled_gate(control=0, target=1, gate=X, n_qubits=3), noise_probability)
    rho = _apply(rho, expand_single_qubit_gate(H, qubit=0, n_qubits=3), noise_probability)

    # Measurement outcomes on Alice's two qubits and Bob's classical corrections.
    corrected_rho = np.zeros_like(rho)
    for m0 in [0, 1]:
        for m1 in [0, 1]:
            projector = _projector_for_measurement(m0, m1)
            branch = projector @ rho @ projector.conj().T
            probability = np.trace(branch).real
            if probability < 1e-15:
                continue
            branch = branch / probability

            # If Alice's q1 measurement is 1, Bob applies X.
            # If Alice's q0 measurement is 1, Bob applies Z.
            correction = np.eye(8, dtype=complex)
            if m1 == 1:
                correction = expand_single_qubit_gate(X, qubit=2, n_qubits=3) @ correction
            if m0 == 1:
                correction = expand_single_qubit_gate(Z, qubit=2, n_qubits=3) @ correction
            branch = correction @ branch @ correction.conj().T
            corrected_rho += probability * branch

    bob_state = partial_trace(corrected_rho, keep=[2], dims=[2, 2, 2])
    fidelity = state_fidelity_with_pure_state(bob_state, input_state)
    return bob_state, fidelity


def _apply(rho: np.ndarray, unitary: np.ndarray, noise_probability: float) -> np.ndarray:
    rho = unitary @ rho @ unitary.conj().T
    if noise_probability > 0:
        rho = depolarize_all_qubits(rho, noise_probability, n_qubits=3)
    return rho
