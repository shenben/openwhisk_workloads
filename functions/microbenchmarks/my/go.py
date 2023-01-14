import os
ls = os.listdir(os.getcwd())
print(ls)
for i in ls:
    j = i.split('.')
    if j[-1] != 'py':
        print(i)
        os.remove(i)