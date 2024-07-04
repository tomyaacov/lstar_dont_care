from staticfg import CFGBuilder
s = """
def T1():
    x, y = 10, 20
    for _ in range(10):
        x = x - 1
        y = y + 1
"""
cfg = CFGBuilder().build_from_src('fib', s)
a = cfg._build_visual().__str__()
with open("a.dot", "w") as f: f.write(a)