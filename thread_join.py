from threading import Thread


class Mythread(Thread):
    def run(self):
        print("My Child Thread")

t=Mythread()
t.start()
# t.join(t)

for i in range(10):
    print("My Main Thread")
