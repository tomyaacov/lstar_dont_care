from itertools import product
import csv


def passed(w):
    if "L2" in w and "A" in w and "C" in w:
        if w.index("L2") < w.index("A") < w.index("C"):
            return False
    return True


total_traces = set()
for n in range(1, 5):
    base = ["L1"] + ["A"] * n + ["C"]
    for i in range(-1, len(base)):
        if i == -1:
            w = base  # without L2
        else:
            w = base[:i] + ["L2"] + base[i:]
        print(w)
        for j in range(len(w) + 1):
            total_traces.add((tuple(w[:j]), passed(w[:j])))
total_traces = sorted(list(total_traces))

with open("data/system_dfa.csv", "w") as f:
    write = csv.writer(f)
    write.writerows([list(x) + [y] for x, y in total_traces])

alphabet = ["L1", "L2", "A", "C"]
spec_data = [(x, True) for x, _ in total_traces]
for i in range(1, 7):
    for w in product(alphabet, repeat=i):
        if not ((w, True) in total_traces or (w, False) in total_traces):
            spec_data.append((w, False))

with open("data/spec_dfa.csv", "w") as f:
    write = csv.writer(f)
    write.writerows([list(x) + [y] for x, y in spec_data])
