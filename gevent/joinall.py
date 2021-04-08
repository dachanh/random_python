import gevent 


def fp():
    print("Running in fp")
    gevent.sleep(0)
    print("foo again")

def bar():
    print("Running in bar")
    gevent.sleep(0)
    print("bar again")

gevent.joinall([
    gevent.spawn(fp),
    gevent.spawn(bar)
])