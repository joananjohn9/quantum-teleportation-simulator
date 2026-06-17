import numpy as np

from quantum_teleportation_noise.states import (
    create_state,
    generate_random_qubit,
)

from quantum_teleportation_noise.teleportation import (
    teleport_state,
    extract_bob_state,
)

from quantum_teleportation_noise.metrics import fidelity


def test_extract_bob_state_valid_outcome():
    state = np.zeros(8, dtype=complex)
    state[0] = 1 / np.sqrt(2)
    state[1] = 1 / np.sqrt(2)

    bob = extract_bob_state(state, "00")

    expected = np.array(
        [1 / np.sqrt(2), 1 / np.sqrt(2)],
        dtype=complex,
    )

    assert np.allclose(bob, expected)


def test_extract_bob_state_rejects_invalid_bit_length():
    state = np.zeros(8, dtype=complex)

    try:
        extract_bob_state(state, "0")
        assert False
    except ValueError:
        assert True


def test_teleportation_known_state_all_outcomes():
    psi = create_state(1 + 0j, 1j)

    results = teleport_state(psi)

    assert set(results.keys()) == {"00", "01", "10", "11"}

    for corrected_state in results.values():
        assert np.isclose(
            fidelity(psi, corrected_state),
            1.0,
        )


def test_teleportation_random_states():
    for _ in range(100):
        psi = generate_random_qubit()
        results = teleport_state(psi)

        for corrected_state in results.values():
            assert np.isclose(
                fidelity(psi, corrected_state),
                1.0,
            )