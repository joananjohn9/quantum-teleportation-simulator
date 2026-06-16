# Mini Report: Quantum Teleportation Noise Simulator

## 1. Objective

The objective of this project is to implement a compact quantum teleportation simulator and quantify how depolarizing noise affects the final teleportation fidelity.

The project focuses on correctness and interpretability rather than using a black-box quantum computing library. The full protocol is implemented with density matrices, tensor products, projective measurement, and conditional correction operations.

## 2. Background

Quantum teleportation transfers an unknown qubit state from one system to another without physically sending the qubit itself. The protocol requires a shared entangled Bell pair and two classical bits of communication.

The input state is

```math
|\psi\rangle = \alpha |0\rangle + \beta |1\rangle.
```

Alice holds the unknown message qubit and one half of an entangled pair. Bob holds the other half. After Alice performs a CNOT gate, a Hadamard gate, and measurement, Bob applies a correction depending on Alice's two classical bits.

## 3. Method

The simulator uses a three-qubit density matrix:

- q0: message qubit
- q1: Alice's Bell-pair qubit
- q2: Bob's Bell-pair qubit

The protocol steps are:

1. Prepare the input state on q0.
2. Prepare a Bell pair between q1 and q2.
3. Apply CNOT(q0, q1).
4. Apply H(q0).
5. Projectively measure q0 and q1.
6. Apply Bob's correction on q2.
7. Trace out Alice's qubits.
8. Compute the fidelity between Bob's state and the original input state.

The depolarizing channel used in this project is

```math
\rho \rightarrow (1-p)\rho + \frac{p}{3}(X\rho X + Y\rho Y + Z\rho Z).
```

This channel is applied after every gate layer to all three qubits.

## 4. Results

The ideal fidelity is approximately 1, confirming that the teleportation protocol is implemented correctly. As the depolarizing noise probability increases, the fidelity decreases monotonically.

The project exports:

- `results/tables/fidelity_vs_noise.csv`
- `results/figures/fidelity_vs_noise.png`

## 5. Interpretation

The result shows that teleportation is exact in an ideal quantum circuit but becomes imperfect when gates are noisy. This is a useful demonstration of why quantum error correction, noise mitigation, and hardware-aware circuit design are important in practical quantum computing.

## 6. Limitations

This project uses a simplified depolarizing noise model. It does not include real-device calibration data, readout noise, relaxation times, crosstalk, or leakage errors.

## 7. Future Work

Natural extensions include implementing the same protocol in Qiskit, adding realistic noise models, comparing different input states, and testing the protocol on real quantum hardware.
