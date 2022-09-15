from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from typing import Optional

from src.singleton import Singleton

from .test import Test


class ColorTree(Enum):
    RED = "red"
    BLACK = "black"


@dataclass(init=True, repr=False, eq=True, frozen=False)
class Node:
    key: Test
    parent: Optional["Node"] = None
    left: Optional["Node"] = None
    right: Optional["Node"] = None
    color: ColorTree = ColorTree.RED


class CommandsTestTree(metaclass=Singleton):
    """Красно-черное дерево"""

    root: Optional[Node]

    def __init__(self) -> None:
        if getattr(self, "root", None) is None:
            self.root = None

    def _left_rotate(self, x: Node) -> None:
        y = x.right
        if y:
            x.right = y.left

            if y.left is not None:
                y.left.parent = x

            y.parent = x.parent
            if x.parent is None:
                self.root = y
            elif x is x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y

            y.left = x
            x.parent = y

    def _right_rotate(self, x: Node) -> None:
        y = x.left
        if y:
            x.left = y.right

            if y.right is not None:
                y.right.parent = x

            y.parent = x.parent
            if x.parent is None:
                self.root = y
            elif x is x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y

            y.right = x
            x.parent = y

    def append(self, z: Node) -> None:
        y = None
        x = self.root
        while x is not None:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right

        z.parent = y
        if y is None:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z

        self._fixup(z)

    def _fixup(self, z: Node) -> None:
        while z.parent is not None and z.parent.color == ColorTree.RED:
            self._change_tree(z)
        if self.root:
            self.root.color = ColorTree.BLACK

    def _change_tree(self, z: Node) -> None:
        if z and z.parent and z.parent.parent and z.parent is z.parent.parent.left:
            y = z.parent.parent.right
            if y is not None and y.color == ColorTree.RED:  # Первая ситуация
                z.parent.color = ColorTree.BLACK
                y.color = ColorTree.BLACK
                z.parent.parent.color = ColorTree.RED
                z = z.parent.parent
            else:
                if z and z.parent and z is z.parent.right:  # Вторая ситуация
                    z = z.parent
                    self._left_rotate(z)
                if z and z.parent and z.parent.parent:
                    z.parent.color = ColorTree.BLACK  # Третья ситуация
                    z.parent.parent.color = ColorTree.RED
                    self._right_rotate(z.parent.parent)
        else:
            if z and z.parent and z.parent.parent and z.parent is z.parent.parent.right:
                y = z.parent.parent.left
                if y is not None and y.color == ColorTree.RED:  # Четвертая ситуация
                    z.parent.color = ColorTree.BLACK
                    y.color = ColorTree.BLACK
                    z.parent.parent.color = ColorTree.RED
                    z = z.parent.parent
                else:
                    if z and z.parent and z is z.parent.left:  # Пятая ситуация
                        z = z.parent
                        self._right_rotate(z)
                    if z and z.parent and z.parent.parent:
                        z.parent.color = ColorTree.BLACK  # Шестая ситуация
                        z.parent.parent.color = ColorTree.RED
                        self._left_rotate(z.parent.parent)

    def _transplant(self, u: Node, v: Node) -> None:
        if u.parent is None:
            self.root = v
        elif u is u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    def _tree_minimum(self, x: Node) -> Node:
        while x.left is not None:
            x = x.left
        return x

    def delete(self, z: Node) -> None:
        color = z.color
        if z.left is None:
            x = z.right
            self._transplant(z, z.right)  # type: ignore
        elif z.right is None:
            x = z.left
            self._transplant(z, z.left)
        else:
            m = self._tree_minimum(z.right)
            color = m.color
            x = m.right
            if m.parent is not z:
                self._transplant(m, m.right)  # type: ignore
                m.right = z.right
                m.right.parent = m
            self._transplant(z, m)
            m.left = z.left
            m.left.parent = m
            m.color = z.color
        if x and color == ColorTree.BLACK:
            self._delete_fixup(x)

    def _change_delete(self, x: Node) -> None:
        if x and x.parent and x is x.parent.left:
            w = x.parent.right
            if w:
                if w.color == ColorTree.RED:
                    w.color = ColorTree.BLACK
                    x.parent.color = ColorTree.RED
                    self._left_rotate(x.parent)
                    w = x.parent.right
                if (
                    x
                    and w
                    and w.right
                    and w.left
                    and w.right.color == ColorTree.BLACK
                    and w.left.color == ColorTree.BLACK
                ):
                    w.color = ColorTree.RED
                    x = x.parent
                else:
                    if (
                        w
                        and w.right
                        and w.left
                        and x
                        and x.parent
                        and w.right.color == ColorTree.BLACK
                    ):
                        w.left.color = ColorTree.BLACK
                        w.color = ColorTree.RED
                        self._right_rotate(w)
                        w = x.parent.right
                    if w and x and x.parent:
                        w.color = x.parent.color
                    if x and x.parent:
                        x.parent.color = ColorTree.BLACK
                    if w and w.right:
                        w.right.color = ColorTree.BLACK
                    if x and x.parent:
                        self._left_rotate(x.parent)
                    if self.root:
                        x = self.root
        elif x and x.parent:
            w = x.parent.left
            if w:
                if w.color == ColorTree.RED:
                    w.color = ColorTree.BLACK
                    x.parent.color = ColorTree.RED
                    self._right_rotate(x.parent)
                    w = x.parent.left
                if (
                    x
                    and w
                    and w.right
                    and w.left
                    and w.right.color == ColorTree.BLACK
                    and w.left.color == ColorTree.BLACK
                ):
                    w.color = ColorTree.RED
                    x = x.parent
                else:
                    if (
                        w
                        and w.left
                        and w.right
                        and x
                        and x.parent
                        and w.left.color == ColorTree.BLACK
                    ):
                        w.right.color = ColorTree.BLACK
                        w.color = ColorTree.RED
                        self._left_rotate(w)
                        w = x.parent.left
                    if w and x and x.parent:
                        w.color = x.parent.color
                    if x and x.parent:
                        x.parent.color = ColorTree.BLACK
                    if w and w.left:
                        w.left.color = ColorTree.BLACK
                    if x and x.parent:
                        self._right_rotate(x.parent)
                    if self.root:
                        x = self.root

    def _delete_fixup(self, x: Node) -> None:
        while x is not self.root and x.color == ColorTree.BLACK:
            self._change_delete(x)
        x.color = ColorTree.BLACK

    def search(self, y: Node) -> Optional[Node]:
        x = self.root
        while x is not None and y.key != x.key:
            if y.key < x.key:
                x = x.left
            else:
                x = x.right
        return x

    @lru_cache(maxsize=None)
    def sort(self) -> list[str]:
        result: list[str] = []
        self._inorder_tree_walk(self.root, result)

        return result

    def _inorder_tree_walk(self, x: Optional[Node], result: list[str]) -> None:
        if x is not None:
            self._inorder_tree_walk(x.left, result)
            result.append(x.key.command + " - " + x.key.name)
            self._inorder_tree_walk(x.right, result)
