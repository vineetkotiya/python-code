from functools import reduce
x = [2,1,5,6,]

# def sum(a,b):
#     print("value a = ",a)
#     print("value b = ",b)
#     # print("value")
#     return a+b

fun = reduce(lambda a,b:a+b,x)
print(fun)
