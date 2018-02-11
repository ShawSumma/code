import pyb2
import pyb1
def strip(i):
    return i.lstrip().rstrip()
def end4s(file):
    depth = 0
    hold = {}
    ret = {}
    pl = 0
    for i in file.split('\n'):
        i = strip(i)
        if i[:3] == 'for':
            depth += 1
            hold[depth] = pl
        if i[:3] == 'end':
            ret[hold[depth]] = pl
            depth -= 1
        pl += 1
    return ret
def inter():
    global filee
    filee = []
    filein = open('test3.txt','r').read()
    file = inter_raw(filein)
    fileend = ''
    for i in filee:
        fileend += i+'\n'
    file = file+'halt\n'+fileend
    file = file.replace('\n\n','\n')
    open('test2.txt','w').write(file)
def inter_raw(filein):
    global filee
    ends = end4s(filein)
    file = []
    pl = 0
    nextl = 0
    xe = filein.split('\n')
    for i in xe:
        i = strip(i)
        if nextl == pl:
            if i[:3] == 'for':
                i = strip(i[3:])
                j = i.split()
                lisn = []
                rend = i[len(j[0]):]
                fnn = str(j[0])+'_'+str(pl)
                wolse = xe[pl+1:ends[pl]]
                wols = ''
                for i in wolse:
                    wols += i+'\n'
                wols = ['\t\t\t'+i for i in inter_raw(wols).split('\n')]
                nextl = ends[pl]
                file.append(str(j[0])+':'+rend)
                file.append('call '+fnn)
                lisn.append('\n\n')
                lisn.append('func '+fnn)
                lisn.append('\t'+j[0]+':'+j[0]+'-1')
                lisn.append('\t'+'switch '+j[0])
                lisn.append('\t\t'+'state 0.0')
                lisn.append('\t\t\t'+'ret 0')
                lisn.append('\t\t'+'state *')
                lisn += wols
                lisn.append('\t\t\t'+'call '+fnn)
                lisn.append('\t\t'+'end')
                lisn.append('\t'+'end')
                filee = lisn + filee
            elif i[:5] == 'print':
                i = strip(i[5:])
                file.append('print '+i)
            elif '=' in i:
                i = i.split('=')
                file.append(i[0]+':'+i[1])
        nextl += 1
        pl += 1
    fileout = ''
    for i in file:
        fileout += i+'\n'
    return fileout
inter()
pyb2.calc()
pyb1.calc()
