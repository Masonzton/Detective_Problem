"""Helpers for running experiments"""

from typing import List, Tuple
from itertools import chain, combinations


def generate_all_combs(n: int) -> List[Tuple[int, int]]:
    """Generate the possibility space of possible murderer witness combos.
    List of tuples with Murderer in position 0, witness in position 1"""
    return [(i, j) for i in range(n) for j in range(n) if i != j]


def filter_with_sample(
    input_list: List[Tuple[int, int]], sampling: List[int]
) -> List[Tuple[int, int]]:
    """Filter the possibility space given a list of interview"""
    new_list = []
    for comb in input_list:
        witness_position = comb[1]
        murder_position = comb[0]
        if (witness_position not in sampling) or (murder_position in sampling):
            new_list.append(comb)

    return new_list


def pretty_print_atoms(atom_numbers: List[int], number_of_interviews: int):
    """Print the atom numbers in a binary format"""
    for atom_number in atom_numbers:
        temp_array = [False for _ in range(number_of_interviews)]
        for interview_number in range(number_of_interviews):
            temp_array[interview_number] = bool(atom_number & (1 << interview_number))

        print(f"{atom_number}: {temp_array}")


def powerset(iterable) -> chain[List[int]]:
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    # want to exclude interviews with whole set and empty set
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)))


def unique_murder_positions(input_list: Tuple[int, int]):
    """return a list of how many unique positions there are for the murderer"""
    unique_x_positions = set()
    for comb in input_list:
        unique_x_positions.add(comb[0])
    return unique_x_positions


def get_murderous_atoms(atoms: List[int]) -> List[int]:
    """Given a set of atoms determine exactly which atoms the murderer could be under.
    Under the assumption that the witness does not speak with this interview combo"""
    # an atom can be murderous if and only if there exists a witness atom such that
    # the murderous atom completely covers it
    murderous_atoms = []
    for murder_atom in atoms:
        for witness_atom in atoms:
            if murder_atom == witness_atom:
                continue
            if witness_atom & ~murder_atom == 0:
                murderous_atoms.append(murder_atom)
                break

    return murderous_atoms


def get_witness_atoms(atoms: List[int]):
    """Given a set of atoms determine exactly which atoms the witness could be under.
    Under the assumption that the witness does not speak with this interview combo"""
    # see get murderous atoms for inverse explanation
    witness_atoms = []
    for witness_atom in atoms:
        for murder_atom in atoms:
            if murder_atom == witness_atom:
                continue
            if witness_atom & ~murder_atom == 0:
                witness_atoms.append(witness_atom)
                break

    return witness_atoms
