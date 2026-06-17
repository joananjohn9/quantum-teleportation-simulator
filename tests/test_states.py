import numpy as np 

from quantum_teleportation_noise.states import (
    ket_0,
    ket_1,
    create_state,
    generate_random_qubit
)

def test_ket_0_is_correct():
    '''
    Function to test |0> state '''

    expected = np.array([1,0], dtype=complex)

    assert np.allclose(ket_0,expected)

def test_ket_1_is_correct():
    '''
    Function to test |1> state '''

    expected = np.array([0,1], dtype=complex)

    assert np.allclose(ket_1,expected)

def test_create_state_is_normalized():
    '''
    Function to test whether the state created
     is normalized '''

    psi = create_state(1+0j, 0+1j)

    assert np.isclose(np.linalg.norm(psi),1.0)

def test_random_qubit_is_normalized():
    '''
    Function to test whether created random qubit 
    is normalized 
    '''
    psi = generate_random_qubit()

    assert np.isclose(np.linalg.norm(psi),1.0)

def test_random_qubit_has_shape_two():
    '''
    Tests the shape of a qubit
    '''
    psi = generate_random_qubit()

    assert psi.shape == (2,)