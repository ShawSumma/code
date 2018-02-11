def make(tokens):
    if tokens == []:
        return ''
    if isinstance(tokens[0],list):
        tabs = [0]*len(tokens[0])
        for i in tokens:
            rad = [i['raw data'] for i in tokens[0]]
            if '}' == rad[-1]:
                tabs
            o = make(i)

    return 'xe'
