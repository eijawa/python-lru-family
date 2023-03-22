[![python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)

*Cache family*
# Last-Recently Used (LRU)
The meaning of this project is to implement LRU cache myself with types support, without ex-standard python library. For priority queue I implemented Linked List version.

An LRU is a *decorator* class.

Evaluation time T (in seconds) based on calculation of Fibonacci Sequence:

| Number | T without cache | T with cache |
|--------|:---------------:|-------------:|
|   32   |      0.28653    |   0.01014    |
|   42   |     33.25495    |   0.02694    |
|   48   |    581.86346    |   0.03312    |

Keep in mind, this values calculated with default size of LRU memory = 10.

## How to convert it into Most Recently Used (MRU)
Convertion to MRU require only changes in `LRU` class.
```python
- self.pqueue: PriorityQueue[datetime] = PriorityQueue[datetime](reverse=True)
+ self.pqueue: PriorityQueue[datetime] = PriorityQueue[datetime]()
```
Simple, right?

## How to convert it into Least-Frequently Used (LFU)
>**Important**<br>In order to make this code easily changeable to support different types of *priority* in `PriorityNode`, I let `peek` method return node's value and priority.

Convertion to LFU require only changes in `LRU` class.
```python
- self.pqueue: PriorityQueue[datetime] = PriorityQueue[datetime](reverse=True)
+ self.pqueue: PriorityQueue[int] = PriorityQueue[int](reverse=True)


  if str_f in self.HT:
-     self.pqueue.set(str_f, datetime.now())
+     _, p = self.pqueue.peek()
+     self.pqueue.set(str_f, p + 1)
  else:
      self.HT[str_f] = f()
  
-     self.pqueue.enqueue(str_f, datetime.now())
+     self.pqueue.enqueue(str_f, 1)
  
      if len(self.pqueue) > self.max_capacity:
          hp_val, _ = self.pqueue.peek()
          del self.HT[hp_val]
  
          self.pqueue.dequeue()
          
  return self.HT[str_f]
```
Maybe it's not optimal, but it's straightforward enought.
