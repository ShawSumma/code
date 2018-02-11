def jn(l):
    return ''.join([str(i)+' ' for i in l])[:-1]
def swa(s,sl):
    sl = sorted(sl,key=len)[::-1]
    for i in sl:
        if s.startswith(i):
            return len(i)
    return 0
def inswa(s,sl):
    return swa(s[::-1],[i[::-1] for i in sl])
def mulin(s,sl):
    global mulint
    sl = sorted(sl,key=len)[::-1]
    for i in sl:
        if i in s:
            mulint = i
            return i
    mulint = ''
    return False
def msplit(l,p):
    l = [l]
    p.sort(key=len)
    p = p[::-1]
    while len(p) > 0:
        c,*p = p
        nl = []
        for i in l:
            nl += i.split(c)
        l = nl
    return l
def mrep(s,sp):
    for i in sp:
        s = s.replace(i,sp[i])
    return s
def getvar(i):
    k = i.lstrip().rstrip()
    mu = mulin(i,['varriable ','varriable called','the varriable called','the varriable','get','get varriable','var\''])
    if mu:
        ind = i.index(mu)
        pre = i[:ind]
        post = i[ind+len(mu):]
        c, *postl = post.split()
        while not c in vs:
            c += ' '+postl[0]
            postl = postl[1:]
        mid = vs[c]
        post = ''.join([i+' ' for i in postl])[:-1]
        return getvar(pre)+mid+getvar(post)
    return k
def setvar(i,d):
    k = i.lstrip().rstrip()
    if k in ['it', 'the last varriable used', 'the last varriable']:
        vs[vs['it']] = d
    else:
        vs[i] = d
        vs['it'] = i
f = open('main.ion').read().replace('\n',' ').split('. ')
pl = 0
vs = {'it':'it'}
nums = ['zero','one','two','three','four','five','six','seven','eight','nine']

while pl < len(f):
    i = f[pl]
    i = i.lstrip().rstrip()
    swalen = swa(i,['this program ','this sentance '])
    if swalen != 0:
        i = i[swalen:]
    swalen = swa(i,['display ','print ','write '])
    if swalen != 0:
        l = [' and ',', ',', and ']
        sw2 = swa(i,['write','write out'])
        if sw2 and mulin(i,[' to ',' to file ',' to the file ',' to the file named ']):
            ind = i.index(mulint)
            fili = i[ind+len(mulint):]
            i = i[sw2:ind]
            i = msplit(i,l)
            out = ''
            for j in i:
                out += getvar(str(j))+' '
            out = out[:-1]
            out = mrep(out,{'new line':'\n','a new line':'\n','space':'','a space':''})
            open(fili,'w').write(out)
        else:
            i = msplit(i[swalen:],l)
            out = ''
            for j in i:
                out += getvar(str(j))+' '
            out = out[:-1]
            out = mrep(out,{'new line':'\n','a new line':'\n','space':'','a space':''})
            print(out)
        pl += 1
        continue
    swalen = swa(i,['run','do','execute'])
    if swalen != 0:
        i = i[swalen+1:]
        if swa(i,'the next'):
            pass
        pl += 1
        continue
    swalen = swa(i,['set ','make ','the var '])
    if swalen != 0 or mulin(i,[' is ',' is now ',' euqals ']):
        l = [' and ',', ',', and ']
        for i in msplit(i,l):
            if swalen == 0:
                ind = i.index(mulint)
                vn = i[:ind]
                vd = i[ind+len(mulint):]
                setvar(vn,getvar(vd))
    pl += 1
#print(vs)
