def student(*mark,**stud):
    for key , value  in stud.items():
        print(key ,":", value)

    for j in  mark:
        print("Student Makrs",j)
stud ={'name':'vineet','agedss':25}
mark = [121,32]

student(*mark,**stud)