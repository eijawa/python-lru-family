from typing import Any, Callable
from functools import partial

from datetime import datetime

from .pqueue import PriorityQueue


class LRU(object):
    def __init__(self, max_capacity: int = 10) -> None:
        self.HT: dict[Any, Any] = dict()
        self.pqueue: PriorityQueue[datetime] = PriorityQueue[datetime](reverse=True)

        self.max_capacity: int = max_capacity

    def __call__(
        self, func: Callable[..., Any]
    ) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            f = partial(func, *args, **kwargs)
            str_f = str(f)

            if str_f in self.HT:
                self.pqueue.set(str_f, datetime.now())
            else:
                self.HT[str_f] = f()
                self.pqueue.enqueue(str_f, datetime.now())

                if len(self.pqueue) > self.max_capacity:
                    hp_val, _ = self.pqueue.peek()
                    del self.HT[hp_val]

                    self.pqueue.dequeue()

            return self.HT[str_f]

        return wrapper
