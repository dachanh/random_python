from scoop import futures


def product(x, y):
    return x * y


def sum(x, y):
    return x + y


if __name__ == "__main__":
    a = range(1, 101)
    b = range(101, 201)
    total = futures.mapReduce(product,sum,a,b)
    print("result : ", total)
