#!/usr/bin/env python
# -*- coding: utf-8 -*-


MOCK_CONTINUE_COMPLETION_INFO = [
    {
      "parent_id": "test_1",
      "completion": {
          "code": "test_code",
          "request_id": "001"
      },
      "ttl": 30
    },
    {
      "parent_id": "test_2",
      "completion": {
          "code": """
                def test_function():
                    print("Hello, World!")
                for i in range(5):
                    print(i)
                def bubble_sort(arr):
                    n = len(arr)
                    for i in range(n):
                        for j in range(0, n-i-1):
                            if arr[j] > arr[j+1]:
                                arr[j], arr[j+1] = arr[j+1], arr[j]
                    return arr
          """,
          "request_id": "002"
      },
      "ttl": 30
    },
    {
      "parent_id": "test_3",
      "completion": {
          "code": """
                def UnionFind(n):
                    self.parent = list(range(n))
                    self.rank = [0] * n
                    self.count = n

                def find(self, x):
                    if self.parent[x] != x:
                        self.parent[x] = self.find(self.parent[x])
                    return self.parent[x]

                def union(self, x, y):
                    root_x = self.find(x)
                    root_y = self.find(y)
                    if root_x != root_y:
                        if self.rank[root_x] < self.rank[root_y]:
                            self.parent[root_x] = root_y
                        elif self.rank[root_x] > self.rank[root_y]:
                            self.parent[root_y] = root_x
                        else:
                            self.parent[root_y] = root_x
                            self.rank[root_x] += 1
                        self.count -= 1
          """,
          "request_id": "003",
          "is_finished": True,
          "is_error": False,
          "error_message": "No error"
      },
      "ttl": 30
    },
]
