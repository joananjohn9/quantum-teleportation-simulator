import numpy as np  

# Make gates 

I = np.array(
    [
        [1,0],
        [0,1]
    ],
    dtype=complex
) # Identity gate

H = 1 / (np.sqrt(2)) * np.array(
    [
        [1,1],
        [1,-1]
    ],
    dtype=complex
) # Hadamard gate 


X = np.array(
    [
        [0,1],
        [1,0]
    ],
    dtype = complex
)

Z = np.array(
    [
        [1, 0],
        [0, -1],
    ],
    dtype=complex,
)

def apply_gate(gate,state) -> np.ndarray:
    return gate@state 

def kron3(a,b,c) -> np.ndarray:
    return np.kron(
        np.kron(a,b),
        c
    )

def cnot_23() -> np.ndarray:

    matrix = np.zeros((8,8),dtype=complex) 

    for index in range(8):
        #change index to bits
        bits = format(index,"03b")
        q1,q2,q3 = bits 

        if q2 == "1":
            q3 = "0" if q3 == "1" else "1"

        new_bits = q1+q2+q3
        new_index = int(new_bits,2)

        matrix[new_index,index] = 1


    return matrix

def cnot_12() -> np.ndarray:
    matrix = np.zeros((8,8),dtype=complex)

    for index in range(8):
        bits = format(index,"03b")
        q1,q2,q3 = bits 
        
        if q1 == "1":
            q2 = "0" if q2 == "1" else "1"

        new_bits = q1+q2+q3 
        new_index = int(new_bits,2)

        matrix[new_index, index] = 1


    return matrix