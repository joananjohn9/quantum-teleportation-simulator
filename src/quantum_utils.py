"""Small quantum-state utilities for a 3-qubit teleportation simulator."""

from __future__ import annotations

import numpy as np

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
P0 = np.array([[1, 0], [0, 0]], dtype=complex)
P1 = np.array([[0, 0], [0, 1]], dtype=complex)


def ket0() -> np.ndarray:
    return np.array([1, 0], dtype=complex)


def ket1() -> np.ndarray:
    return np.array([0, 1], dtype=complex)


def random_qubit_state(seed: int = 7) -> np.ndarray:
    """Return a normalized random one-qubit pure state."""
    rng = np.random.default_rng(seed)
    vec = rng.normal(size=2) + 1j * rng.normal(size=2)
    return vec / np.linalg.norm(vec)


def state_from_angles(theta: float, phi: float) -> np.ndarray:
    """Return cos(theta/2)|0> + exp(i phi) sin(theta/2)|1>."""
    return np.array(
        [np.cos(theta / 2), np.exp(1j * phi) * np.sin(theta / 2)], dtype=complex
    )


def density(psi: np.ndarray) -> np.ndarray:
    psi = np.asarray(psi, dtype=complex)
    return np.outer(psi, psi.conj())


def kron_all(operators: list[np.ndarray]) -> np.ndarray:
    result = operators[0]
    for op in operators[1:]:
        result = np.kron(result, op)
    return result


def expand_single_qubit_gate(gate: np.ndarray, qubit: int, n_qubits: int = 3) -> np.ndarray:
    """Expand a 1-qubit gate. Qubit 0 is the leftmost/most significant qubit."""
    ops = [I2 for _ in range(n_qubits)]
    ops[qubit] = gate
    return kron_all(ops)


def controlled_gate(control: int, target: int, gate: np.ndarray, n_qubits: int = 3) -> np.ndarray:
    """Build a controlled single-qubit gate."""
    ops0 = [I2 for _ in range(n_qubits)]
    ops1 = [I2 for _ in range(n_qubits)]
    ops0[control] = P0
    ops1[control] = P1
    ops1[target] = gate
    return kron_all(ops0) + kron_all(ops1)


def apply_unitary(rho: np.ndarray, unitary: np.ndarray) -> np.ndarray:
    return unitary @ rho @ unitary.conj().T


def partial_trace(rho: np.ndarray, keep: list[int], dims: list[int]) -> np.ndarray:
    """Partial trace over all subsystems not in keep."""
    n = len(dims)
    keep = sorted(keep)
    traced = [i for i in range(n) if i not in keep]
    reshaped = rho.reshape(dims + dims)
    for subsystem in reversed(traced):
        reshaped = np.trace(reshaped, axis1=subsystem, axis2=subsystem + n)
        dims.pop(subsystem)
        n -= 1
    dim_keep = int(np.prod(dims))
    return reshaped.reshape((dim_keep, dim_keep))


def state_fidelity_with_pure_state(rho: np.ndarray, psi: np.ndarray) -> float:
    """F(|psi>, rho) = <psi|rho|psi>."""
    psi = psi.reshape((-1, 1))
    value = (psi.conj().T @ rho @ psi).item()
    return float(np.real_if_close(value))
