import numpy as np

from hmm_functions import HMMParam, get_default_HMM_parameters, write_HMM_to_file

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# Make test data
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
def create_test_data(data_set_length):
    '''Create test data set of size data_set_length. Also create uniform weights and uniform mutation rates'''
    np.random.seed(42)

    window_size = 1000
    mutation_rate_window = 1000000

    # Initialization parameters (prob of staring in states)
    state_values = [0,1]
    hmm_parameters = get_default_HMM_parameters()

    print('creating 2 chromosomes with 50 Mb of test data (100K bins) with the following parameters..\n')
    print(hmm_parameters)  

    mutation_matrix = {
        'A': [0, 0.16, 0.68, 0.16],
        'C': [0.16, 0,0.16, 0.68],
        'G': [0.68, 0.16, 0, 0.16],
        'T': [0.16, 0.68, 0.16, 0],
    }
    bases = ['A','C','G','T']

    # Make obs file
    with open('obs.txt','w') as obs:

        print('chrom', 'pos', 'ancestral_base', 'genotype', sep = '\t', file = obs)

        for chrom in ['chr1', 'chr2']:
            for index in range(data_set_length):
                if index == 0:
                    current_state = np.random.choice(state_values, p=hmm_parameters.starting_probabilities)
                else:
                    current_state = np.random.choice(state_values, p=hmm_parameters.transitions[prevstate] )

                n_mutations = np.random.poisson(lam=hmm_parameters.emissions[current_state]) 
                for mutation in [int(x) for x in np.random.uniform(low=index*window_size, high=index*window_size + window_size, size=n_mutations)]: 
                    ancestral_base = np.random.choice(bases, p=[0.31, 0.19, 0.19, 0.31])
                    derived_base = np.random.choice(bases, p=mutation_matrix[ancestral_base])
                    print(chrom, mutation, ancestral_base, ancestral_base + derived_base, sep = '\t', file = obs)          

                prevstate = current_state

    # Make mutation file
    with open('mutrates.bed','w') as mutrates:
        for chrom in ['chr1', 'chr2']:
            for start in range(int(data_set_length * window_size / mutation_rate_window)):
                print(chrom, start * mutation_rate_window, (start + 1) * mutation_rate_window, 1, sep = '\t', file = mutrates)

    # Make weights file
    with open('weights.bed','w') as weights:
        for chrom in ['chr1', 'chr2']:
            print(chrom, 1, data_set_length * window_size, sep = '\t', file = weights)

    # Make initial guesses
    initial_guess = HMMParam(['Human', 'Archaic'], [0.5, 0.5], [[0.99,0.01],[0.02,0.98]], [0.03, 0.3])
    write_HMM_to_file(initial_guess, 'Initialguesses.json')