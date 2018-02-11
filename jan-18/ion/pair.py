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
def pair_inv(x,chs,depth=0):
    x = x[::-1]
    chs = chs[::-1]
    return pair(x,chs,depth=depth)
