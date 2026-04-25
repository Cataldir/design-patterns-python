# test_iterator.py - pytest verifying traversal orders and protocol compliance
from __future__ import annotations

import pytest

from good_example import TreeNode


@pytest.fixture
def tree_root() -> TreeNode:
    return TreeNode(1, [
        TreeNode(2, [TreeNode(4), TreeNode(5)]),
        TreeNode(3),
    ])


class TestDepthFirst:
    def test_dfs_produces_pre_order_sequence(
        self, tree_root: TreeNode
    ) -> None:
        assert list(tree_root) == [1, 2, 4, 5, 3]

    def test_sum_uses_iterator_protocol(
        self, tree_root: TreeNode
    ) -> None:
        assert sum(tree_root) == 15

    def test_single_node_yields_itself(self) -> None:
        leaf = TreeNode(42)
        assert list(leaf) == [42]


class TestBreadthFirst:
    def test_bfs_produces_level_order_sequence(
        self, tree_root: TreeNode
    ) -> None:
        assert list(tree_root.bfs()) == [1, 2, 3, 4, 5]

    def test_bfs_single_node(self) -> None:
        leaf = TreeNode(7)
        assert list(leaf.bfs()) == [7]


class TestStopIteration:
    def test_exhausted_iterator_raises_stop_iteration(
        self, tree_root: TreeNode
    ) -> None:
        it = iter(tree_root)
        for _ in it:
            pass
        with pytest.raises(StopIteration):
            next(it)


class TestMultipleIterations:
    def test_iter_returns_fresh_generator_each_time(
        self, tree_root: TreeNode
    ) -> None:
        first = list(tree_root)
        second = list(tree_root)
        assert first == second == [1, 2, 4, 5, 3]
