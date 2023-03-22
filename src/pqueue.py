from __future__ import annotations

import operator
from typing import TYPE_CHECKING, Any, Generic, Self, TypeVar

if TYPE_CHECKING:
    # I don't know if I'm right...
    # It seems close to the truth...

    # https://peps.python.org/pep-0544/#self-types-in-protocols

    from typing import Protocol

    from _typeshed import (
        SupportsDunderGE,
        SupportsDunderGT,
        SupportsDunderLE,
        SupportsDunderLT,
    )

    class _SupportPredicates(
        SupportsDunderGE[Any],
        SupportsDunderGT[Any],
        SupportsDunderLE[Any],
        SupportsDunderLT[Any],
        Protocol,
    ):
        ...

    _PriorityType = TypeVar("_PriorityType", bound=_SupportPredicates)
else:
    _PriorityType = TypeVar("_PriorityType")


class PriorityNode(Generic[_PriorityType]):
    def __init__(
        self,
        val: Any,
        priority: _PriorityType,
        next: Self | None = None,
    ) -> None:
        self.val = val
        self.priority = priority
        self.next: Self | None = next

    def __str__(self) -> str:
        return f"({self.val!s}, {self.priority})"


class PriorityQueue(Generic[_PriorityType]):
    def __init__(self, reverse: bool = False) -> None:
        self.__head: PriorityNode[_PriorityType] | None = None

        self.__len: int = 0

        # If reverse is True -> Ascending order (low priority -> high priority)
        # else -> Descending order (high priority -> low priority) !DEFAULT
        # t_operator means (less|greater) then
        # e_operator means (less|greater)equal then
        if reverse:
            self.__t_operator = operator.gt
            self.__e_operator = operator.ge
        else:
            self.__t_operator = operator.lt
            self.__e_operator = operator.le

    def enqueue(self, val: Any, priority: _PriorityType) -> None:
        """Add value to the queue, based on priority"""

        n = PriorityNode(val, priority)

        if self.empty():
            self.__head = n
        else:
            if self.__t_operator(self.__head.priority, priority):
                n.next = self.__head
                self.__head = n
            else:
                ptr = self.__head

                while ptr.next:
                    if self.__e_operator(ptr.next.priority, priority):
                        break

                    ptr = ptr.next

                n.next = ptr.next
                ptr.next = n

        self.__len += 1

    def dequeue(self) -> None:
        """Remove value from head"""

        if self.empty():
            return None

        if self.__head.next is not None:
            self.__head = self.__head.next
        else:
            self.__head = None

        self.__len -= 1

    def peek(self) -> tuple[Any, _PriorityType] | tuple[None, None]:
        """Return element from head"""

        if self.empty():
            return None, None

        return self.__head.val, self.__head.priority

    def set(self, val: Any, priority: _PriorityType) -> None:
        """Set new priority value for node in queue"""

        # Algo can be optimized by memory
        # if we will re-enqueue not (val, priority), but Node itself

        _del = self.__head

        while _del and _del.val != val:
            _del = _del.next

        if _del is None:
            raise ValueError

        if self.__head == _del:
            self.__head = self.__head.next
        else:
            ptr = self.__head

            while ptr.next != _del:
                ptr = ptr.next

            ptr.next = _del.next

        self.enqueue(val, priority)

    def empty(self) -> bool:
        return self.__head is None

    def show(self) -> None:
        ptr = self.__head

        while ptr.next:
            print(ptr, end=" -> ")
            ptr = ptr.next
        print(ptr)

    def __len__(self) -> int:
        return self.__len
