import heapq

class BinaryHeap:
    def __init__(self):
        self.heap = []
        self._counter = 0

    def push(self, heuristic, board):
        heapq.heappush(self.heap, (heuristic, self._counter, board))
        self._counter += 1

    def pop(self):
        if not self.heap:
            return None
        h, _, board = heapq.heappop(self.heap)
        return (h, board)

    def __len__(self):
        return len(self.heap)