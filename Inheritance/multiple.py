class Base1:
    def __init__(self, name):
        self.name = name
        # print("Base 1 class")


class Base2:
    def __init__(self, address, name):
        Base1.__init__(self,name)
        self.address = address
        # print("Base 2 class")


class Normal(Base1, Base2):
    def __init__(self, amount, address, name):
        Base2.__init__(self,address, name)
        # super().__init__(name)
        self.amount = amount
        print("Normal Class")

    def show(self):
        print(self.amount, self.name, self.address)


n = Normal(10, 'indore', 'lakhan')
n.show()
