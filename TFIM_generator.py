from qiskit import QuantumCircuit
import subprocess
import os

def generate_TFIM_gates(qubits, steps, dt, g, location):
    exe = location+"/release/examples/f3c_time_evolution_TFYZ"
    gates = []
    
    if not os.path.exists("TFIM_Operators"):
        os.mkdir("TFIM_Operators")
    
    # steps = steps - 1     
    # with open("TFIM_Operators/Operator_Generator.ini", 'w+') as f:
    #     f.write("[Qubits]\nnumber = "+str(qubits)+"\n\n")
    #     f.write("[Trotter]\nsteps = 1\ndt = 0\n\n")
    #     f.write("[Jy]\nvalue = 0\n\n")
    #     f.write("[Jz]\nvalue = 1\n\n")
    #     f.write("[hx]\nramp = constant\nvalue = "+str(g)+"\n\n")
    #     f.write("[Output]\nname = TFIM_Operators/n="+str(qubits)+"_g="+str(g)+"_dt=0_i=\nimin = 1\nimax = 2\nstep = 1\n")
    # subprocess.run([exe, "TFIM_Operators/Operator_Generator.ini"])
    # os.remove("TFIM_Operators/Operator_Generator.ini")
    # qc = QuantumCircuit.from_qasm_file("TFIM_Operators/n="+str(qubits)+"_g="+str(g)+"_dt=0_i=1.qasm")
    # gates.append(qc.to_gate(label = "TFIM 1").control())
    # os.remove("TFIM_Operators/n="+str(qubits)+"_g="+str(g)+"_dt=0_i=1.qasm")

    with open("TFIM_Operators/Operator_Generator.ini", 'w+') as f:
        f.write("[Qubits]\nnumber = "+str(qubits)+"\n\n")
        f.write("[Trotter]\nsteps = "+str(steps)+"\ndt = "+str(dt)+"\n\n")
        f.write("[Jy]\nvalue = 0\n\n")
        f.write("[Jz]\nvalue = 1\n\n")
        f.write("[hx]\nramp = constant\nvalue = "+str(g)+"\n\n")
        f.write("[Output]\nname = TFIM_Operators/n="+str(qubits)+"_g="+str(g)+"_dt="+str(dt)+"_i=\nimin = 1\nimax = "+str(steps+1)+"\nstep = 1\n")
    exe = location+"/release/examples/f3c_time_evolution_TFYZ"
    subprocess.run([exe, "TFIM_Operators/Operator_Generator.ini"])
    os.remove("TFIM_Operators/Operator_Generator.ini")
    for step in range(steps):
        qc = QuantumCircuit.from_qasm_file("TFIM_Operators/n="+str(qubits)+"_g="+str(g)+"_dt="+str(dt)+"_i="+str(step+1)+".qasm")
        gates.append(qc.to_gate(label = "TFIM "+str(step+2)).control())
        os.remove("TFIM_Operators/n="+str(qubits)+"_g="+str(g)+"_dt="+str(dt)+"_i="+str(step+1)+".qasm")
    os.rmdir("TFIM_Operators")
    return gates

# from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
# from qiskit.circuit.library import QFT
# from qiskit_aer import AerSimulator
# from numpy import pi

# particles = 2
# Dt = .1
# gates = [generate_TFIM_gates(particles, int(2*pi/Dt), Dt, 10, '../f3cpp')[1]]

# s_k =[]
# for controlled_U in gates:
#     bits = 20
#     qr_ancilla = QuantumRegister(bits)
#     qr_eigen   = QuantumRegister(particles)
#     cr         = ClassicalRegister(bits)

#     qc = QuantumCircuit(qr_ancilla, qr_eigen, cr)
#     qc.h(qr_ancilla)
#     qc.h(qr_eigen)
#     qc.barrier()
    
#     for i in range(len(qr_ancilla)):
#         for _ in range(i):
#             qc.append(controlled_U, qargs=[qr_ancilla[i]]+qr_eigen[:] )
#     qc.append(QFT(bits, inverse = True), qr_ancilla)
#     for i in range(len(qr_ancilla)): qc.measure(qr_ancilla[i], cr[i])
#     # print(qc)
#     aer_sim = AerSimulator()
#     trans_qc = transpile(qc, aer_sim)
#     counts = aer_sim.run(trans_qc, shots = 10**4).result().get_counts()
#     binary_num = ''
#     max_num = 0
#     for key in counts:
#         if (counts[key] > max_num):
#             max_num = counts[key]
#             binary_num = key
#     # print("Binary Number with Maximum count:     0."+binary_num)
#     decimal_num = 0
#     for i in range(len(binary_num)):
#         decimal_num += int(binary_num[i])/2**(i+1)
#     s_k.append(decimal_num)
# print(s_k)

