import numpy as np

from quantum_teleportation_noise.states import ket_0, ket_1

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


def test_identity_gate_preserves_state():
    result = apply_gate(I, ket_0)

    assert np.allclose(result, ket_0)


def test_hadamard_on_zero():
    result = apply_gate(H, ket_0)

    expected = (1 / np.sqrt(2)) * np.array(
        [1, 1],
        dtype=complex,
    )

    assert np.allclose(result, expected)


def test_hadamard_on_one():
    result = apply_gate(H, ket_1)

    expected = (1 / np.sqrt(2)) * np.array(
        [1, -1],
        dtype=complex,
    )

    assert np.allclose(result, expected)


def test_pauli_x_flips_zero_to_one():
    result = apply_gate(X, ket_0)

    assert np.allclose(result, ket_1)


def test_pauli_x_flips_one_to_zero():
    result = apply_gate(X, ket_1)

    assert np.allclose(result, ket_0)


def test_pauli_z_preserves_zero():
    result = apply_gate(Z, ket_0)

    assert np.allclose(result, ket_0)


def test_pauli_z_flips_phase_of_one():
    result = apply_gate(Z, ket_1)

    expected = -ket_1

    assert np.allclose(result, expected)


def test_kron3_state_dimension():
    state = kron3(ket_0, ket_0, ket_0)

    assert state.shape == (8,)


def test_kron3_gate_dimension():
    gate = kron3(I, H, I)

    assert gate.shape == (8, 8)


def test_cnot_23_maps_010_to_011():
    state_010 = np.zeros(8, dtype=complex)
    state_010[2] = 1.0

    result = apply_gate(cnot_23(), state_010)

    expected = np.zeros(8, dtype=complex)
    expected[3] = 1.0

    assert np.allclose(result, expected)


def test_cnot_12_maps_100_to_110():
    state_100 = np.zeros(8, dtype=complex)
    state_100[4] = 1.0

    result = apply_gate(cnot_12(), state_100)

    expected = np.zeros(8, dtype=complex)
    expected[6] = 1.0

    assert np.allclose(result, expected)