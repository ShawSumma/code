def strip(s):
    return s.lstrip().rstrip()
file1 = open('main.txt').read()
states = {}
state = {}
for i in file1:
    i = strip(i)
    if i[:5] == 'state':
