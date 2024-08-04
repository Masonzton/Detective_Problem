"""Calculate the required interviews for a given number of people"""

from helpers import generate_all_combs, filter_with_sample, unique_murder_positions
from typing import List
import math


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


def calculate_interviews_needed(number_of_people: int) -> int:
    """Calculate the number of interviews required to determine the suspect"""
    N = number_of_people
    lower_bound = int(math.log2(N))
    # this is a guess for how many you will need to try
    # could technically just have no upper bound?
    upper_bound = lower_bound + 10
    for guess in range(lower_bound, upper_bound + 1):
        if math.comb(guess, int(guess / 2)) >= N:
            print(f"Number of samples is {guess}")
            break
    else:
        raise ValueError(
            f"Could not compute interviews needed for {number_of_people}, try increasing upper bound of search"
        )

    return guess


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


def main():
    number_of_people = 20
    number_of_interviews = calculate_interviews_needed(number_of_people)
    # calculate the atoms that we will use as interviews
    # An atom is a representation of exactly which interviews a slot is assigned to.
    # for example, with k = 3 interviews ABC. There are 2^3 = 8 atoms. Namely
    # not in A and not in B and not in C -> 000
    # not in A and not in B and in C -> 001
    # ~A &&  B && ~C -> 010
    # ~A &&  B &&  C -> 011
    # A  && ~B && ~C -> 100
    # and so on with each number 0 to 2^k-1 being assigned a unique combinations of interviews
    # that it partakes in
    atom_list = construct_atom_list(number_of_people, number_of_interviews)

    # turn that atom list into the actual interviews
    interview_list = atoms_to_interview(atom_list)
    print(f"interviews to conduct are: {interview_list}")

    # validate the answer. This could take a bit to validate
    print("generating validation set")
    possibility_space = generate_all_combs(number_of_people)

    filtered_space = possibility_space
    for interview in interview_list:
        filtered_space = filter_with_sample(filtered_space, interview)

    print(
        f"""possibility space left after sampling is
        size={len(filtered_space)}.
        entries={filtered_space}"""
    )
    print(f"unique murderer positions is {unique_murder_positions(filtered_space)}")


if __name__ == "__main__":
    main()
