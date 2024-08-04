"""Goal is to classify potential sample space. In other word,
Count the number of possible interview strategies"""

from itertools import combinations, permutations
from helpers import get_murderous_atoms, pretty_print_atoms, get_witness_atoms


def permute_bits(number, permutation):
    # Initialize the result
    result = 0

    # Loop over the permutation and set the bits in the result
    for i, perm_index in enumerate(permutation):
        # Extract the bit from the original number
        bit = number & (1 << perm_index)

        # Set the corresponding bit in the result
        if bit:
            result = result | (1 << i)

    return result


def main():
    number_of_people = 6
    number_of_interviews = 4
    all_atoms = list(range(2**number_of_interviews))
    all_subsets_of_atoms = list(combinations(all_atoms, number_of_people))

    all_permutations = list(permutations(range(number_of_interviews)))

    print(f"all Subsets of atoms: {len(all_subsets_of_atoms)}")

    # filter this list of atoms down based on permutation symmetries
    # do this by iterating over each subset of atoms and removing all atoms in the set that
    # are equivalent under symmetry
    index_in_all_subsets = 0
    while index_in_all_subsets < len(all_subsets_of_atoms):
        current_subset = all_subsets_of_atoms[index_in_all_subsets]
        for perm in all_permutations:
            # modify subset according to permutation
            transformed_subset = tuple(
                [permute_bits(atom, perm) for atom in current_subset]
            )
            if (
                transformed_subset != current_subset
                and transformed_subset in all_subsets_of_atoms
            ):
                all_subsets_of_atoms.remove(transformed_subset)

        index_in_all_subsets += 1
        if index_in_all_subsets % 1000 == 0:
            print(
                f"current index in subset: {index_in_all_subsets}, atoms left: {len(all_subsets_of_atoms)}"
            )

    print(f"all unique subsets of atoms size == {len(all_subsets_of_atoms)}")

    # try out each atom pair for a win
    winning_combos = []
    for atom_subset in all_subsets_of_atoms:
        murder_atoms = get_murderous_atoms(atom_subset)
        if len(murder_atoms) <= 1:
            winning_combos.append(atom_subset)

    print(
        f"all winning subsets of atoms: size {len(winning_combos)}.\n{winning_combos}"
    )
    print("")
    for index, atom_set in enumerate(winning_combos):
        print(f"subset: {index}: {atom_set}")
        pretty_print_atoms(atom_set, number_of_interviews)
        print(f"potential murder atoms: {get_murderous_atoms(atom_set)}")
        print(f"potential witness atoms: {get_witness_atoms(atom_set)}")
        print("\n")

    # Note. Only one combination has 0 murderers and 0 witnesses left. Meaning only
    # looking at n = 6 people with k = 4 interviews
    # 31 possible unique win combos for n=6,k=4

    # one combination is able to eliminate the entire possibility space. This is the normal combination
    # where each individual is given a unique set of interviews to partake in

    # the rest are is with 5 out of 6 people partaking in a unique set of 2 interviews (aka standard strategy)
    # but then one atom/person is partaking in more than 2 interviews, meaning that it is the murderer

    # also this program runs out of memory for 20 people 6 interviews
    # and is too slow at the atom filtering step for 10 people lol


if __name__ == "__main__":
    assert permute_bits(5, [1, 0, 2]) == 6
    main()
