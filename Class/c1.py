from unicodedata import name


class c1:
    def __init__(self, name,roll,address,pin):
        self.name = name
        self.roll = roll
        self.address = address
        self.pin = pin

    def show(self):
        print("Name : ", self.name)
        print("Address : ", self.address)
        print("Roll : ", self.roll)
        print("Pin : ", self.pin)


s = c1('vineet', 32323,'indore',76767)
s.show()
