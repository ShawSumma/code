from pair import *
ordops = [
    ['*','/','%'],
    ['+','-'],
    ['==','!=','<=','>=','<','>'],
    ['..'],
    ['='],
]

pyord = [
    '=','+=','-=','*=','/='
]

optrans = {
    '..' : 'range(0,1)'
}

def makeop(toks):
    global ordops
    global tokens
    tokens = toks
    opt = []
    i = 0
    pars = pair([i['data'] for i in tokens],['(',')'])
    while i < len(tokens):
        if i in pars:
            opt += [-1] * (pars[i] - i+1)
            i = pars[i]+1
        if i < len(tokens):
            if tokens[i]['type'] == 'op':
                o = ordops[tokens[i]['data']]
            else:
                o = -1
            opt.append(o)
            i += 1
    return opt
def getop(optyp):
    global ordops
    global tokens
    gelk = optyp
    if optyp in optrans:
        gelk = optrans[optyp]
        gelk = gelk.replace('0','~~0~~').replace('1','~~1~~')
        gelk = gelk.replace('~~0~~',gen(tokens[:pl]))
        gelk = gelk.replace('~~1~~',gen(tokens[pl+1:]))
    return gelk

def main():
    global ordops
    v = ordops
    ordops = {}
    for pl,l in enumerate(v):
        for j in l:
            ordops[j] = pl

main()
