import os
from datetime import datetime
from functools import wraps


def logger(path):
    def __logger(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            func_time_call = datetime.now()
            result = old_function(*args, **kwargs)
            with open(f'{path}', 'a') as log:
                log.write(f"|{func_time_call}| FUNCTION NAME:{new_function.__name__}, ARGUMENTS:{args}, NAMED ARGUMENTS:{kwargs}, RETURNED VALUE:{result}\n")
                log.close()
            return result
        return new_function
    return __logger