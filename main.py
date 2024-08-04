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

for comb in all_combs:
    print(comb)

print("")


def first_sample(input_list, sample_number):
    filtered_list = []
    for comb in input_list:
        sampled_side = comb[0:sample_number]
        un_sampled_side = comb[sample_number:]
        split_comb = f"{sampled_side}|{un_sampled_side}"
        if not ("W" in sampled_side and "X" not in sampled_side):
            filtered_list.append(split_comb)

    return filtered_list


for i in range(N + 1):
    filtered_list = first_sample(all_combs, i)
    print(f"{i}: {len(filtered_list)}")
    pass

print("")
filtered_list = first_sample(all_combs, 3)
for comb in filtered_list:
    print(comb)
