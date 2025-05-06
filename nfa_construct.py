class State:
    def __init__(self):
        self.transitions = {}
        self.epsilon = []

class NFA:
    def __init__(self, start, accept):
        self.start = start
        self.accept = accept

def thompson_construction(postfix):
    stack = []

    for char in postfix:
        if char.isalnum():
            start = State()
            accept = State()
            start.transitions[char] = [accept]
            stack.append(NFA(start, accept))

        elif char == '.':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            nfa1.accept.epsilon.append(nfa2.start)
            stack.append(NFA(nfa1.start, nfa2.accept))

        elif char == '|':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            start = State()
            accept = State()
            start.epsilon.extend([nfa1.start, nfa2.start])
            nfa1.accept.epsilon.append(accept)
            nfa2.accept.epsilon.append(accept)
            stack.append(NFA(start, accept))

        elif char == '*':
            nfa = stack.pop()
            start = State()
            accept = State()
            start.epsilon.extend([nfa.start, accept])
            nfa.accept.epsilon.extend([nfa.start, accept])
            stack.append(NFA(start, accept))
        elif char == '+':
            nfa = stack.pop()
            start = State()
            accept = State()
            start.epsilon.append(nfa.start)
            nfa.accept.epsilon.extend([nfa.start, accept])
            stack.append(NFA(start, accept))
        elif char == '?':
            nfa = stack.pop()
            start = State()
            accept = State()
            start.epsilon.extend([nfa.start, accept])
            nfa.accept.epsilon.append(accept)
            stack.append(NFA(start, accept))

    return stack[-1]

