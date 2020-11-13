import threading

x = 0


def increment():
    global x
    x += 1
    pass


def function_statement():
    global x
    for _ in range(50000):
        increment()
    print(threading.current_thread().name, " ", x)
    pass


def run_thread():
    thread1 = threading.Thread(target=function_statement)
    thread2 = threading.Thread(target=function_statement)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    pass


if __name__ == "__main__":
    for _ in range(2):
        run_thread()
