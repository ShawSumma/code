#!/usr/bin/env python3
import sys
import lex
def pairo(x,chs,depth=0):
    hold = {}
    dep = 0
    pl = 0
    ret = {}
    for i in x:
        if i == chs[0]:
            dep += 1
            hold[dep] = pl
        elif i == chs[1]:
            if depth == 0 or dep <= depth:
                ret[hold[dep]] = pl
            dep -= 1
        pl += 1
    return ret
def lin(i):
        i = str(i)
        if i == 'True':
            return 1
        if i == 'False':
            return 0
        return float(i)
def cvs(i):
    global vs
    if i in vs:
        return vs[i]
    return lin(i)
def car(a,o,b):
    global vs
    a = cvs(a)
    b = cvs(b)
    if o == '+':
        r = a+b
    if o == '-':
        r = a-b
    if o == '*':
        r = a*b
    if o == '/':
        r = a/b
    if o == '%':
        r = a%b
    if o == '^':
        r = a**b
    if o == '==':
        r = a==b
    if o == '!=':
        r = a!=b
    if o == '<':
        r = a<b
    if o == '>':
        r = a<b
    if o == '<=':
        r = a<=b
    if o == '>=':
        r = a>=b
    if o == 'and':
        r = a and b
    if o == 'or':
        r = a or b
    if o == 'xor':
        r = a + b == 1
    if o == 'xor-not':
        r = a + b == 1
    return r
def calc_t(toks):
    global vs
    val = None
    typ = None
    toksv = []
    for i in toks:
        if i == 'not':
            toksv.append('1')
            toksv.append('xor-not')
        else:
            toksv.append(i)
    toks = toksv
    ordops = [['xor','and','or'],['xor-not'],['==','!=','>=','<='],['+','-'],['*','/','%'],['^']]
    ordget = {}
    for i in range(len(ordops)):
        for j in ordops[i]:
            ordget[j] = i
    place = 1
    maxim = len(ordops)+1
    while place < len(toks)-1:
        cur = toks[place]
        maxim= min([maxim,ordget[cur]])
        place += 2
    if maxim == len(ordops)+1:
        a = cvs(toks[0])
        return a
    ret = [[]]
    for i in toks:
        if i in ordget and ordget[i] == maxim:
                ret[-1] = calc_t(ret[-1])
                ret.append(i)
                ret.append([])
        else:
            ret[-1].append(i)
    ret[-1] = calc_t(ret[-1])
    place = 1
    out = ret[0]
    while place < len(ret)-1:
        o = ret[place]
        b = ret[place+1]
        out = car(out,o,b)
        place += 2
    out = lin(out)
    return out
def token_n(wed):
    wed = wed+';'
    ret = wed.split()
    toks = []
    cur = ''
    for i in wed:
        if i in ['+','-','*','/','^','%','==','!=','<','>','<=','>=','not','and','or','xor']:
            toks.append(cur.lstrip().rstrip())
            toks.append(i)
            cur = ''
            i = ''
        cur += i
        if cur == ' ':
            cur = ''
    toks.append(cur[:-1])
    return toks
def figure_n(wed):
    wed = token_n(wed)
    wed = calc_t(wed)
    return wed
def i_eval(toks):
    global vs
    rev = [i[0] for i in toks]
    if 'paren' in rev:
        find = rev.index('paren')
        bind = len(rev)-rev[::-1].index('paren')
        if rev[find-1] == 'name':
            fun = toks[find-1][1]
            pl = 2
            while rev[find-pl] == 'dot':
                fun = toks[find-pl-1][1]+'.'+fun
                pl += 2
                find -= 2
            mk = toks[find+pl-1:bind-1]
            try:
                skp = pairo(mk,[['paren','('],['paren',')']],depth=1)
            except:
                print('\nerror')
                print('the pair function failed')
                print('there may be missing commas')
                exit()
            pl = 0
            perams = [[]]
            while pl < len(mk):
                if pl in skp:
                    perams[-1] += mk[pl:skp[pl]+1]
                    pl = skp[pl]
                elif mk[pl][0] == 'comma':
                    perams.append([])
                else:
                    perams[-1].append(mk[pl])
                pl += 1
            while [] in perams:
                del perams[perams.index([])]
            if fun == 'import':
                vsx = vs
                vs = {}
                name = perams[0][0][1]
                lexd = lex.main(open(name).read())
                run(lexd)
                ovs = vs
                vs = vsx
                for i in ovs:
                    vs['{}.'.format(name.split('/')[-1].split('.')[-2])+i] = ovs[i]
                return
            if fun == 'exec':
                pass
                #lexd = lex.main(i_eval())
                return
            elif fun == 'pyexec':
                return exec(i_eval(perams[0]),{},vs)
            elif fun == 'pyeval':
                return eval(i_eval(perams[0]),{},vs)
            elif fun == 'calc':
                return figure_n(perams[0][0][1])
            elif fun == 'func':
                var = i_eval(perams[1])
                vs[perams[0][0][1]] = [var,perams[2:]]
                return None
            elif fun == 'return':
                return ['return',i_eval(perams[0])]
            elif fun == 'read':
                return open(perams[0][0][1]).read()
            elif fun == 'write':
                open(perams[0][0][1],'w').write(i_eval(perams[1]))
                return
            elif fun == 'str.split':
                strin = i_eval(perams[0])
                return strin.split(i_eval(perams[1]))
            elif fun == 'str':
                return str(i_eval(perams[0]))
            elif fun == 'args':
                return perams
            elif fun == 'main':
                for i in perams:
                    i_eval(i)
                return
            elif fun == 'set':
                sto = i_eval(perams[1])
                vs[perams[0][0][1]] = sto
                return
            elif fun == 'print':
                for i in perams:
                    print(i_eval(i))
                return None
            elif fun == 'int':
                return float(i_eval(perams[0]))
            elif fun == 'add':
                t = 0
                for i in perams:
                    t += i_eval(i)
                return t
            elif fun == 'sub':
                t = i_eval(perams[0])
                for i in perams[1:]:
                    t -= i_eval(i)
                return t
            elif fun == 'mul':
                t = 1
                for i in perams:
                    t *= i_eval(i)
                return t
            elif fun == 'div':
                t = i_eval(perams[0])
                for i in perams[1:]:
                    t /= i_eval(i)
                return t
            elif fun == 'pow':
                t = i_eval(perams[0])
                for i in perams[1:]:
                    t = t ** i_eval(i)
                return t
            elif fun == 'mod':
                return i_eval(perams[0]) % i_eval(perams[1])
            elif fun == 'list':
                t = []
                for i in perams:
                    t.append(i_eval(i))
                return t
            elif fun == 'list.element':
                t = i_eval(perams[0])
                return t[i_eval(perams[1])]
            elif fun == 'list.index':
                t = i_eval(perams[0])
                return t.index(i_eval(perams[1]))
            elif fun == 'list.tostr':
                return ''.join
            elif fun == 'while':
                e = perams[0]
                while i_eval(e):
                    for i in perams[1:]:
                        i_eval(i)
                return
            elif fun == 'if':
                e = perams[0]
                if i_eval(e):
                    for i in perams[1:]:
                        i_eval(i)
                return
            elif fun == 'comp.ne':
                return i_eval(perams[0]) != i_eval(perams[1])
            elif fun == 'comp.e':
                return i_eval(perams[0]) == i_eval(perams[1])
            elif fun == 'comp.l':
                return i_eval(perams[0]) < i_eval(perams[1])
            elif fun == 'comp.g':
                return i_eval(perams[0]) > i_eval(perams[1])
            elif fun == 'comp.le':
                return i_eval(perams[0]) >= i_eval(perams[1])
            elif fun == 'comp.ge':
                return i_eval(perams[0]) <= i_eval(perams[1])
            elif fun in vs:
                func = vs[fun]
                hvs = vs
                vs = {}
                pl = 0
                for i in func[0]:
                    vs[i_eval(i)] = i_eval(perams[pl])
                    pl += 1
                for line in func[1]:
                    x = i_eval(line)
                    if isinstance(x,list) and len(x) == 2 and x[0] == 'return':
                        vs = hvs
                        return x[1]
                vs = hvs
            print(vs)
            print('\nerror!')
            print('you called a function that does not exsist')
            print('its name is \"'+fun+'\"')
            exit()
    t = toks[0][0]
    if t == 'name':
        t = []
        for i in toks:
            t.append(i[1])
        t = ''.join(t)
        if t in vs:
            return vs[t]
        else:
            print(vs)
            exit()

    if t == 'int':
        return float(toks[0][1])
    if t == 'str':
        r = str(toks[0][1])
        if r[0] == '$':
            r = vs[r[1:]]
        return r
def run(toks):
    global vs
    vs = {}
    tn = [[]]
    for i in toks:
        if i != ['newl']:
            tn[-1].append(i)
        else:
            tn.append([])
    while [] in tn:
        del tn[tn.index([])]
    for line in tn:
        i_eval(line)
def t_main(toks):
    run(toks)
vs = {}

if len(sys.argv) > 1:
    l = lex.main(open(sys.argv[1]).read())
    t_main(l)
else:
    print('please provide a file to run')
    name = input()
    l = lex.main(open(name).read())
    t_main(l)
