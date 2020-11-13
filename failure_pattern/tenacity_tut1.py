import os
import random
import tenacity


def error_function():
    if random.randint(0, 1) == 1:
        print("Failure")
        raise RuntimeError
    print("Sucess")
    pass


if __name__ == "__main__":
    for _ in range(10):
        tenacity.Retrying()(error_function())
