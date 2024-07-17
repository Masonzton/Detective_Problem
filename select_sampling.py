"""specify sampling by list of numbers"""

from typing import List
# just start with n = 5
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
    print(f"Unique X positions: {unique_x_positions}: {len(unique_x_positions)}, unique witness: {unique_w_positions}: {len(unique_w_positions)}, total combinations: {len(input_list)}")

def sample_positions(input_list: List[str], sample_list: List[int]):
    filtered_list = []
    for comb in input_list:
        sampled_group = [comb[sample] for sample in sample_list]
        if not("W" in sampled_group and "X" not in sampled_group):
            filtered_list.append(comb)
    
    return filtered_list
debug_length(all_combs)

filtered_list = sample_positions(all_combs, [3, 4, 5])
# for comb in filtered_list:
#     print(comb)
debug_length(filtered_list)
# print(len(filtered_list))

filtered_list = sample_positions(filtered_list, [0, 1, 2,])
# for comb in filtered_list:
#     print(comb)
debug_length(filtered_list)

filtered_list = sample_positions(filtered_list, [1, 2, 3, 4])
# for comb in filtered_list:
#     print(comb)
debug_length(filtered_list)

filtered_list = sample_positions(filtered_list, [0, 2, 4, 5])
# for comb in filtered_list:
#     print(comb)
debug_length(filtered_list)

filtered_list = sample_positions(filtered_list, [0, 2, 4, 5])
# for comb in filtered_list:
#     print(comb)
debug_length(filtered_list)