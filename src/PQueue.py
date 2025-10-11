from heapq import heappush, heappop

class PQueue:
    def __init__(self):
        self._h = []
        self._t = 0

    def push(self, priority, item):
        heappush(self._h, (priority, self._t, item))
        self._t += 1

    def pop(self):
        return heappop(self._h)[2]

    def __bool__(self):
        return bool(self._h)