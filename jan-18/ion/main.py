import lex
import etree
import tree
import view
f = open('main.ion').read()
l = lex.make(f)
e = etree.make(l)
view.view(e)
#t = tree.make(e)
#print(t)
