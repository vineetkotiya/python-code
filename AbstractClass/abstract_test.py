from abc import ABC ,abstractmethod

class Father(ABC):
    # abstract method define
    @abstractmethod
    def fun(self):
        pass

# concrete method
    def show(self):
        print("Show Father Details")
    

class Child(Father):
    def fun(self):
        print("father class")
    

c=Child()
c.show()    
c.fun()

