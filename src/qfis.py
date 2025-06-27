from qiskit import QuantumRegister, QuantumCircuit, ClassicalRegister, qpy
from qiskit.primitives import StatevectorSampler
import numpy as np
from .fuzzy import FuzzyInput, FuzzyOutput

def init_fis():
    sao2_red  = FuzzyInput('SaO2 Reduction', 0, 100)
    sao2_red.add_tag('low', 'linzmf', [1, 2])
    sao2_red.add_tag('normal', 'trapmf', [1.8, 2, 4, 5])
    sao2_red.add_tag('high', 'trapmf', [4, 6, 8, 10])
    sao2_red.add_tag('very_high', 'linsmf', [9, 12])

    sao2_red_dur = FuzzyInput('SaO2 Red. Duration', 0, 400)
    sao2_red_dur.add_tag('very_short', 'linzmf', [3, 4])
    sao2_red_dur.add_tag('short', 'trapmf', [3, 4, 5, 6])
    sao2_red_dur.add_tag('normal', 'trapmf', [5, 6.5, 35, 60])
    sao2_red_dur.add_tag('large', 'trapmf', [35, 45, 120, 130])
    sao2_red_dur.add_tag('very_large', 'linsmf', [120, 130])

    event = FuzzyOutput('Event', 0, 1)
    event.add_tag('very_low', 0.0)
    event.add_tag('low', 0.3)
    event.add_tag('normal', 0.5)
    event.add_tag('high', 0.7)
    event.add_tag('very_high', 1.0)
    
    return sao2_red, sao2_red_dur, event

def get_quantum_circuit(fuzzy_inputs):
    """Builds the quantum circuit.

    Args:
        fuzzy_inputs (List[float]): Values of the crisp inputs.
    """

    def _init_amplitudes(values, n_qbits):
        amplitudes = values
        while len(amplitudes) < 2**n_qbits:
            amplitudes = np.append(amplitudes, [0])
        total = sum(amplitudes)
        if total > 1.0:                 # If probability exceeds 1.0, we normalize the values
            amplitudes /= total
        elif total < 1.0:               # If probability lies below 1.0, we add the remaining probability to a garbage state
            amplitudes[-1] = 1.0 - total
        return list(np.sqrt(amplitudes))

    if len(fuzzy_inputs) != 2:
        raise ValueError(f'Unexpected number of input values, expected 2 but \'{len(fuzzy_inputs)}\' were given.')

    sao2_red, sao2_red_dur, event = init_fis()

    # Create circuit
    fuzzy_vars = [sao2_red, sao2_red_dur, event]
    qregs = {}
    for fuzzy_var in fuzzy_vars:
        n_tags = len(fuzzy_var.tags)
        n_qbits = int(np.ceil(np.log2(n_tags))) + 1
        qregs[fuzzy_var.name] = QuantumRegister(n_qbits)
    
    creg = ClassicalRegister(int(np.ceil(np.log2(len(event.tags)))) + 1, 'meas') # type: ignore
    qc = QuantumCircuit(*qregs.values(), creg)

    # Init states
    for fuzzy_input, fuzzy_var in zip(fuzzy_inputs, [sao2_red, sao2_red_dur]):
        fuzzy_values = np.array(list(fuzzy_var.evaluate(fuzzy_input).values()))
        qc.prepare_state(_init_amplitudes(fuzzy_values, len(qregs[fuzzy_var.name])), qregs[fuzzy_var.name], label=f'{fuzzy_var.name}_init')
        
    with open("rules.qpy", "rb") as file:
        rules = qpy.load(file)[0]
    qc.append(rules, qc.qubits)
    
    qc.measure(qregs[event.name], reversed(creg)) # type: ignore
    return qc

def run_quantum_circuit(fuzzy_inputs):
    """Runs the quantum circuit on StatevectorSampler and returns the defuzzified result (crisp output).

    Args:
        fuzzy_inputs (List[float]): Values of the crisp inputs.
    """
    
    def _process_result(result):
        _, _, event = init_fis()
        outputs = {}
        for tag in event.tags: # type: ignore
            tag_bin = '0' + format(event.tags.index(tag), "#0{}b".format((int(np.ceil(np.log2(len(event.tags))) + 2))))[2:][::-1] # type: ignore
            if tag_bin in result.keys():
                outputs[tag.name] = result[tag_bin]

        good_shots = 0
        for _,v in outputs.items():
            good_shots += v

        if good_shots == 0:
            return 0

        num = 0
        for tag in event.tags: # type: ignore
            if tag.name in outputs.keys():
                num += tag.mf.evaluate(outputs[tag.name])

        return num/good_shots

    SHOTS = 4096
    qc = get_quantum_circuit(fuzzy_inputs)

    sampler = StatevectorSampler()
    job = sampler.run([qc], shots=SHOTS)
    result = job.result()[0].data.meas.get_counts()

    return _process_result(result)


if __name__ == '__main__':    
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-gqc", "--get_quantum_circuit", help="Calls the get_quantum_circuit() method.", action="extend", nargs='+', type=float)
    parser.add_argument("-rqc", "--run_quantum_circuit", help="Calls the run_quantum_circuit() method.", action="extend", nargs='+', type=float)
    args = parser.parse_args()
    
    if args.get_quantum_circuit:
        qc = get_quantum_circuit(args.get_quantum_circuit)
        print(qc.decompose(reps=1))

    if args.run_quantum_circuit:
        results = run_quantum_circuit(args.run_quantum_circuit)
        print(results)