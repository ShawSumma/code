import token
import run
code = open('ions/1.ion').read()
tokens = token.token(code)
for i in tokens:
    print([j['type'] for j in i])
run.run(tokens)
