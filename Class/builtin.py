class Empy:
    address = 'indore'

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    # def show(self):
    #     print("name " , self.name)
    #     print("age " , self.age)
    #     print("gender " , self.gender)


e = Empy('abhi', 23, 'male')
setattr(e, "name", "rahul")
print(getattr(e, "name"))
# delattr(e,'name')
print(getattr(e, "name"))
print(getattr(e, "address"))
