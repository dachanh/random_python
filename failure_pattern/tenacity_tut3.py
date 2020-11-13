import random

import tenacity

"""
random time 
"""


def error_function():
    if random.randint(0, 1) == 1:
        print("Failure")
        raise RuntimeError
    print("Sucess")
    pass


@tenacity.retry(wait=tenacity.wait_fixed(10) + tenacity.wait_random(0, 3))
def retry_error():
    error_function()


if __name__ == "__main__":
    for _ in range(10):
        retry_error()
