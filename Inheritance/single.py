class School:
    def __init__(self,pin):
        self.name = "DPS"
        self.address = 'indore'
        self.pin=pin


class Student(School):
    def __init__(self,pin):
        super().__init__(pin)
        self.stud_name = 'Ajay'
        self.stud_fees = 3000

    def show(self):
        print("School Name : ",self.name)
        print("School Address : ",self.address)
        print("Student Name: ",self.stud_name)
        print("Student Fees: ",self.stud_fees)
        print("Student Pin: ",self.pin)

s=Student(2112)
s.show()