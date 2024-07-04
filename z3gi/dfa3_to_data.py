

def get_table_data(dfa3, table):
    for s in dfa3.states:
        s.reach_reject = False
        s.reach_accept = False
    before = 0
    after = 0
    for s in dfa3.states:
        if s.output == "-":
            s.reach_reject = True
            after += 1
    while after != before:
        before = after
        for s in dfa3.states:
            for a, new_s in s.transitions.items():
                if new_s.reach_reject and not s.reach_reject:
                    after += 1
                    s.reach_reject = True
    before = 0
    after = 0
    for s in dfa3.states:
        if s.output == "+":
            s.reach_accept = True
            after += 1
    while after != before:
        before = after
        for s in dfa3.states:
            for a, new_s in s.transitions.items():
                if new_s.reach_accept and not s.reach_accept:
                    after += 1
                    s.reach_accept = True
    data = set()
    for prefix in table._get_row_representatives():
        for suffix in table.E:
            word = prefix + suffix
            dfa3.reset_to_initial()
            for c in word:
                dfa3.step(c)
            s = dfa3.current_state
            if len(word) > 0:
                result = dfa3.execute_sequence(dfa3.initial_state, word)
                if result[-1] != "?":
                    data.add((word, result[-1] == "+"))
                else:
                    if s.reach_accept and not s.reach_reject:
                        data.add((word, True))
                    elif s.reach_reject and not s.reach_accept:
                        data.add((word, False))
    return data


def get_dfs_data(dfa3):
    for s in dfa3.states:
        s.reach_reject = False
        s.reach_accept = False
    before = 0
    after = 0
    for s in dfa3.states:
        if s.output == "-":
            s.reach_reject = True
            after += 1
    while after != before:
        before = after
        for s in dfa3.states:
            for a, new_s in s.transitions.items():
                if new_s.reach_reject and not s.reach_reject:
                    after += 1
                    s.reach_reject = True
    before = 0
    after = 0
    for s in dfa3.states:
        if s.output == "+":
            s.reach_accept = True
            after += 1
    while after != before:
        before = after
        for s in dfa3.states:
            for a, new_s in s.transitions.items():
                if new_s.reach_accept and not s.reach_accept:
                    after += 1
                    s.reach_accept = True
    for s1 in dfa3.states:
        s1.shortest_words_from = {}
        for s2 in dfa3.states:
            s1.shortest_words_from[s2] = []
        s1.shortest_words_from[s1].append(tuple())

    for s in dfa3.states:
        visited = set()
        stack = [s]
        while len(stack) > 0:
            curr = stack.pop(0)
            if curr in visited:
                continue
            visited.add(curr)
            for a, new_s in curr.transitions.items():
                stack.append(new_s)
                if len(new_s.shortest_words_from[s]) == 0 or len(curr.shortest_words_from[s][0]) + 1 == len(new_s.shortest_words_from[s][0]):
                    for w in curr.shortest_words_from[s]:
                        new_s.shortest_words_from[s].append(w + (a,))

    data = set()
    init = dfa3.initial_state
    for s in dfa3.states:
        if s.output != "?":
            for w in s.shortest_words_from[init]:
                data.add((w, s.output == "+"))
        elif s.reach_accept and not s.reach_reject:
            for w in s.shortest_words_from[init]:
                data.add((w, True))
        elif s.reach_reject and not s.reach_accept:
            for w in s.shortest_words_from[init]:
                data.add((w, False))

    for s1 in dfa3.states:
        for s2 in dfa3.states:
            for w1 in s1.shortest_words_from[init]:
                for w2 in s2.shortest_words_from[s1]:
                    if s2.output != "?":
                        data.add((w1 + w2, s2.output == "+"))
                    elif s2.reach_accept and not s2.reach_reject:
                        data.add((w1 + w2, True))
                    elif s2.reach_reject and not s2.reach_accept:
                        data.add((w1 + w2, False))

    return data




