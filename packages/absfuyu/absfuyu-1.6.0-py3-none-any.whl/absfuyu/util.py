#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilities Module
----------------
Some random utilities

Contain:
- toCelcius
- toFahrenheit
- unique_list
- @measure_performance
"""




# Module level
##############################################################
__all__ = [
    "toCelcius", "toFahrenheit", "unique_list",
    "measure_performance",
]





# Library
##############################################################
from functools import wraps as __wraps
import tracemalloc as __tracemalloc
from time import perf_counter as __perf_counter
from typing import Any as __Any
from typing import List as __List

from .core import Number as __Num



# Function
##############################################################
def toCelcius(
        number: __Num,
        roundup: bool = True
    ) -> __Num:
    """
    Summary
    -------
    Convert Fahrenheit to Celcius

    Parameters
    ----------
    number : Number
        F degree
    
    roundup : bool
        round the figure to .2f if True
        (default: True)

    Returns
    -------
    Number
        C degree
    """

    c_degree = (number-32)/1.8
    if roundup:
        return round(c_degree,2)
    else:
        return c_degree



def toFahrenheit(
        number: __Num,
        roundup: bool = True
    ) -> __Num:
    """
    Summary
    -------
    Convert Celcius to Fahrenheit

    Parameters
    ----------
    number : Number
        C degree
    
    roundup : bool
        round the figure to .2f if True
        (default: True)

    Returns
    -------
    Number
        F degree
    """

    f_degree = (number*1.8)+32
    if roundup:
        return round(f_degree,2)
    else:
        return f_degree



def unique_list(lst: __List[__Any]) -> __List[__Any]:
    """
    Summary
    -------
    Remove duplicate items in list

    Parameters
    ----------
    lst : list
        List that needs "cleaning"

    Returns
    -------
    list
        list that has no duplicates
    """
    return list(set(lst))


def reverse_number(number: __Num) -> __Num:
    """
    Reverse a number
    
    Parameters
    ----------
    number : int or float
        a number
    
    Returns
    -------
    A reversed number
    """
    
    # Try to convert from str to float
    if isinstance(number, str):
        try:
            number = float(number)
        except:
            raise ValueError("Must be a number")
    
    # Type: int
    if isinstance(number, int):
        return int(str(number)[::-1])
    
    # Type: float
    elif isinstance(number, float):
        if str(number).endswith(".0"): # normal number
            return int(str(str(number)[:-2])[::-1]) # remove decimals
        else:
            return float(str(number)[::-1])
    
    # Invalid number
    else:
        raise ValueError("Must be a number")

def measure_performance(func):
    r"""
    Summary
    -------
    Measure performance of a function

    Usage
    -----
    Use this as the decorator (@measure_performance)
    """
    
    @__wraps(func)
    def wrapper(*args, **kwargs):
        # Start memory measure
        __tracemalloc.start()
        # Start time measure
        start_time = __perf_counter()
        # Run function
        func(*args, **kwargs)
        # Get memory stats
        current, peak = __tracemalloc.get_traced_memory()
        # Get finished time
        finish_time = __perf_counter()
        # End memory measure
        __tracemalloc.stop()
        
        # Print output
        # print(f'{"-"*40}')
        # print(f'Function: {func.__name__}')
        # #print(f'Method: {func.__doc__}')
        # print(f"Memory usage:\t\t {current / 10**6:.6f} MB")
        # print(f"Peak memory usage:\t {peak / 10**6:.6f} MB")
        # print(f'Time elapsed (seconds):\t {finish_time - start_time:.6f}')
        # print(f'{"-"*40}')
        
        stat = {
            "Function": func.__name__,
            "Memory usage": current / 10**6,
            "Peak memory usage": peak / 10**6,
            "Time elapsed (seconds)": finish_time - start_time,
        }
        out: bool = False
        
        print(f"""
        {"-"*40}
        Function: {stat["Function"]}
        Memory usage:\t\t {stat["Memory usage"]:,.6f} MB
        Peak memory usage:\t {stat["Peak memory usage"]:,.6f} MB
        Time elapsed (seconds):\t {stat["Time elapsed (seconds)"]:,.6f}
        {"-"*40}
        """)
        
        if out:
            return stat
        
    return wrapper