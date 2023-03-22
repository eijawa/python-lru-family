import pytest

from src.pqueue import PriorityQueue

values_with_priority_list = [
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 8),
    (8, 9),
    (9, 10),
]


@pytest.fixture
def queue() -> PriorityQueue[int]:
    return PriorityQueue[int]()


@pytest.fixture
def filled_queue(queue: PriorityQueue[int]) -> PriorityQueue[int]:
    for v, p in values_with_priority_list:
        queue.enqueue(v, p)

    return queue


def test_enqueue(queue: PriorityQueue[int]) -> None:
    for v, p in values_with_priority_list:
        queue.enqueue(v, p)

        assert queue.peek()[0] == v


def test_dequeue_with_filled(filled_queue: PriorityQueue[int]) -> None:
    filled_queue.dequeue()

    assert filled_queue.peek()[0] == values_with_priority_list[-2][0]


def test_set_with_existed_value(filled_queue: PriorityQueue[int]) -> None:
    filled_queue.set(1, 24)

    assert filled_queue.peek()[0] == 1


def test_set_with_non_existed_value(filled_queue: PriorityQueue[int]) -> None:
    with pytest.raises(ValueError):
        filled_queue.set(24, 1)
