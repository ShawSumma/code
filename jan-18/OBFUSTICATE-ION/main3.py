f = open('main3.ion').read()
out = 'let _ion\n'
fis = []
for c in f.split('\n'):
    c = c.split()
    oc = c
    if len(c) < 1:
        pass
    elif c[0] == 'fi':
        f, *fis = fis
        print(f)
        out += 'now '+f[0]+'\n'
        out += 'add 1\n'
        out += 'end\n'
    elif len(c) < 2:
        pass
    elif c[1] == '=':
        f = c[0]
        out += 'let '+f+'\n'
        c = c[2:]
        for i in c:
            if i.isnumeric():
                out += 'add '+i+'\n'
            else:
                out += 'mov '+i+' _ion\n'
                out += 'mov _ion '+f'\n'
                out += 'now '+f+'\n'
    elif c[0][:5] == 'print':
        if c[1][0] == '~':
            c[1] = c[1][1:]
            i = ''.join([q+' ' for q in c[1:]])[:-1]
            i = i.replace('\\n','\n')
            for j in i:
                out += 'let _ion\n'
                out += 'add '+str(ord(j))+'\n'
                out += 'print _ion\n'
            continue
        for i in c[1:]:
            if not i.isnumeric():
                out += 'print '+i+'\n'
            else:
                out += 'let _ion\n'
                out += 'add 48\n'
                las = 48
                for k in i:
                    k = int(k)+48
                    if k-las > 0:
                        out += 'add '+str(k-las)+'\n'
                    if k-las < 0:
                        out += 'sub '+str(abs(k-las))+'\n'
                    out += 'print _ion\n'
                    las = k
        if c[0][5:] == 'ln':
            out += 'let _ion\n'
            out += 'add '+str(ord('\n'))+'\n'
            out += 'print _ion\n'
    elif c[1][-1] == '=':
        f = c[0]
        out += 'now '+f+'\n'
        opr = c[1][0]
        opr = {'+':'add','-':'sub'}[opr]
        for i in c[2:]:
            if i.isnumeric():
                out += opr+' '+i+'\n'
            else:
                out += 'mov '+i+' _ion\n'
                out += 'mov _ion '+f+'\n'
                out += 'now '+f+'\n'
    elif c[1] == '-=':
        f = c[0]
        out += 'now '+f+'\n'
        for i in c[2:]:
            out += 'add '+i+'\n'
    elif c[0] == 'if':
        ptr = c[1]
        fis = [c[1:]]+fis
        out += 'now '+ptr+'\n'
        out += 'sub '+c[2]+'\n'
        out += 'while '+ptr+'\n'
        out += 'add '+ptr+'\n'

open('main2.ion','w').write(out)
import main2
