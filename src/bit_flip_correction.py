"""
Example demonstrating bit-flip error correction using a three-qubit code.

This example shows how to:
1. Encode a single qubit state into a three-qubit entangled state
2. Simulate a bit-flip error
3. Detect and correct the error using syndrome measurements
4. Decode the state back to a single qubit
"""

from bloqade import qasm2
from bloqade.pyqrack import PyQrack


@qasm2.extended
def create_bit_flip_circuit(q: qasm2.QReg):
    # Prepare initial state with Hadamard
    qasm2.h(q[0])

    # Encode into three-qubit state
    qasm2.cx(q[0], q[1])  # CNOT from qubit 0 to 1
    qasm2.cx(q[0], q[2])  # CNOT from qubit 0 to 2

    # Simulate bit-flip error on second qubit
    qasm2.x(q[1])

    # Add syndrome qubits and measure
    qasm2.cx(q[0], q[3])  # First syndrome
    qasm2.cx(q[1], q[3])
    qasm2.cx(q[0], q[4])  # Second syndrome
    qasm2.cx(q[2], q[4])

    # Measure syndrome qubits
    qasm2.measure(q[3], qasm2.creg(1)[0])  # First syndrome measurement
    qasm2.measure(q[4], qasm2.creg(2)[0])  # Second syndrome measurement

    # Error correction based on syndrome (will be classical controlled)
    # Note: In real hardware, this would be controlled by classical measurement results
    qasm2.x(q[1])  # Correct the error we introduced

    # Decode back to single qubit
    qasm2.cx(q[0], q[1])
    qasm2.cx(q[0], q[2])

    # Final measurement of the corrected qubit
    qasm2.measure(q[0], qasm2.creg(3)[0])

    return q


@qasm2.extended
def main():
    # Create a 5-qubit register (3 for encoding, 2 for syndrome)
    q = qasm2.qreg(5)
    return create_bit_flip_circuit(q)


def visualize_circuit():
    """Create and visualize the bit-flip correction circuit."""
    # Create the circuit
    target = qasm2.emit.QASM2()
    ast = target.emit(main)
    qasm2.parse.pprint(ast)


def run_simulation():
    """Run the circuit on PyQrack simulator."""
    device = PyQrack()
    result = device.run(main)
    print("\nSimulation Results:")
    print(result)


if __name__ == "__main__":
    print("Bit-Flip Error Correction Example")
    print("--------------------------------")

    # Visualize the circuit
    print("\nGenerating circuit visualization...")
    visualize_circuit()

    # Run the simulation
    print("\nRunning simulation...")
    run_simulation()

    print("\nNote: This example demonstrates the basic structure of bit-flip error correction.")
    print("In a real quantum computer, the error correction would be controlled by")
    print("classical measurement results from the syndrome qubits.")
