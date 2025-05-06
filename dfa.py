def read_dfa(filename):
    Sigma = []
    States = []
    F = []
    q0 = []
    transitions = {}

    with open(filename, "r") as file:
        section = None
        for line in file:
            line = line.strip()
            if line.startswith("#") or line == "":
                continue
            if line == "Sigma:":
                section = "sigma"
                continue
            elif line == "States:":
                section = "states"
                continue
            elif line == "Transitions:":
                section = "transitions"
                continue
            elif line == "End":
                section = None
                continue

            if section == "sigma":
                Sigma.append(line)
            elif section == "states":
                parts = line.split(", ")
                state = parts[0]
                States.append(state)
                if len(parts) > 1:
                    if "S" in parts:
                        q0.append(state)
                    if "F" in parts:
                        F.append(state)
            elif section == "transitions":
                src, symbol, dst = line.split(", ")
                transitions[(src, symbol)] = dst

    return Sigma, States, q0, F, transitions

def validate_dfa(Sigma, States, q0, F, transitions):
    if len(q0) != 1:
        return False
    for (src, symbol), dst in transitions.items():
        if src not in States or dst not in States:
            return False
        if symbol not in Sigma:
            return False
    return True

def simulate_dfa(dfa: dict, input_string: str) -> bool:
    """
    Simulate a DFA produced by your nfa_to_dfa converter.
    'dfa' must be a dict with keys:
       - "start":   the start state
       - "transitions": a map (state, symbol) -> next_state
       - "accepting":   a set of accepting states
    """
    curr_state = dfa["start"]
    for symbol in input_string:
        key = (curr_state, symbol)
        if key not in dfa["transitions"]:
            return False
        curr_state = dfa["transitions"][key]
    return curr_state in dfa["accepting"]

if __name__ == "__main__":
    Sigma, States, q0, F, transitions = read_dfa("dfa.txt")
    if not validate_dfa(Sigma, States, q0, F, transitions):
        print("Automat INVALID")
    else:
        string = input("Input string: ")
        if simulate_dfa(Sigma, States, q0, F, transitions, string):
            print("Da")
        else:
            print("NU")