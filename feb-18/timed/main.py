def main():
    global fns
    global vs
    code = open('eng.txt').read()
    lines = code.split('\n')
    pl = 0
    fns = {}
    vs = {}
    run(lines)
    print(vs)
def getvs(post):
    if post.isnumeric():
        return int(post)
    if post[:-1].isnumeric() and post[-1] in 'yzafpnumcdhkMGTPEZY':
        
    return vs[post]
def calc(post):
    if len(post) == 1:
        return getvs(post[0])
def run(lines):
    global fns
    global vs
    pl = 0
    while pl < len(lines):
        line = lines[pl].split()
        if 'is' in line:
            eq = line.index('is')
            pre = line[:eq]
            post = line[eq+1:]
            vs['pre'] = calc(post)
        pl += 1
main()
