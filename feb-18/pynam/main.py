import shlex, subprocess, time
def rc(*args):
    if len(args) == 0:
        rt = str
    else:
        rt = args[0]
    args = shlex.split('gcc %s -o _a.out' % 'test.c')
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    c = p.communicate()
    if not c[1] in [None,'']:
        print('error')
    else:
        args = shlex.split('./_a.out')
        p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        c = p.communicate()
        return rt(c[0].split('\n')[-1])
def ping(data):
    wx = open('test.c','w')
    orig = open('_ping.c','w').read()
    orig = orig.replace('--data-1--',data)
    wx.write(orig)
    t = time.time()
    rc()
x = rc(float)
print(x)
