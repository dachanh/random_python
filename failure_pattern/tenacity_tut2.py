import random

import tenacity


def error_function():
    global successed
    if random.randint(0, 1) == 1:
        print("Failure")
        raise RuntimeError
    print("Sucess ", successed)
    successed += 1
    pass


@tenacity.retry(wait=tenacity.wait_fixed(1))
def retry_error():
    error_function()


if __name__ == "__main__":
    successed = 1
    for _ in range(10):
        retry_error()
