def view(lis,d=0,):
    d += 1
    for i in range(len(lis)):
        j = lis[i]
        if isinstance(j,list):
            print('    '*(d-1)+'[')
            view(j,d=d)
            print('    '*(d-1)+']')
        else:
            print('    '*(d-1)+str(j))
def lspt(lis,it):
    ret = []
    for i in lis:
        if not i in it:
            ret.append(i)
    return ret
def pair(x,chs,depth=0):
    hold = {}
    dep = 0
    pl = 0
    ret = {}
    for i in x:
        if i == chs[0]:
            dep += 1
            hold[dep] = pl
        elif i == chs[1]:
            if dep <= depth:
                ret[hold[dep]] = pl
            dep -= 1
        pl += 1
    return ret
def tokenize(line):
    toks = [['start']]
    flags = []
    specs = {}
    for i in line:
        if i == ' ':
            if toks[-1][0] != 'space':
                toks.append(['space'])
        elif i in '\"':
            if not 'dstr' in flags:
                flags.append('dstr')
                specs['dstr'] = ''
            else:
                toks.append(['str',specs['dstr']])
                del flags[flags.index('dstr')]
                del specs['dstr']
        elif 'dstr' in flags:
            specs['dstr'] += i
        elif i == '(':
            toks.append(['l_b'])
        elif i == ')':
            toks.append(['r_b'])
        elif i.isnumeric() and len(flags) == 0:
            if toks[-1][0] != 'int':
                toks.append(['int',''])
            toks[-1][1] += i
        elif i == '$':
            toks.append(['vars',''])
        else:
            if toks[-1][0] == 'vars':
                toks[-1] = ['var','']
            elif toks[-1][0] == 'var':
                pass
            elif toks[-1][0] != 'name':
                toks.append(['name',''])
            toks[-1][1] += i
    toks.append(['end'])
    return toks
def tokall(code):
    return [tokenize(i) for i in code.split('\n')]
def trea(tokens):
    return [tree(i) for i in tokens]
def tree(tokens):
    par = pair(tokens,[['l_b'],['r_b']],depth=1)
    newt = []
    place = 0
    while place != len(tokens):
        if place in par:
            newt.append(tree(tokens[place+1:par[place]]))
            place = par[place]
        else:
            newt.append(tokens[place])
        place += 1
    return newt
def t2a(tree):
    return [t2ln(i) for i in tree]
def t2ln(tree):
    return t2t(tree[1:-1])
def t2t(tree):
    fnn = None
    nex = True
    perams = []
    for i in tree:
        if i[0] == 'name':
            fnn = i[1]
            nex = False
        elif i[0] == 'space':
            nex = True
        elif nex:
            nex = False
            perams.append(i)
    for i in range(len(perams)):
        if isinstance(perams[i][0],list):
            perams[i] = t2t(perams[i])
    if fnn != None:
        return ['call',fnn,perams]
def runs(synt):
    for i in synt:
        run(i)
def run(i):
    if i[0] == 'call':
        print(i)
code = open('main.ion').read()
tokens = tokall(code)
syntree = trea(tokens)
syntree = t2a(syntree)
runs(syntree)
