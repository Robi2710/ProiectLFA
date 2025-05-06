def epsilon_closure(states):
    stack = list(states)
    closure = set(states)

    while stack:
        state = stack.pop()
        for next_state in state.epsilon:
            if  next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)
    return closure

def move(states, symbol):
    result = set()
    for state in states:
        if symbol in state.transitions:
            result.update(state.transitions[symbol])
    return result

def nfa_to_dfa(nfa):
    from collections import deque

    dfa_states = {}  # map: frozenset(NFA states) -> DFA state id
    dfa_transitions = {}  # (dfa_state_id, symbol) -> dfa_state_id
    dfa_accepting = set()

    state_id = 0
    initial_closure = frozenset(epsilon_closure([nfa.start]))
    dfa_states[initial_closure] = state_id
    unmarked = deque([initial_closure])
    state_id += 1

    symbols = set()

    def collect_symbols(state, seen):
        if state in seen:
            return
        seen.add(state)
        for sym, targets in state.transitions.items():
            symbols.add(sym)
            for t in targets:
                collect_symbols(t, seen)
        for eps in state.epsilon:
            collect_symbols(eps, seen)
    collect_symbols(nfa.start, set())

    while unmarked:
        current = unmarked.popleft()
        current_id = dfa_states[current]

        for symbol in symbols:
            if symbol == '': continue
            next_nfa_states = epsilon_closure(move(current, symbol))
            next_nfa_frozen = frozenset(next_nfa_states)

            if not next_nfa_frozen:
                continue

            if next_nfa_frozen not in dfa_states:
                dfa_states[next_nfa_frozen] = state_id
                unmarked.append(next_nfa_frozen)
                state_id += 1

            dfa_transitions[(current_id, symbol)] = dfa_states[next_nfa_frozen]

    for states_set, id_ in dfa_states.items():
        if nfa.accept in states_set:
            dfa_accepting.add(id_)

    return {
        "start": 0,
        "transitions": dfa_transitions,
        "accepting": dfa_accepting
    }