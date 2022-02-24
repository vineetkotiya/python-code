from random import randrange
from threading import Thread
def mythead():
    print("My Number :")


for i in range(10):
    t=Thread(target=mythead)
    t.start()
for j in range(5):
    print("Thanku ")

