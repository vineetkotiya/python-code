age =[12,34,2,4,42,43,23]

def myfun(x):
    if x<18:
        return False
    else:
        return True


ages = filter(myfun,age)

for i in ages:
    print(i)