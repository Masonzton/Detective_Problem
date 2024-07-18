"""Sample groups by partitions"""
from typing import List
from itertools import chain, combinations

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

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

print(f"Total sample space: {(2**N)**4}")

def example_1():
    filtered_list = all_combs
    winners = 0
    # lets just iterate through all subsets
    min_left = N
    for subset_0 in powerset(range(N)):
        filtered_list = all_combs
        if len(subset_0) == 0 or len(subset_0) == N:
            continue
        filtered_list_0 = sample_positions(filtered_list, subset_0)
        # min_left = min(debug_length(filtered_list), min_left)
        for subset_1 in powerset(range(N)):
            if len(subset_1) == 0 or len(subset_1) == N:
                continue
            filtered_list_1 = sample_positions(filtered_list_0, subset_1)
            # min_left = min(debug_length(filtered_list), min_left)
            for subset_2 in powerset(range(N)):
                if len(subset_2) == 0 or len(subset_2) == N:
                    continue
                filtered_list_2 = sample_positions(filtered_list_1, subset_2)
                new_length = debug_length(filtered_list_2)
                # if (new_length <= 1):
                #     print(f"{subset_0}, {subset_1}, {subset_2}")
                #     debug_length(filtered_list_2, debug=True)
                min_left = min(new_length, min_left)
                for subset_3 in powerset(range(N)):
                    if len(subset_3) == 0 or len(subset_3) == N:
                        continue
                    filtered_list_3 = sample_positions(filtered_list_2, subset_3)
                    new_length = debug_length(filtered_list_3)
                    # if (new_length <= 1):
                    if (len(filtered_list_3) <= 1):
                        print(f"{len(subset_0)}:{subset_0}, {len(subset_1)}: {subset_1}, {len(subset_2)}: {subset_2}, {len(subset_3)}: {subset_3}")
                        debug_length(filtered_list_3, debug=True)
                        winners += 1
                        return
                    min_left = min(new_length, min_left)
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

