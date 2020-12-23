import os
import logging

LOGGING = "./logging"
os.makedirs(LOGGING, exist_ok=True)


def make_logger(logger_name, log_file, level=logging.INFO):
    log_setup = logging.getLogger(logger_name)

    formatter = logging.Formatter(
        "%(levelname)s: %(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p"
    )

    fileHandler = logging.FileHandler(log_file, mode="a")
    fileHandler.setFormatter(formatter)

    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    log_setup.setLevel(level)
    log_setup.addHandler(fileHandler)
    log_setup.addHandler(streamHandler)


def logger(msg, level, logfile):
    if logfile == "access":
        log = logging.getLogger("access")
    if logfile == "error":
        log = logging.getLogger("error")
    if logfile == "debug":
        log = logging.getLogger("debug")
    if level == "info":
        log.info(msg)
    if level == "warning":
        log.warning(msg)
    if level == "error":
        log.error(msg)


if __name__ == "__main__":
    make_logger("access", os.path.join(LOGGING, "access.log"))
    make_logger("debug", os.path.join(LOGGING, "debug.log"))
    make_logger("error", os.path.join(LOGGING, "error.log"))
    for a in range(100):
        for b in range(100):
            result = None
            for tmp in range(4):
                logger("a = {}, b ={}".format(a, b), "info", "access")
                try:
                    if tmp == 0:
                        result = a / b
                    if tmp == 1:
                        result = a + b
                    if tmp == 2:
                        result = a * b
                    if tmp == 3:
                        result = a - b
                    logger(
                        "stage " + str(tmp) + " = " + "result = " + str(result),
                        "info",
                        "debug",
                    )
                except Exception as e:
                    logger(e, "error", "error")
                    continue
