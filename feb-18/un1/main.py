class game:
    def __init__(self):
        print(dia['intro'])
def load_dia():
    global dia
    dat = open('dia.txt').read()
    dia = {}
    for block in dat.split('.name'):
        block = block.lstrip().rstrip()
        if block != '':
            i = block.index('\n')
            dia[block[:i]] = block[i:].lstrip().rstrip()
load_dia()
main = game()
