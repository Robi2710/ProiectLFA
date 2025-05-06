from shunting_yard import shunting_yard

def concatenation(regex):
    rez = []
    op = set('|*+?')
    prev = None

    for ch in regex:
        if prev:
            if (
                ((prev not in op and prev != '(')
                 or (prev in '*+?')
                 or (prev == ')'))
                and (ch not in op and ch != ')')
            ):
                rez.append('.')
        rez.append(ch)
        prev = ch

    return ''.join(rez)
def parse(regex):
    regexconcat = concatenation(regex)
    return shunting_yard(regexconcat)