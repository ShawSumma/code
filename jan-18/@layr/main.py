import sys
def rall(l):
    global pl
    def getvs(bvs):
        if bvs[0] == '$':
            r = vs[bvs[1:]]
        elif bvs[0] == '\'' and bvs[-1] == '\'':
            r = bvs[1:-1]
        else:
            r = int(bvs)
        return r
    points = {}
    for pl,lp in enumerate(l):
        if lp.lstrip().rstrip() == '':
            pl += 1
            continue
        if lp[-1] == ':':
            points[lp[:-1]] = pl
    traces = []
    vs = {'lis':[]}
    pl = 0
    while pl < len(l):
        lp = l[pl]
        if lp == '':
            pl += 1
            continue
        #print(vs)
        if lp[:3] in ['jmp','run']:
            ix = lp[4:].split()[::-1]
            a = getvs(ix[0])
            b = ix[1]
            if a != 0:
                if lp[:3] == 'run':
                    traces.append(pl)
                pl = points[b]
        elif lp[:3] == 'ret':
            pl = traces[-1]
            traces = traces[:-1]
        elif lp[:3] in ['add','sub','mul','div']:
            ix = lp[4:].split()
            a,b = ix
            v = a
            a = vs[a]
            b = getvs(b)
            ms = {
                'add':lambda a,b: a+b,
                'sub':lambda a,b: a-b,
                'mul':lambda a,b: a*b,
                'div':lambda a,b: a//b,
            }
            r = ms[lp[:3]](a,b)
            vs[v] = r
        elif lp[:3] in ['equ','les','gre','loe','goe','neq']:
            ix = lp[4:].split()
            a,b = ix
            v = a
            a = vs[a]
            b = getvs(b)
            ms = {
                'equ':lambda a,b: a==b,
                'neq':lambda a,b: a!=b,
                'les':lambda a,b: a<b,
                'gre':lambda a,b: a>b,
                'loe':lambda a,b: a<=b,
                'goe':lambda a,b: a>=b,
            }
            r = ms[lp[:3]](a,b)
            vs[v] = int(r)
        elif lp[:3] == 'mov':
            ix = lp[4:].split()
            a,*b = ix
            b = ''.join(i+' ' for i in b)[:-1]
            r = getvs(b)
            vs[a] = r
        elif lp[:4] == 'push':
            ix = lp[5:].split()
            a,*b = ix
            b = ''.join(i+' ' for i in b)[:-1]
            r = getvs(b)
            vs[a].append(r)
        elif lp[:3] == 'pop':
            ix = lp[4:].split()
            a,b = ix
            vs[a] = vs[b][-1]
            del vs[b][-1]
        elif lp[:4] == 'size':
            ix = lp[4:].split()
            a,b = ix
            vs[a] = len(vs[b])
        elif lp[0] == '*':
            print(vs[lp[2:]])
        pl += 1
f = open(sys.argv[1]).read()
l = f.split('\n')
l = list(map(lambda x: x.lstrip().rstrip(), l))
try:
    rall(l)
except:
    print('line : %i' % (pl+1))
    raise
