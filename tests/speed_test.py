from time import time
from typing import Any, Callable

from devtools import debug

from src.lru import LRU


def test_without_cache() -> None:
    def fib_no_cache(n: int) -> int:
        if n == 1 or n == 2:
            return 1

        return fib_no_cache(n - 1) + fib_no_cache(n - 2)

    run_with_exec_time(fib_no_cache, 48)


def test_with_cache() -> None:
    @LRU()
    def fib_cache(n: int) -> int:
        if n == 1 or n == 2:
            return 1

        return fib_cache(n - 1) + fib_cache(n - 2)

    run_with_exec_time(fib_cache, 48)


def run_with_exec_time(f: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
    start_time = time()

    result = f(*args, *kwargs)

    end_time = time()

    debug("Execution time: {0:.5f}\nResult: {1}".format(end_time - start_time, result))
