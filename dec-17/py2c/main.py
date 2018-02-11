import tokenize
def mktok(file):
    x = tokenize.generate_tokens(file.readline)
    for i in x:
        k = list(i)
        n = {
         'name' : k[1],
         'lr' : k[4],
        }
        print(n)
mktok(open('test.py'))
