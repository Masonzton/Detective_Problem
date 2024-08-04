"""File to iterate through all atom combinations"""

from typing import List, Tuple
from itertools import combinations


# list is of the form, murderer witness
def generate_all_combs(n: int) -> List[Tuple[int, int]]:
    return [(i, j) for i in range(n) for j in range(n) if i != j]


def unique_murder_positions(input_list: Tuple[int, int]):
    unique_x_positions = set()
    for comb in input_list:
        unique_x_positions.add(comb[0])
    return len(unique_x_positions)


def calculate_atoms_from_history(
    N: int, sample_history: List[List[int]]
) -> List[List[int]]:
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


def atom_selection_to_interview(
    atom_numbers: List[int], number_of_interviews: int
) -> List[List[int]]:
    sample_list = []
    for interview_number in range(number_of_interviews):
        current_interview = []
        for person, atom_number in enumerate(atom_numbers):
            if atom_number & (1 << interview_number):
                current_interview.append(person)
        sample_list.append(current_interview)

    return sample_list


def all_atoms_generator(number_of_people, number_of_interviews):
    number_of_atoms = 2**number_of_interviews
    for atom_list in combinations(range(number_of_atoms), number_of_people):
        yield atom_list


def filter_with_sample(input_list: List[Tuple[int, int]], sampling: List[int]):
    """Filter the possibility space given an interview"""
    new_list = []
    for comb in input_list:
        witness_position = comb[1]
        murder_position = comb[0]
        if (witness_position not in sampling) or (murder_position in sampling):
            new_list.append(comb)

    return new_list


def pretty_print_atoms(atom_numbers: List[int], number_of_interviews: int):
    for atom_number in atom_numbers:
        temp_array = [False for _ in range(number_of_interviews)]
        for interview_number in range(number_of_interviews):
            temp_array[interview_number] = bool(atom_number & (1 << interview_number))

        print(f"{temp_array}")


def example_1():
    number_of_people = 8
    number_of_interviews = 4
    all_combs = generate_all_combs(number_of_people)

    iteration_number = 0

    min_left = number_of_people
    for atom_set in all_atoms_generator(
        number_of_people=number_of_people, number_of_interviews=number_of_interviews
    ):
        # print(atom_set)
        sample_history = atom_selection_to_interview(
            atom_numbers=atom_set, number_of_interviews=number_of_interviews
        )
        # print(sample_history)
        filtered_list = all_combs
        for sampling in sample_history:
            filtered_list = filter_with_sample(filtered_list, sampling)
            # print(filtered_list)

        possibilities = unique_murder_positions(filtered_list)
        # print(possibilities)

        # if possibilities <= 1:
        if len(filtered_list) <= 1:
            print("!!!!!!Winner combo found!!!!!!!")
            print("Interviews are:")
            for interview in sample_history:
                print(interview)
            print(f"Atoms are: {atom_set}")
            pretty_print_atoms(atom_set, number_of_interviews)
            return

        if possibilities < min_left:
            best_example = sample_history
            best_atoms = atom_set
            min_left = possibilities

        iteration_number += 1
        if (iteration_number % 100_000) == 0:
            print(iteration_number)

    print("*******No solution found. Best example is")
    for sample in best_example:
        print(sample)
    print(f"Atoms are: {atom_set}")
    pretty_print_atoms(best_atoms, number_of_interviews)


example_1()
