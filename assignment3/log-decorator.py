# Task 1: Writing and Testing a Decorator

import logging

logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log", "a"))


def logger_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        func_name = func.__name__
        pos_args = args if args else "none"
        kw_args = kwargs if kwargs else "none"
        log_message = (
            f"function: {func_name}\n"
            f"positional parameters: {pos_args}\n"
            f"keyword parameters: {kw_args}\n"
            f"return: {result}\n"
        )

        logger.log(logging.INFO, log_message)
        return result

    return wrapper


@logger_decorator
def greeting():
    print("Hello, World!")


@logger_decorator
def check_values(*args):
    return True


@logger_decorator
def keyword_logger(**kwargs):
    return logger_decorator


if __name__ == "__main__":
    greeting()
    check_values(10, 20, 30)
    keyword_logger(first_name="Jane", last_name="Smith", age=35)
