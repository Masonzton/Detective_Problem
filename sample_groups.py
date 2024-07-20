"""Sample groups by brute force iterating and other nonsense"""
from typing import List
from itertools import chain, combinations
import itertools

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    # want to exclude interviews with whole set and empty set
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)))

N = 6
all_combs: List[str] = []

for i in range(N):
    for j in range(N):
        if i == j:
            continue
        entry = ["O" for i in range(N)]
        entry[i] = "X"
        entry[j] = "W"

        all_combs.append("".join(entry))

def debug_length(input_list: List[str], debug=False):
    unique_x_positions = set()
    unique_w_positions = set()
    for comb in input_list:
        idx = comb.find("X")
        assert idx >= 0
        unique_x_positions.add(idx)
        idx = comb.find("W")
        assert idx >= 0
        unique_w_positions.add(idx)
    if debug:
        print(f"Unique X positions: {unique_x_positions}: {len(unique_x_positions)}, unique witness: {unique_w_positions}: {len(unique_w_positions)}, total combinations: {len(input_list)}")
    return (len(unique_x_positions))

def sample_positions(input_list: List[str], sample_list: List[int]):
    filtered_list = []
    for comb in input_list:
        sampled_group = [comb[sample] for sample in sample_list]
        if not("W" in sampled_group and "X" not in sampled_group):
            filtered_list.append(comb)
    
    return filtered_list

def calculate_atoms(N: int, sample_history: List[List[int]]) -> List[List[int]]:
    number_of_interviews = len(sample_history)

    # calculate the atoms of samples given it's history
    number_of_atoms = 2**(number_of_interviews)

    # how many values are there for each atom
    atom_list = [0 for _ in range(number_of_atoms)]
    atom_groups = [ [] for _ in range(number_of_atoms)]
    for atom_number in range(number_of_atoms):
        # atoms index corresponds to which samples are off or on
        # for example, i = 0 means selections that fall into no sample
        temp_array = [False for _ in range(number_of_interviews)]
        for interview_number in range(number_of_interviews):
            temp_array[interview_number] = bool(atom_number & (1 << interview_number))
        
        for person in range(N):
            # in atom only if temp_array matches
            is_in_atom = True
            for interview_number, interview in enumerate(sample_history):
                if (person in interview) != temp_array[interview_number]:
                    is_in_atom = False
                    break
                    # skip this person for this atom
            if is_in_atom:
                atom_list[atom_number] += 1
                atom_groups[atom_number].append(person)
        print(f"{temp_array}: {atom_list[atom_number]}: {atom_groups[atom_number]}")
    # return atom_list
    return atom_groups

print(f"Total sample space: {(2**N)**4}")

def debug_print_history(interview_history):
    filtered_list = all_combs
    for interview in interview_history:
        filtered_list = sample_positions(filtered_list, interview)

    interview_lengths = [len(t) for t in interview_history]
    print(f"interviews: {interview_history}: length of each is: {interview_lengths}")
    debug_length(filtered_list, debug=True)
    calculate_atoms(N, interview_history)
    pass

def example_1():
    winners = 0
    min_left = N
    number_of_interviews = 3
    # lets just iterate through all subsets
    # combine power sets to make the total interview space
    for interview_history in itertools.combinations_with_replacement(powerset(range(N)), number_of_interviews):
        filtered_list = all_combs
        for interview in interview_history:
            filtered_list = sample_positions(filtered_list, interview)

        new_length = debug_length(filtered_list)
        if (new_length <= 1):
        # if (len(filtered_list_3) <= 1):
            # interview_str = ",".join(interview_history)
            debug_print_history(interview_history)
            winners += 1
            return

        if new_length < min_left:
            min_left = new_length
            best_set = interview_history

    debug_print_history(best_set)
        
    print(winners)
        
    print(min_left)

example_1()

# first sample the first group
# sample_history = []

# sample_group_0 = [i for i in range(3)]

# sample_history.append(sample_group_0)

# # get all the possible other samples
# s0 = len(sample_group_0)

# #whatever is left
# sC = N - len(s0)

