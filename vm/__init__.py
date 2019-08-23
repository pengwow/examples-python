from collections import Counter
ddd = ['22222','33333','44444','22222']
aaa = ['aaaaa','aaaaa','ddddd','aaaaa']


fff = list(zip(aaa,ddd))

xxx = Counter(fff)
print(xxx)

