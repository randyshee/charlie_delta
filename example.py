import math
from bloqade import qasm2

@qasm2.extended
def qft(qreg: qasm2.QReg, n: int):
    if n == 0:
        return qreg

    qasm2.h(qreg[0])
    for i in range(1, n):
        qasm2.cu1(qreg[i], qreg[0], 2 * math.pi / 2**i)
    qft(qreg, n - 1)
    return qreg