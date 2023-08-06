import re
from typing import TypeVar, Union
from  functools import wraps
import pandas as pd

F = TypeVar('F')

def timer(func):
    """ func taste times(second) decorator
        @functools.wraps : wrapper.__name__ = func.__name__
    """
    def wrapper(*args, **kwargs):
        from time import perf_counter
        time_start = perf_counter()
        result = func(*args, **kwargs)
        time_end = perf_counter()
        spend_time =  time_end - time_start
        print(f" Cost time:  {spend_time:.4f} S")
        return result
    return wrapper
  

def to_numeric(func: F) -> F:
    """ dataframe / series to numeric"""
    ignore = ["ts_code",'index_code','index_symbol','symbol','code',"ID",'name', 'level','name_level']
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        values = func(*args,**kwargs)
        if isinstance(values, pd.DataFrame):
            for column in values.columns:
                if column not in ignore:
                    values[column] = values[column].apply(convert)
        elif isinstance(values, pd.Series):
            for index in values.index:
                if index not in ignore:
                    values[index] =convert(values[index])
        return values
    
    def convert(o:Union[str, int, float]) -> Union[str, int, float]:
        if not re.findall('\d', str(o)):
            return o
        try:
            o = int(o) if str(o).isalnum() else float(o)
        except Exception:
            pass
        return o

    return wrapper
        