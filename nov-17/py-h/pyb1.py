def lin(i):
    i = str(i)
    if i == 'True':
        return 1
    if i == 'False':
        return 0
    return float(i)
def cvs(i):
    global vs
    if not 'vs' in {**globals(),**locals()}:
        vs = {}
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
def fplaces(wspt):
    jmps = {}
    wes = []
    for i in range(0,len(wspt)):
        i = len(wspt)-1-i
        if wspt[i][:1] == ':':
            jmps[wspt[i][1:].lstrip().rstrip()] = i
        wspt[i] = wspt[i].lstrip().rstrip()
        wes += [wspt[i]]
    wes = wes[::-1]
    return [jmps,wes]
def run(wed):
    global vs
    weds = wed.split('\n')
    jmps, weds = fplaces(weds)
    calls = []
    wed = []
    for i in weds:
        if len(i) > 0:
            wed.append(i.lstrip().rstrip())
    pl = 0
    while pl < len(wed):
        m = wed[pl]
        print('\t'+str(pl+1))
        set_t = m.split('is')
        if m[-1] == '?':
            m = m[:-1].lstrip().rstrip()
            n = figure_n(m)
            jmps = fplaces(weds[pl:])[0]
            n = str(n)
            n = str(n) if n in jmps else '*'
            n = jmps[n]
            pl += n
        elif m[0] == ':':
            pass
        elif len(set_t) == 2:
            set_t = [i.lstrip().rstrip() for i in set_t]
            vs[set_t[0]] = figure_n(set_t[1])
        elif m[:4] == 'call':
            m = m[4:]
            jmps = fplaces(weds)[0]
            calls.append(pl)
            pl = jmps[m.lstrip().rstrip()]
        elif m[:3] == 'jmp':
            m = m[3:]
            jmps = fplaces(weds)[0]
            pl = jmps[m.lstrip().rstrip()]
        elif m[:3] == 'ret':
            m = m[3:]
            jmps = fplaces(weds)[0]
            pl = calls[-1]
            calls = calls[:-1]
        else:
            p = figure_n(m.lstrip().rstrip())
            print(p)
        pl += 1
def openbap(name):
    global wed
    wed = open(name).read()
    return wed
def runbap():
    global name
    global vs
    vs = {}
    run(openbap(name))
calc = runbap
name = 'test1.txt'
