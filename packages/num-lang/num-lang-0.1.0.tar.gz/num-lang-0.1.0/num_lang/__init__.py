__version__ = '0.1.0'

def parse(code):
    def algonum(x, y):
        final = []
        for i in range(len(x)): final.append([x[i], str(i + y)])
        return final
    
    alphabetlow = {v:k for k, v in algonum("abcdefghijklmnopqrstuvwxyz", 0)}
    alphabethigh = {v:k for k, v in algonum("abcdefghijklmnopqrstuvwxyz".upper(), 26)}
    nums = {v:k for k, v in algonum("1234567890", 52)}
    other = {v:k for k, v in algonum("'" + '"/*-+!@#$%^&*()_[]{};:|\,./<>?/ `~', 62)}
    
    algo = {**alphabetlow, **alphabethigh, **nums, **other}
    
    final = ""
    
    for i in code:
        i = i.split("/")
        for j in i:
            try: final += algo[j]
            except: pass
        final += "\n"
    
    return final