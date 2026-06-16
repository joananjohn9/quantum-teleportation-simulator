import numpy as np 

# Define the qubits
ket_0 = np.array([1,0],dtype=complex) # |0> 
ket_1 = np.array([0,1],dtype=complex) # |1> 



def normalize(state):
    ''' 
    Function normalizes a given state 
    '''

    norm = np.linalg.norm(state) 
    
    if norm == 0:
        raise ValueError("Cannot normalize the zero vector")
    
    return state/norm 

def create_state(alpha: complex, beta : complex) -> np.ndarray:
    
    return normalize(alpha* ket_0 + beta*ket_1)

    
def generate_random_qubit() -> np.ndarray:
    alpha = np.random.randn() + 1j * np.random.randn()
    beta = np.random.randn() + 1j * np.random.randn()

    return normalize(alpha * ket_0 + beta * ket_1)