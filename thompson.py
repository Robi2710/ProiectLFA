from nfa import State, NFA

def NFA_construct(postfix):
    st = []

    for chr in postfix:
        if chr.isalnum():
            start = State()
            accept = State()
            start.transitions[chr] = [accept]
            st.append(NFA(start,accept))

        elif chr == '.':
            nfa2 = st.pop()
            nfa1 = st.pop()
            nfa1.accept.transitions[None] = [nfa2.start]
            st.append(NFA(nfa1.start,nfa2.accept))

        elif chr == '|':
            nfa2 = st.pop()
            nfa1 = st.pop()
            start = State()
            accept = State()
            start.transitions[None] = [nfa1.start, nfa2.start]
            nfa1.accept.transitions[None] = [accept]
            nfa2.accept.transitions[None] = [accept]
            st.append(NFA(start,accept))

        elif chr == '*':
            nfa = st.pop()
            start = State()
            accept = State()
            start.transitions[None] = [nfa.start, accept]
            nfa.accept.transitions[None] = [nfa.start, accept]
            st.append(NFA(start, accept))

        elif chr == '+':
            nfa = st.pop()
            start = State()
            accept = State()
            start.transitions[None] = [nfa.start]
            nfa.accept.transitions[None] = [nfa.start, accept]
            st.append(NFA(start, accept))

        elif chr == '?':
            nfa = st.pop()
            start = State()
            accept = State()
            start.transitions[None] = [nfa.start, accept]
            nfa.accept.transitions[None] = [nfa.start]
            st.append(NFA(start, accept))

        else:
            raise ValueError("Unknown character '%s'" % chr)
    if len(st) !=1 :
        raise ValueError("error")

    return st[0]
