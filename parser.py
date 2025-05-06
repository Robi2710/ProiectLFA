from shunting_yard import shunting_yard

def concatenation(regex):
    rez = []
    op = set('|*+?')
    prev = None

    for ch in regex:
        if prev:
            # whenever prev and ch should be concatenated,
            # inject a '.' operator instead of repeating ch
            if (prev not in op and prev != '(') and (ch not in op and ch != ')'):
                rez.append('.')      # <— insert explicit concat
        rez.append(ch)
        prev = ch

    return ''.join(rez)

def parse(regex):
    regexconcat = concatenation(regex)
    return shunting_yard(regexconcat)