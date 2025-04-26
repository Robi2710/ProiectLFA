def shunting_yard(regex):
    precedence = {
        '|' : 1,
        '.' : 2,
        '*' : 3,
        '+' : 3,
        '?' : 3,
    }
    final = []
    st = []

    for chr in regex:
        if chr.isalnum():
            final.append(chr)
        elif chr == '(':
            st.append(chr)
        elif chr == ')':
            while st and st[-1] != '(':
                final.append(st.pop())
            st.pop()
        else:
            while st and st[-1] != '(' and precedence.get(st[-1], 0) >= precedence.get(chr, 0):
                final.append(st.pop())
            st.append(chr)
    while st:
        final.append(st.pop())

    return ''.join(final)
