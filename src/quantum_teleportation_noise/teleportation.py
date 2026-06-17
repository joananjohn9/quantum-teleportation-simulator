import numpy as np

from quantum_teleportation_noise.states import ket_0

from quantum_teleportation_noise.gates import (
    I,
    H,
    X,
    Z,
    apply_gate,
    kron3,
    cnot_23,
    cnot_12,
)


CNOT23 = cnot_23()
CNOT12 = cnot_12()


def extract_bob_state(state: np.ndarray, alice_bits: str) -> np.ndarray:
    if len(alice_bits) != 2:
        raise ValueError("alice_bits must be a two-bit string like '00', '01', '10', or '11'.")

    bob_state = np.zeros(2, dtype=complex)

    for index, amplitude in enumerate(state):
        bits = format(index, "03b")

        if bits[:2] == alice_bits:
            bob_bit = int(bits[2])
            bob_state[bob_bit] = amplitude

    norm = np.linalg.norm(bob_state)

    if norm == 0:
        raise ValueError(f"Measurement outcome {alice_bits} has zero probability.")

    return bob_state / norm


def correct_bob_state(bob_state: np.ndarray, alice_bits: str) -> np.ndarray:
    if alice_bits == "00":
        return apply_gate(I, bob_state)

    if alice_bits == "01":
        return apply_gate(X, bob_state)

    if alice_bits == "10":
        return apply_gate(Z, bob_state)

    if alice_bits == "11":
        return apply_gate(Z @ X, bob_state)

    raise ValueError("alice_bits must be one of: 00, 01, 10, 11")


def teleport_state(psi: np.ndarray) -> dict[str, np.ndarray]:
    results: dict[str, np.ndarray] = {}

    initial_state = kron3(psi, ket_0, ket_0)

    H2 = kron3(I, H, I)
    state_after_H2 = apply_gate(H2, initial_state)

    state_after_cnot23 = apply_gate(CNOT23, state_after_H2)
    state_after_cnot12 = apply_gate(CNOT12, state_after_cnot23)

    H1 = kron3(H, I, I)
    state_after_H1 = apply_gate(H1, state_after_cnot12)

    for outcome in ["00", "01", "10", "11"]:
        bob = extract_bob_state(state_after_H1, outcome)
        corrected = correct_bob_state(bob, outcome)
        results[outcome] = corrected

    return results