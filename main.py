import json
from parser import parse
from nfa_construct import thompson_construction
from nfa_to_dfa import nfa_to_dfa
from dfa import simulate_dfa

def load_tests(json_path: str):
    with open(json_path, "r") as f:
        return json.load(f)

def build_dfa_from_regex(regex: str):
    postfix = parse(regex)
    nfa = thompson_construction(postfix)
    dfa = nfa_to_dfa(nfa)
    return dfa

def run_tests_on_dfa(dfa: dict, test_strings: list):
    results = []
    for t in test_strings:
        inp = t["input"]
        exp = t["expected"]
        got = simulate_dfa(dfa, inp)
        results.append((inp, exp, got))
    return results

def main():
    all_cases = load_tests("LFA-Assignment2_Regex_DFA_v2.json")

    for case in all_cases:
        name   = case["name"]
        regex  = case["regex"]
        tests  = case["test_strings"]

        print(f"\n=== {name}: /{regex}/ ===")
        dfa = build_dfa_from_regex(regex)
        for inp, exp, got in run_tests_on_dfa(dfa, tests):
            mark = "✔" if got == exp else "✘"
            print(f" {mark}  input={inp!r:6} expected={exp} got={got}")

if __name__ == "__main__":
    main()
