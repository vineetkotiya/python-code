class Student:
    address = 'indore'  #class variable
    def __init__(self,name):
        self.name=name #instance variable
    def show(self):
        pin = 25   #local variable
        print(self.name,self.address,pin)

    def show1(self):
        print(self.pin,self.name,self.indore)
x=Student('rahul')
x.show()
x.show1()