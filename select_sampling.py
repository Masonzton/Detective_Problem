"""specify sampling by list of numbers. Also calculate atoms"""

from typing import List
import math


def generate_all_combs(n: int) -> List[str]:
    all_combs: List[str] = []

    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            entry = ["O" for i in range(n)]
            entry[i] = "X"
            entry[j] = "W"

            all_combs.append("".join(entry))

    return all_combs


def debug_length(input_list: List[str]):
    unique_x_positions = set()
    unique_w_positions = set()
    for comb in input_list:
        idx = comb.find("X")
        assert idx >= 0
        unique_x_positions.add(idx)
        idx = comb.find("W")
        assert idx >= 0
        unique_w_positions.add(idx)
    print(
        f"Unique X positions: {unique_x_positions}: {len(unique_x_positions)}, unique witness: {unique_w_positions}: {len(unique_w_positions)}, total combinations: {len(input_list)}"
    )


def sample_positions(input_list: List[str], sample_list: List[int]):
    filtered_list = []
    for comb in input_list:
        sampled_group = [comb[sample] for sample in sample_list]
        if not ("W" in sampled_group and "X" not in sampled_group):
            filtered_list.append(comb)

    return filtered_list


def calculate_atoms(N: int, sample_history: List[List[int]]) -> List[List[int]]:
    number_of_interviews = len(sample_history)

    # calculate the atoms of samples given it's history
    number_of_atoms = 2 ** (number_of_interviews)

    # how many values are there for each atom
    atom_list = [0 for _ in range(number_of_atoms)]
    atom_groups = [[] for _ in range(number_of_atoms)]
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


# debug_length(all_combs)


def atoms_to_interview(atoms: List[List[int]]) -> List[List[int]]:
    number_of_atoms = len(atoms)
    # length of the list should be a power of two
    assert (number_of_atoms & (number_of_atoms - 1) == 0) and number_of_atoms != 0
    number_of_interviews = int(math.log2(number_of_atoms))
    sample_list = []
    for interview_number in range(number_of_interviews):
        current_interview = []
        for atom_number in range(number_of_atoms):
            if atom_number & (1 << interview_number):
                current_interview.extend(atoms[atom_number])
        sample_list.append(current_interview)

    return sample_list


def construct_atom_list(number_of_people, number_of_interviews):
    number_of_atoms = 2**number_of_interviews
    ideal_split = int(number_of_interviews / 2)
    atom_list = [[] for _ in range(number_of_atoms)]
    current_person = 0
    for atom_number in range(number_of_atoms):
        if atom_number.bit_count() == ideal_split:
            atom_list[atom_number] = [current_person]
            current_person += 1
            if current_person >= number_of_people:
                # all people are assigned yay :)
                break

    # all people should have been assigned
    assert current_person >= number_of_people
    return atom_list


def experiment_1_manual():
    SAMPLE_HISTORY = [
        [0, 1, 2],
        [0, 3, 4],
        [1, 3, 5],
        [2, 4, 5],
    ]
    N = 6
    filtered_list = generate_all_combs(6)
    for sample in SAMPLE_HISTORY:
        filtered_list = sample_positions(filtered_list, sample)
        debug_length(filtered_list)

    # for entry in filtered_list:
    #     print(entry)
    atom_list = calculate_atoms(N, SAMPLE_HISTORY)
    sample_list = atoms_to_interview(atom_list)
    for sample in sample_list:
        print(sample)

    return atom_list


def experiment_2_calculated():
    N = 10
    lower_bound = int(math.log2(N))
    # this is a guess?
    upper_bound = lower_bound + 10
    for guess in range(lower_bound, upper_bound + 1):
        if math.comb(guess, int(guess / 2)) >= N:
            print(f"Number of samples is {guess}")
            break
    else:
        # guess not found
        assert False
    atom_list = construct_atom_list(N, guess)
    interviews = atoms_to_interview(atom_list)
    for interview in interviews:
        print(interview)
    # this next step is really slow, but I don't care
    print("generating validation data")
    filtered_list = generate_all_combs(N)
    for sample in interviews:
        filtered_list = sample_positions(filtered_list, sample)
        debug_length(filtered_list)

    pass


# experiment_1_manual()
experiment_2_calculated()
