import os
from datetime import datetime
from functools import wraps


def logger(path):
    def __logger(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            func_time_call = datetime.now()
            error = None
            try:
                result = old_function(*args, **kwargs)
                with open(f'{path}', 'a') as log:
                    log.write(f"|{func_time_call}| FUNCTION NAME:{new_function.__name__}, ARGUMENTS:{args}, NAMED ARGUMENTS:{kwargs}, RETURNED VALUE:{result}\n")
                    log.close()
            except Exception as err:
                error = err
                with open(f'{path}', 'a') as log:
                    log.write(f"FAILED |{func_time_call}| FUNCTION NAME:{new_function.__name__}, ARGUMENTS:{args}, NAMED ARGUMENTS:{kwargs}, RETURNED ERROR:{error}\n")
                    log.close()
                raise error
            return result
        return new_function
    return __logger