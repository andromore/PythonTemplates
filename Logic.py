"""Логика"""

def con(*a):
    b = True
    for i in a:
        if not i:
            b = False
    return b


def inv(a):
    return not a


def dis(*a):
    b = False
    for i in a:
        if i:
            b = True
    return b


def imp(a, b):
    if a and not b:
        return True
    else:
        return False


def eqv(a, b):
    if (a and b) or (not a and not b):
        return True
    else:
        return False


def exc(a, b):
    if (a and not b) or (b and not a):
        return True
    else:
        return False


def logic(a):
    return eval(a)


def trass_table(n):
    a = []

    def command(n, *b):
        for i in [False, True]:
            if n >= 1:
                command(n - 1, *b, i)
            else:
                if list(b) not in a:
                    a.append(list(b))
    command(n)
    return a


def checking(a):
    b = [None, None, None, None, None, None]
    b[0] = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    b[1] = ['con', 'dis', 'inv', 'eqv', 'exc', 'imp']
    b[2] = ['+', '-', '*', '/', '//', '**', '%']
    b[3] = ['==', '!=', '<', '>', '<=', '>=']
    b[4] = [',', '.', '(', ')', ' ']
    b[5] = ['True', 'False']

    def command(a, b):
        for i in b:
            if i in a:
                a = a.replace(i, '')
        return a
    a = command(a, b[1])
    a = command(a, b[2])
    a = command(a, b[3])
    a = command(a, b[4])
    a = command(a, b[5])
    c = []
    for i in b[0]:
        if i in a:
            a = a.replace(i, '')
            c.append(i)
    return a, c


def logic_table(a):
    b, c = checking(a)
    if b != '':
        raise Exception(b)
    d = len(c)
    d = trass_table(d)
    e = []
    for i in d:
        f = dict()
        for j in range(0, len(i)):
            f[c[j]] = str(i[j])
        e.append(f)
    g = []
    for i in e:
        f = a
        for j in i:
            f = f.replace(j, i[j])
        g.append(f)
    for i in range(0, len(e)):
        e[i]['Function'] = logic(g[i])
    return e


def logic_function(a):
    b, c = checking(a)
    b = len(c)
    if b >= 1:
        return b, logic_table(a)
    else:
        return b, logic(a)
