#!/usr/bin/env python3

# create a general circuit that the user can design it by chosing the input

def dj_oracle(case, n):
    general_oracle = QuantumCircuit(n+1)

    if case == 'constant':
        output = np.random.randint(2)
        if output == 1:
            general_oracle.x(n)

    if case == 'balanced':
        b = np.random.randint(1,2**n)

        b_str = format(b, '0'+str(n)+'b')

        for qubit in range(len(b_str)):
            if b_str[qubit] == '1':
                general_oracle.x(qubit)

        for qubit in range(n):
            general_oracle.cx(qubit, n)

        for qubit in range(len(b_str)):
            if b_str[qubit] == '1':
                general_oracle.cx(qubit)

    oracle_gate = general_oracle.to_gate()
    oracle_gate.name = "Oracle"
    return oracle_gate


def dj_algorithm(oracle, n):
    dj_circuit = QuantumCircuit(n+1, n)

    # Set up the output qubit:
    dj_circuit.x(n)
    dj_circuit.h(n)

    # And set up the input register:
    for qubit in range(n):
        dj_circuit.h(qubit)

    # Let's append the oracle gate to our circuit:
    dj_circuit.append(oracle, range(n+1))
    
    # Finally, perform the H-gates again and measure:
    for qubit in range(n):
        dj_circuit.h(qubit)
    
    for i in range(n):
        dj_circuit.measure(i, i)
    
    return dj_circuit                                

def DeutschCircuit(case, n):
     oracle_gate = dj_oracle(case, n)
     dj_circuit = dj_algorithm(oracle_gate, n)

     return dj_circuit


def Draw_histogram(circuit):
     aer_sim = Aer.get_backend('aer_simulator')
     transpiled_circuit = transpile(circuit, aer_sim)
     qobj = assemble(transpiled_circuit)
     results = aer_sim.run(qobj).result()
     answer = results.get_counts()
     plot = plot_histogram(answer)
    
     return plot


def which_case(circuit):

     aer_sim = Aer.get_backend('aer_simulator')
     transpiled_circuit = transpile(circuit, aer_sim)
     qobj = assemble(transpiled_circuit)
     results = aer_sim.run(qobj).result()
     answer = results.get_counts()

     result=max(answer, key=answer.get)
     for i,e in enumerate(result):
         if i==0:
             first=e
         else:
             if e!=first:
                 print("Not Recognized")
                 break
     if i==len(result)-1:
         if first==0:
             print("Constant")
         else:
             print("Balanced")
     
     return result   
     