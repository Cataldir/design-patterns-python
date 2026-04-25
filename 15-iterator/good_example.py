# good_example.py - Iterator pattern with generators and the iterator protocol
from __future__ import annotations

from collections import deque
from collections.abc import Iterator


class TreeNode:
    def __init__(
        self, value: int, children: list["TreeNode"] | None = None
    ) -> None:
        self.value = value
        self.children = children or []

    def __iter__(self) -> Iterator[int]:
        """Depth-first pre-order traversal."""
        yield self.value
        for child in self.children:
            yield from child

    def bfs(self) -> Iterator[int]:
        """Breadth-first level-order traversal."""
        queue: deque[TreeNode] = deque([self])
        while queue:
            node = queue.popleft()
            yield node.value
            queue.extend(node.children)


if __name__ == "__main__":
    root = TreeNode(1, [
        TreeNode(2, [TreeNode(4), TreeNode(5)]),
        TreeNode(3),
    ])
    print(list(root))
    print(list(root.bfs()))
    print(sum(root))
