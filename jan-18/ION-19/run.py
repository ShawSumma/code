def pair(x,chs,depth=0,rev=False):
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
                if rev:
                    ret[pl] = hold[dep]
                else:
                    ret[hold[dep]] = pl
            dep -= 1
        pl += 1
    return ret
def run(tokens):
    pl = 0
    while pl < len(tokens):
        toks = tokens[pl]
        types = [i['type'] for i in toks]
        datas = [i['raw data'] for i in toks]
        if types[-1] == 'colon':
            pl += 1
