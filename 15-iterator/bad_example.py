# bad_example.py - Client code coupled to tree internals for traversal
from __future__ import annotations

from collections import deque


class TreeNode:
    def __init__(
        self, value: int, children: list["TreeNode"] | None = None
    ) -> None:
        self.value = value
        self.children = children or []


def collect_values_dfs(root: TreeNode) -> list[int]:
    result: list[int] = []
    stack: list[TreeNode] = [root]
    while stack:
        node = stack.pop()
        result.append(node.value)
        for child in reversed(node.children):
            stack.append(child)
    return result


def collect_values_bfs(root: TreeNode) -> list[int]:
    result: list[int] = []
    queue: deque[TreeNode] = deque([root])
    while queue:
        node = queue.popleft()
        result.append(node.value)
        for child in node.children:
            queue.append(child)
    return result


if __name__ == "__main__":
    root = TreeNode(1, [
        TreeNode(2, [TreeNode(4), TreeNode(5)]),
        TreeNode(3),
    ])
    print(collect_values_dfs(root))
    print(collect_values_bfs(root))
