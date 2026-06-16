import numpy as np

from src.quantum_teleportation_noise.states import generate_random_qubit
from src.quantum_teleportation_noise.teleportation import teleport_state
from src.quantum_teleportation_noise.metrics import fidelity


N_TESTS = 100

fidelities = []

for _ in range(N_TESTS):
    psi = generate_random_qubit()
    results = teleport_state(psi)

    for corrected_state in results.values():
        F = fidelity(psi, corrected_state)
        fidelities.append(F)

fidelities = np.array(fidelities)

print("Quantum Teleportation Validation")
print("--------------------------------")
print(f"Random states tested: {N_TESTS}")
print(f"Total corrected outcomes tested: {len(fidelities)}")
print(f"Average fidelity: {np.mean(fidelities):.12f}")
print(f"Minimum fidelity: {np.min(fidelities):.12f}")
print(f"Maximum fidelity: {np.max(fidelities):.12f}")