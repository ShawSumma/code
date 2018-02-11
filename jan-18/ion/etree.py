import ops
from pair import *
def make(tokens):
    types = [i['type'] for i in tokens]
    data = [i['data'] for i in tokens]
    toks = list(zip(types,data))
    print(toks)
    pairs = {
        'lparen':pair(data,'()'),
        'rparen':pair_inv(data,'()'),
    }
    out = []
    if pairs['lparen'] != {}:
        ww = pairs['lparen']
        begi = min(ww)
        endi = ww[begi]
        if data[0] in words:
            kind = data[0]
            firstind = min(ww)
            pairind = ww[firstind]
            pre = tokens[1:firstind]
            mid = tokens[firstind+1:pairind]
            aft = tokens[pairind+1:]
            pre = make(pre)
            mid = make(mid)
            aft = make(aft)
            return ['do',[kind,pre,mid],aft]
        if tokens[begi-1]['type'] != 'name':
            pre = tokens[:begi]
            mid = tokens[begi+1:endi]
            post = tokens[endi+1:]
            return make(pre)+[make(mid)]+make(post)
        else:
            pre = make(tokens[:begi-1])
            mid = make(tokens[begi+1:endi])
            post = make(tokens[endi+1:])
            out = [pre, ['call',data[begi-1],mid], post]
            if out[0] == []:
                out = out[1:]
            if out[-1] == []:
                out = out[:-1]
            return out

    if 'op' in types:
        while 'op' in types:
            bestop = ops.makeop(tokens)
            ind = bestop.index(max(bestop))
            maxop = data[ind]
            maxi = max(bestop)
            mid = ops.getop(maxop)
            pre = make(tokens[:ind])
            out = []
            out.append(make(mid))
            tokens = tokens[ind:]
        post = make(tokens)
        return ['op',mid,[out],post]
    return data
words = [
    'if',
    'elif',
    'else'
]
