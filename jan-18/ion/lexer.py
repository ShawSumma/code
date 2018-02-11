import re
def tokenize(mats,strin):
    tokens = []
    while strin != '':
        for pl,mat in enumerate(mats):
            match = mat(strin)
            if not match in [{},None]:
                a = strin[:match['pos'][0]]
                b = strin[match['pos'][1]:]
                del match['pos']
                match['id'] = pl
                ign = match['type'] == 'ignore'
                if not ign:
                    tokens.append(match)
                strin = a+b
                break
    return tokens

def token(*args):
    def w(fun):
        def sub(curtok):
            out = fun(curtok)
            out['ignore'] = False
            if len(args) == 1:
                reg = args[0]
                mat = re.match(reg,curtok)
                if mat != None:
                    name = fun.__name__
                    out['type'] = name if name[:2] != 't_' else name[2:]
                    out['pos'] = []
                    out['pos'] += mat.span()
                    beg = out['pos'][0]
                    end = out['pos'][1]
                    out['data'] = curtok[beg:end]
            else:
                name = fun.__name__
                out['type'] = name if name[:2] != 't_' else name[2:]
                flags = args[0].split(' ')
                if 'in' in flags:
                    for i in args[1]:
                        if curtok.startswith(i):
                            out['pos'] = [0,len(i)]
                            out['data'] = i
                else:
                    reg = args[1]
                    mat = re.match(reg,curtok)
                    if mat != None:
                        name = fun.__name__
                        out['type'] = name if name[:2] != 't_' else name[2:]
                        out['pos'] = []
                        out['pos'] += mat.span()
                        beg = out['pos'][0]
                        end = out['pos'][1]
                        out['data'] = curtok[beg:end]
            #print(out)
            if not 'pos' in out:
                return {}
            return out
        return sub
    return w
