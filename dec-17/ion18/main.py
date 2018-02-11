import token
import tree

data = open('main.ion').read()
tokens = token.token(data)
open('tree.txt','w').write(str(tokens))
out = tree.make(tokens)
open('out.py','w').write(out)
