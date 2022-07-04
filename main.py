import requests
import psutil
import functools
import os
from collections import OrderedDict


def cache(max_limit=64):
    def internal(f):
        @functools.wraps(f)
        def deco(*args, **kwargs):
            # В якості простої функції, ця частина працює, а в якості декоратору - чомусь ні
            cache = {}
            if args[0] in cache.keys():
                cache[args[0]] += 1
            else:
                cache.update({args[0]: 1})
            f(*args, **kwargs)
            result = OrderedDict(sorted(cache.items(), key=lambda x: x[1]))
            if len(result) > max_limit:
                result.popitem(last=False)
            return result
            ################################################################################
        return deco
    return internal


def memory_usage_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        process = psutil.Process(os.getpid())
        memory_before = process.memory_info()[0]
        my_func = func(*args, **kwargs)
        print(f'This function takes {process.memory_info()[0] - memory_before} bytes')
        return my_func
    return wrapper


@memory_usage_decorator
def fetch_url(url, first_n=100):
    """Fetch a given url"""
    res = requests.get(url)
    return res.content[:first_n] if first_n else res.content


fetch_url('https://google.com')
fetch_url('https://github.com')
fetch_url('https://reyestr.court.gov.ua')
fetch_url('https://ua.tribuna.com')
fetch_url('https://ithillel.com')
