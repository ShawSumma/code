import sys
def getvs(s):
    if s.isnumeric():
        return s
    else:
        return '$%s' % s
def math(el,temp='0'):
    global out
    tempv = temp
    if len(el) == 1:
        return getvs(el[0])
    tlis = {
        '+' : 'add',
        '-' : 'sub',
        '*' : 'mul',
        '/' : 'div',
    }
    pli = 0
    ret = ''
    nt = '_temp_%s' % tempv
    ret += 'mov %s %s\n' % (nt, getvs(el[0]))
    while len(el) > 1:
        typ = tlis[el[1]]
        ret += typ+' %s %s\n' % (nt, getvs(el[2]))
        el = el[2:]
    return ret
def emath(e):
    if len(e) > 1:
        ret = ''
        ret += math(e)
        nam = '_temp_%s' % 0
        return ret+'mov _temp_out $%s\n\n' % nam
    else:
        out = 'mov _temp_out %s\n' % getvs(e[0])
        return out
def inter(l):
    global out
    out = 'mov _lis $lis\n'
    whd = {}
    for line in l:
        #print(line)
        if line.lstrip().rstrip() == '':
            continue
        cs = line.split()
        if len(cs) <= 0:
            continue
        if cs[0] == 'func':
            out += 'jmp _end_%s 1\n' % cs[1]
            name = '%s:\n' % cs[1]
            out += name
        if cs[0] == 'end':
            if cs[1] == 'func':
                out += 'ret\n'
                name = '_end_%s:\n' % (cs[2])
                out += name
            if cs[1] == 'if':
                name = '_end_%s:\n' % (cs[2])
                out += name
            if cs[1] == 'while':
                name = '_end_%s:\n' % (cs[2])
                out += name
                out
        if cs[0] == 'call':
            out += 'mov %s.args $_lis\n'
            for pl,i in enumerate(cs[2:]):
                gr = emath(cs[2:])
                out += gr
                out += 'push %s.args %s\n' % (cs[1],emath(i))
            out += 'run %s 1\n' % cs[1]
        if cs[0] == 'print':
            gr = emath(cs[1:])
            out += gr
            out += '* _temp_out\n'
        if len(cs) <= 1:
            continue
        if cs[1] == '=':
            if cs[2] != 'list':
                gr = emath(cs[2:])
                out += gr
                out += 'mov %s $_temp_out\n' % cs[0]
            else:
                out += 'mov %s $_lis\n' % cs[0]
        if cs[0] == 'push':
            gr = emath(cs[2:])
            out += gr
            out += 'push %s $_temp_out\n' % cs[1]
        if cs[0] == 'pop':
            gr = emath(cs[2:])
            out += gr
            out += 'pop %s _temp_out\n' % cs[1]
        if cs[0] == 'if':
            gr = emath(cs[1:-1])
            out += gr
            out += 'equ _temp_out 0\n'
            out += 'jmp _end_%s $_temp_out\n' % cs[-1]
        if cs[0] == 'while':
            out += 'jmp _end_%s 1\n' % cs[-1]
            whd[cs[-1]] = cs[1:-1]
    return out
f = sys.argv[1]
f = open(f).read()
l = f.split('\n')
l = list(map(lambda x: x.lstrip().rstrip(), l))
o = inter(l)
open(sys.argv[2],'w').write(o)
