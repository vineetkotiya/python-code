from threading import Thread


class Mythread(Thread):
    def run(self):
        print("My Child Thread")

t=Mythread()
t.start()


for i in range(10):
    print("My Main Thread")
