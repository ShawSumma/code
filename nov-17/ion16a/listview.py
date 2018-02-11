def viewraw(lis,d=0,):
    d += 1
    c = []
    for i in range(len(lis)):
        j = lis[i]
        if isinstance(j,list):
            c.append('  '*(d-1)+'[')
            c += viewraw(j,d=d)
            c.append('  '*(d-1)+']')
        else:
            c.append('  '*(d-1)+str(j))
    return c
def view(lis):
    ret = ''
    for i in viewraw(lis):
        ret += i+'\n'
    return ret
