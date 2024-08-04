from itertools import permutations

# 2. burnside lemma is

# sum (fix(g)) for g in G  / size(G) = S/G

# how many members of G
# 5! = 120
# how many of those orbits are fixed?

# for each item

k = 5
N = 20

number = 0
for permutation in permutations([i for i in range(k)], k):
    number += 1

print(number)
