def strip(i):
    return i.lstrip().rstrip()
def calc():
    global name
    fileinx = open(name,'r').read()
    file = []
    opens = 0
    for i in fileinx.split('\n'):
        i = strip(i)
        if i[:6] == 'switch':
            file.append(strip(i[6:])+' ?')
            opens += 1
        elif i[:5] == 'state':
            i = strip(i[5:])
            file.append('jmp end'+str(opens))
            file.append(':'+i)
        elif i[:3] == 'end':
            file.append(':end'+str(opens))
            opens -= 1
        elif i == 'halt':
            file.append('jmp exit')
        elif i[:4] == 'func':
            i = strip(i[4:])
            file.append(':'+i)
        elif i[:3] == 'ret':
            i = strip(i[3:])
            if i == '':
                i = '0'
            file.append('out is '+ i)
            file.append('ret')
        elif i[:5] == 'print':
            if i[:4] == 'call':
                ic = strip(i[4:])
                file.append('call '+ic)
                i == 'out'
            else:
                i = strip(i[5:])
            file.append(i)
        elif i[:4] == 'call':
            i = strip(i[4:])
            file.append('call '+i)
        elif ':' in i:
            i = i.split(':')
            i[1] = strip(i[1])
            if i[1][:4] == 'call':
                ic = strip(i[1][4:])
                file.append('call '+ic)
                file.append(strip(i[0])+' is out')
            else:
                file.append(strip(i[0])+' is '+i[1])
    if 'jmp exit' in file:
        file.append(':exit')
    fileout = ''
    for i in file:
        fileout += i+'\n'
    open('test1.txt','w').write(fileout)
name = 'test2.txt'
if __name__ == '__main__':
    import pyb1
    calc()
    pyb1.calc()
