from nfa_construct import State, NFA

def NFA_construct(postfix):
    st = []

    for ch in postfix:
        if ch.isalnum():
            start = State()
            accept = State()
            start.transitions[ch] = [accept]
            st.append(NFA(start, accept))

        elif ch == '.':
            nfa2 = st.pop()
            nfa1 = st.pop()
            nfa1.accept.epsilon.append(nfa2.start)
            st.append(NFA(nfa1.start, nfa2.accept))

        elif ch == '|':
            nfa2 = st.pop()
            nfa1 = st.pop()
            start = State()
            accept = State()
            start.epsilon.extend([nfa1.start, nfa2.start])
            nfa1.accept.epsilon.append(accept)
            nfa2.accept.epsilon.append(accept)
            st.append(NFA(start, accept))

        elif ch == '*':
            nfa = st.pop()
            start = State()
            accept = State()
            start.epsilon.extend([nfa.start, accept])
            nfa.accept.epsilon.extend([nfa.start, accept])
            st.append(NFA(start, accept))

        elif ch == '+':
            nfa = st.pop()
            start = State()
            accept = State()
            start.epsilon.append(nfa.start)
            nfa.accept.epsilon.extend([nfa.start, accept])
            st.append(NFA(start, accept))

        elif ch == '?':
            nfa = st.pop()
            start = State()
            accept = State()
            start.epsilon.extend([nfa.start, accept])
            nfa.accept.epsilon.append(accept)
            st.append(NFA(start, accept))

        else:
            raise ValueError(f"Unknown symbol {ch!r}")

    if len(st) != 1:
        raise ValueError("Malformed regex (stack ended with >1 NFAs)")

    return st[0]