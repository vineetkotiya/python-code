from abc import ABC ,abstractmethod

class Gun(ABC):
    @abstractmethod
    def area(self):
        pass
    
    def gun(self):
        print("GUN : AK-47")


class Army(Gun):
    def area(self):
        print("Area Land")


class Navy(Gun):
    def area(self):
        print("Area Under water")
        

class Airforce(Gun):
    def area(self):
        print("Area Sky")
        

a=Army()
n=Navy()
af=Airforce()

a.area()
a.gun()
n.area()
n.gun()
af.area()
af.gun()