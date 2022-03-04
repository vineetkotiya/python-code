def gen(x):
    # print("Value of ",x,y)
    # t=x+40
    yield x


for i in range(100):
    x=gen(i)
    print(x)
    print(next(x))
    