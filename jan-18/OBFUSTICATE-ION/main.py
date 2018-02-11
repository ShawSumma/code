o = open('main.ion').read()
p,d,v = 0,0,0
j = {}
r = [0 for i in range(2**16)]
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
            if depth == 0 or dep <= depth:
                ret[hold[dep]] = pl
            dep -= 1
        pl += 1
    return ret
pr = pair(o,'[]')
while p < len(o):
    c = o[p]
    r[v]
    if c == '+':
        r[v] = (r[v]+1) % 2**8
    elif c == '-':
        r[v] = (r[v]-1) % 2**8
    elif c == '>':
        v = (v+1) % 2**16
    elif c == '<':
        v = (v-1) % 2**16
    elif c == '.':
        print(chr(r[v]),end='')
    elif c == ',':
        r[v] = int(input())
    elif c == '[':
        d += 1
        if r[v] == 0:
            pass
            p = pr[p]
        j[d] = p
    elif c == ']':
        if r[v] != 0:
            p = j[d] - 1
        d -= 1
    p += 1
