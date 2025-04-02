from qiskit import QuantumCircuit
import subprocess
import os

def generate_TFIM_gates(qubits, steps, dt, g, location):
    exe = location+"/release/examples/f3c_time_evolution_TFYZ"
    gates = []
    
    if not os.path.exists("TFIM_Operators"):
        os.mkdir("TFIM_Operators")
    
    # add timestep where dt = 0
    with open("TFIM_Operators/Operator_Generator.ini", 'w+') as f:
        f.write("[Qubits]\nnumber = "+str(qubits)+"\n\n")
        f.write("[Trotter]\nsteps = 1\ndt = 0\n\n") # maybe need new number for steps
        f.write("[Jy]\nvalue = 0\n\n")
        f.write("[Jz]\nvalue = 1\n\n")
        f.write("[hx]\nramp = constant\nvalue = "+str(g)+"\n\n")
        f.write("[Output]\nname = TFIM_Operators/n="+str(qubits)+"_g="+str(g)+"_dt="+str(dt)+"_i=\nimin = 1\nimax = 2\nstep = 1\n")
    exe = location+"/release/examples/f3c_time_evolution_TFYZ"
    subprocess.run([exe, "TFIM_Operators/Operator_Generator.ini"])
    os.remove("TFIM_Operators/Operator_Generator.ini")
    qc = QuantumCircuit.from_qasm_file("TFIM_Operators/n="+str(qubits)+"_g="+str(g)+"_dt="+str(dt)+"_i=1.qasm")
    gate = qc.to_gate(label = "TFIM 0").control()
    gates.append(gate)
    os.remove("TFIM_Operators/n="+str(qubits)+"_g="+str(g)+"_dt="+str(dt)+"_i=1.qasm")
    steps=steps-1

    with open("TFIM_Operators/Operator_Generator.ini", 'w+') as f:
        f.write("[Qubits]\nnumber = "+str(qubits)+"\n\n")
        f.write("[Trotter]\nsteps = "+str(steps)+"\ndt = "+str(dt)+"\n\n") # maybe need new number for steps
        f.write("[Jy]\nvalue = 0\n\n")
        f.write("[Jz]\nvalue = 1\n\n")
        f.write("[hx]\nramp = constant\nvalue = "+str(g)+"\n\n")
        f.write("[Output]\nname = TFIM_Operators/n="+str(qubits)+"_g="+str(g)+"_dt="+str(dt)+"_i=\nimin = 1\nimax = "+str(steps+1)+"\nstep = 1\n")
    exe = location+"/release/examples/f3c_time_evolution_TFYZ"
    subprocess.run([exe, "TFIM_Operators/Operator_Generator.ini"])
    os.remove("TFIM_Operators/Operator_Generator.ini")
    for step in range(steps):
        qc = QuantumCircuit.from_qasm_file("TFIM_Operators/n="+str(qubits)+"_g="+str(g)+"_dt="+str(dt)+"_i="+str(step+1)+".qasm")
        gate = qc.to_gate(label = "TFIM "+str(step+1)).control()
        gates.append(gate)
        os.remove("TFIM_Operators/n="+str(qubits)+"_g="+str(g)+"_dt="+str(dt)+"_i="+str(step+1)+".qasm")
    os.rmdir("TFIM_Operators")
    return gates


# from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
# from qiskit.circuit.library import QFT
# from qiskit_aer import AerSimulator
# from numpy import pi

# particles  = 2
# bits       = 1
# qr_ancilla = QuantumRegister(bits)
# qr_eigen   = QuantumRegister(particles)
# cr         = ClassicalRegister(bits)
# Dt         = 1
# shots      = 100
# g          = 1
# gates      = generate_TFIM_gates(particles, 2*int(2*pi/Dt)+1, Dt, g, '../f3cpp')

# for controlled_U in gates:
#     qc = QuantumCircuit(qr_ancilla, qr_eigen, cr)
#     qc.h(qr_ancilla)
#     qc.h(qr_eigen)
#     qc.barrier()

#     for i in range(len(qr_ancilla)):
#         for _ in range(2**(i)):
#             qc.append(controlled_U, qargs=[qr_ancilla[i]]+qr_eigen[:] )
#     qc.append(QFT(bits, inverse = True), qr_ancilla)
#     for i in range(len(qr_ancilla)): qc.measure(qr_ancilla[i], cr[i])
#     # print(qc)
#     aer_sim = AerSimulator()
#     trans_qc = transpile(qc, aer_sim)
#     counts = aer_sim.run(trans_qc, shots = shots).result().get_counts()
#     p0 = 0
#     if counts.get('0') is not None:
#         p0 = counts['0']/shots
#     meas = 2*p0-1
#     print(meas)