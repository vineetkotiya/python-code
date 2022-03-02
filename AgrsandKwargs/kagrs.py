def my(*marks,**var):
    print("Student Name is : ",var['name'])
    print("Student Marks : ",marks)


marks =[25,250]
var = {'name':'vineet'}
my(*marks,**var)