def make(tree):
    if isinstance(tree,list) and tree != []:
        if tree[0] in ['if','elif','else']:
            run = 0
            while not isinstance(tree[run],list):
                run += 1
            out = [tree[0],[make(tree[1:run]),make(tree[run])]]
            out.append(make(tree[run+1]))
            return out
        elif len(tree) > 1:
            out = ['call',[make(tree[0]),make(tree[1])]]
            out += [make(tree[2:])] if len(tree) > 2 else []
            return out
        else:
            return tree[0]
    return tree
