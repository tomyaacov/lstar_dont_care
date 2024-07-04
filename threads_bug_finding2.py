x, y = 5, 25
def T1():
    global x, y

    for _ in range(5):
        yield "x = x - 1"
        x = x - 1
        #print(x)

        yield "y = y + 1"
        y = y + 1
        #print(x)

def T2():
    global x, y
    yield "if x == 2:"
    #print("if x is " + str(x))
    if x == 2:
        yield "x = 10"
        x = 5
    else:
        yield "x=1*x"
        x = 1 * x  # changed from 2 to 1
    yield "x = x / 1"
    x = x / 1  # changed from 2 to 1





def program():
    global x, y
    x, y = 5, 25
    threads = [T1(), T2()]
    finished = [False] * len(threads)
    for t in threads:
        next(t)
    i = yield False
    while True:
        if "T1" in i:
            try:
                next(threads[0])
            except StopIteration:
                finished[0] = True
        elif "T2" in i:
            try:
                next(threads[1])
            except StopIteration:
                finished[1] = True
        if not all(finished):
            i = yield False
        else:
            #print(x + y)
            if x + y != 30:
                while True:
                    yield True
            else:
                while True:
                    yield False


def program_transitions():
    global x, y
    x, y = 5, 25
    threads = [T1(), T2()]
    finished = [False] * len(threads)
    for t in threads:
        next(t)
    i = yield False
    last = None
    while True:
        if i[-1] == last or (last is None and i[-1] == "B"):
            while True:
                yield False
        last = i[-1]
        if "T1B" in i:
            try:
                next(threads[0])
            except StopIteration:
                finished[0] = True
        elif "T2B" in i:
            try:
                next(threads[1])
            except StopIteration:
                finished[1] = True
        if not all(finished):
            i = yield False
        else:
            #print(x + y)
            if x + y != 30:
                while True:
                    yield True
            else:
                while True:
                    yield False



if __name__ == "__main__":
    from generator_based_dfa import GeneratorBasedDFA
    B = GeneratorBasedDFA(program)
    print(B.execute_sequence(B.initial_state, ["T1"] * 4 + ["T2"] + ["T1"] * 0 + ["T2"] + ["T1"] * 0 + ["T2"] + ["T1"] * 6)[-1])
    # print(B.execute_sequence(B.initial_state,["T1"] * 10 + ["T2", "T1", "T2", "T2"] + ["T1"] * 9)[-1])
    # print(B.execute_sequence(B.initial_state,  ["T1"] * 10 + ["T1"] * 10 + ["T2", "T2", "T2"])[-1])
    #print(B.execute_sequence(B.initial_state,  ["T1"] * 10 + ["T1"] * 6 + ["T2", "T2", "T2"] + ["T1"]* 4)[-1])
    # threads = [T1(), T2()]
    # for t in threads:
    #     print(next(t))
    #
    # word = [1] * 10 + [2, 1, 2, 2, 2, 2, 2, 2] + [1] * 30
    # word = [1] * 10 + [2, 1, 2, 2] + [1] * 9
    #
    # finished = [False] * len(threads)
    #
    # for i in word:
    #     try:
    #         print(next(threads[i - 1]))
    #     except StopIteration:
    #         finished[i - 1] = True
    #
    # if not all(finished):
    #     print("Threads are still running")
    # else:
    #     assert x + y == 30
    #     print("Run was OK")


