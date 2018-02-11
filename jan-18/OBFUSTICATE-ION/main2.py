code = open('main2.ion').read()
op = ''
ld = {}
ldt = {}
vn = {'_Hold':1}
d = 0
pl = 0
def nvs(v):
    jn = vn[v]-pl
    c = '>' if vn[v] > pl else '<'
    ic = '>' if c == '<' else '<'
    return [c*abs(jn),ic*abs(jn),jn]
for i in code.split('\n'):
    i = i.lstrip().rstrip()
    if i[:3] == 'add':
        op += '+'*(int(i[4:]))
    if i[:3] == 'sub':
        op += '-'*(int(i[4:]))
    if i[:4] == 'loop':
        d += 1
        a,b,n = nvs(i[5:])
        op += a
        op += '['
        op += b
        ld[d] = a
        ldt[d] = i[5:]
    if i[:3] == 'end':
        op += ld[d]
        a,b,no = nvs(ldt[d])
        op += a
        op += ']'
        d -= 1
        pl += no
    if i[:4] == 'aloc':
        c = len(vn) + 1
        vn[i[5:]] = c
    if i[:3] == 'let':
        c = len(vn) + 1
        vn[i[4:]] = c
        i = 'now'+i[3:]
        a,b,no = nvs(i[4:])
        op += a
        op += '[-]'
        pl += no
    if i[:3] == 'now':
        a,b,no = nvs(i[4:])
        op += a
        pl += no
    if i[:5] == 'print':
        a,b,no = nvs(i[6:])
        op += a
        op += '.'
        op += b
    if i[:4] == 'out':
        op += '.'
    if i[:3] == 'mov':
        i = i[4:].split(' ')
        a,b,dif = nvs(i[0])
        pl += dif
        hold,bhold,dif3 = nvs('_Hold')
        a2,b2,di2 = nvs(i[1])
        cop = ''
        cop += a
        cop += '['
        cop += '-'+hold+'+'+bhold
        cop += a2
        cop += '+'
        cop += b2
        cop += ']'
        cop += hold
        cop += '['
        cop += '+'+bhold+'-'+hold
        cop += ']'
        cop += bhold
        op += cop
        cop += bhold
open('main.ion','w').write(op)
import main
