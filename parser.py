from shunting_yard import shunting_yard

def concatenation(regex):

    rez = []
    op = set('|*+?')
    prev = None

    for chr in regex:
        if prev:
            if (prev not in op and prev != '(') and (chr not in op and chr != ')'):
                rez.append(chr)
            if prev in '*+?' and (chr not in op and chr != ')' ):
                rez.append(chr)
            if prev == ')' and (chr not in op and chr != ')'):
                rez.append(chr)
        rez.append(chr)
        prev = chr

    return ''.join(rez)

def parse(regex):
    regexconcat = concatenation(regex)
    postfix = shunting_yard(regexconcat)
    return postfix