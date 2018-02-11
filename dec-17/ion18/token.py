import re
def token(code):

    code = '\n'+code
    while '\n\n' in code:
        code = code.replace('\n\n','\n')
    ops = ['=','+=','*=','-=','/=']
    ops += ['+','*','-','/','**','%']
    ops += ['..']
    ops += ['==','!=','<=','>=','<','>']
    ops += ['&&','!&&','||','|*|','!|*|','<-']
    ops += ['.']
    ops.sort(key=len)
    ops = ops[::-1]

    keywords = ['if','elif','else']
    keywords += ['break','while','for']
    keywords += ['true','false']
    keywords += ['try','except','global','def']
    keywords += ['int','float','list']
    keywords.sort(key=len)
    keywords = keywords[::-1]
    keywords = []

    parenre = re.compile(r'\(|\)')
    brackre = re.compile(r'\{|\}')
    squre = re.compile(r'\[|\]')
    comma = ','

    decimalre = re.compile(r'[0-9]+\.[0-9]+')
    intre = re.compile(r'[0-9]+')
    namere = re.compile(r'[a-zA-Z_]+[a-zA-Z0-9_]*')
    ignore = [' ','\t','\n']

    holdpar = {}
    pardep = 0
    holdsqu = {}
    squdep = 0
    holdbra = {}
    bradep = 0

    tokens = []
    line = 0
    while len(code) > 0:
        while code[0] in ignore:
            if code[0] == '\n':
                code = code[1:]
                line += 1
                tokens.append({'type':'newl','raw data':'\n','line':line})
            else:
                code = code[1:]
            if len(code) == 0:
                break
        go = True

        decm = decimalre.match(code)
        if decm != None:
            span = decm.span()
            decsize = span[1]-span[0]
            token = {
                'type':'dec',
                'raw data':code[:decsize],
                'line':line,
            }
            tokens.append(token)
            code = code[decsize:]
            go = False
        if go != False:
            for i in ops:
                if code.startswith(i):
                    opsize = len(i)
                    token = {
                        'type':'op',
                        'raw data':code[:opsize],
                        'line':line,
                    }
                    tokens.append(token)
                    code = code[opsize:]
                    go = False
                    break
        if go != False:
            intm = intre.match(code)
            if intm != None:
                mspan = intm.span()
                intsize = mspan[1]-mspan[0]
                token = {
                    'type':'int',
                    'raw data':code[:intsize],
                    'line':line,
                }
                tokens.append(token)
                code = code[intsize:]
                go = False
        if go != False:
            intm = parenre.match(code)
            if intm != None:
                mspan = intm.span()
                size = 1
                ty = code[:1]
                token = {
                    'type':'paren',
                    'raw data':ty,
                    'line':line,
                }
                if ty == '(':
                    token['depth'] = pardep
                    pardep += 1
                    holdpar[pardep] = len(tokens)
                else:
                    token['back'] = holdpar[pardep]
                    pardep -= 1
                    token['depth'] = pardep
                tokens.append(token)
                code = code[1:]
                go = False
        if go != False:
            if len(code) > 0 and code[0] == ':':
                token = {
                    'type':'colon',
                    'raw data':':',
                    'line':line,
                }
                tokens.append(token)
                code = code[1:]
                go = False
        if go != False:
            intm = brackre.match(code)
            if intm != None:
                mspan = intm.span()
                size = 1
                ty = code[:1]
                token = {
                    'type':'braket',
                    'raw data':ty,
                    'line':line,
                }
                if ty == '{':
                    token['depth'] = bradep
                    bradep += 1
                    holdbra[bradep] = len(tokens)
                else:
                    token['back'] = holdbra[bradep]
                    bradep -= 1
                    token['depth'] = bradep
                tokens.append(token)
                code = code[1:]
                go = False
            if go != False:
                intm = squre.match(code)
                if intm != None:
                    mspan = intm.span()
                    size = 1
                    ty = code[:1]
                    token = {
                        'type':'squket',
                        'raw data':ty,
                        'line':line,
                    }
                    if ty == '[':
                        token['depth'] = squdep
                        squdep += 1
                        holdsqu[squdep] = len(tokens)
                    else:
                        token['back'] = holdsqu[squdep]
                        squdep -= 1
                        token['depth'] = squdep
                    tokens.append(token)
                    code = code[1:]
                    go = False
            if go != False:
                if code.startswith(comma):
                    namesize = len(comma)
                    token = {
                        'type':'comma',
                        'raw data':code[:1],
                        'line':line,
                    }
                    tokens.append(token)
                    code = code[1:]
                    go = False
            if go != False:
                for i in keywords:
                    if code.startswith(i):
                        namesize = len(i)
                        token = {
                            'type':'keyword',
                            'raw data':code[:namesize],
                            'line':line,
                        }
                        tokens.append(token)
                        code = code[namesize:]
                        go = False
                        break
            if go != False:
                intm = namere.match(code)
                if intm != None:
                    mspan = intm.span()
                    intsize = mspan[1]-mspan[0]
                    token = {
                        'type':'name',
                        'raw data':code[:intsize],
                        'line':line,
                    }
                    tokens.append(token)
                    code = code[intsize:]
                    go = False
    out = []
    for i in tokens:
        if i['type'] == 'newl':
            out.append([])
        else:
            out[-1].append(i)
    return out[:-1]
