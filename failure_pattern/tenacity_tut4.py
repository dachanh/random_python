import random

import tenacity


def error_function():
    if random.randint(0, 1) == 1:
        print("Failure")
        raise RuntimeError
    temp = None if random.randint(0,10) == 2 else 0
    print("Sucess ",temp)
    return None


@tenacity.retry(
    wait=tenacity.wait_fixed(10),
    stop=tenacity.stop_after_delay(1),
    retry=(
        tenacity.retry_if_exception_type(IOError)
        | tenacity.retry_if_result(lambda result: result == None)
    )
)
def retry_error():
    global timming
    error_function()
    print(timming)
    timming += 1


if __name__ == "__main__":
    timming = 0
    for _ in range(10):
        retry_error()
