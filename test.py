import time, threading


def first():
    start = time.time()
    for i in range(100000000):
        pass
    stop = time.time()
    print(stop-start)

def second():
    start = time.time()
    for i in range(100000000):
        pass
    stop = time.time()
    print(stop-start)

thread1 = threading.Thread(target=first)
thread2 = threading.Thread(target=second)

thread1.start()
thread2.start()

thread1.join()
thread2.join()