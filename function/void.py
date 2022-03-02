# sum function is a void function because its not returning any value to function and void function is non returning function  
def sum(a,b):
    total=a+b
    print("Total : ",total)
    return total

x=sum(10,30)
print(x)

# add function is a non void function becasue its return value to function 
def add(a,b):
    total=a+b
    return total

x=sum(10,30)
print(x)
