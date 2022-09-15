from unittest.mock import Mock, patch

from pytest import Config

from src.test import Test
from src.tree import ColorTree, CommandsTestTree, Node


class TestLeftRotate:
    def test_if_x_does_not_have_parent(self, patch_singleton: Config) -> None:
        a = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        b = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        c = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        y = Node(
            parent=None,
            left=b,
            right=c,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        x = Node(
            parent=None,
            left=a,
            right=y,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        a.parent = x
        b.parent = y
        c.parent = y
        y.parent = x

        CommandsTestTree()._left_rotate(x)

        assert a.parent is x
        assert b.parent is x
        assert x.parent is y
        assert c.parent is y
        assert y.parent is None

        assert a.left is None
        assert b.left is None
        assert x.left is a
        assert c.left is None
        assert y.left is x

        assert a.right is None
        assert b.right is None
        assert x.right is b
        assert c.right is None
        assert y.right is c

    def test_if_x_is_left_node_of_parent(self, patch_singleton: Config) -> None:
        a = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        b = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        c = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        y = Node(
            parent=None,
            left=b,
            right=c,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        x = Node(
            parent=None,
            left=a,
            right=y,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        d = Node(
            parent=None,
            left=x,
            right=None,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )

        a.parent = x
        b.parent = y
        c.parent = y
        y.parent = x
        x.parent = d

        CommandsTestTree()._left_rotate(x)

        assert a.parent is x
        assert b.parent is x
        assert x.parent is y
        assert c.parent is y
        assert y.parent is d
        assert d.parent is None

        assert a.left is None
        assert b.left is None
        assert x.left is a
        assert c.left is None
        assert y.left is x
        assert d.left is y

        assert a.right is None
        assert b.right is None
        assert x.right is b
        assert c.right is None
        assert y.right is c
        assert d.right is None

    def test_if_x_is_right_node_of_parent(self, patch_singleton: Config) -> None:
        a = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        b = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        c = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        y = Node(
            parent=None,
            left=b,
            right=c,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        x = Node(
            parent=None,
            left=a,
            right=y,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        d = Node(
            parent=None,
            left=None,
            right=x,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )

        a.parent = x
        b.parent = y
        c.parent = y
        y.parent = x
        x.parent = d

        CommandsTestTree()._left_rotate(x)

        assert a.parent is x
        assert b.parent is x
        assert x.parent is y
        assert c.parent is y
        assert y.parent is d
        assert d.parent is None

        assert a.left is None
        assert b.left is None
        assert x.left is a
        assert c.left is None
        assert y.left is x
        assert d.left is None

        assert a.right is None
        assert b.right is None
        assert x.right is b
        assert c.right is None
        assert y.right is c
        assert d.right is y

    def test_if_y_does_not_have_left_node(self, patch_singleton: Config) -> None:
        b = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        c = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        y = Node(
            parent=None,
            left=b,
            right=c,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        x = Node(
            parent=None,
            left=None,
            right=y,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )

        b.parent = y
        c.parent = y
        y.parent = x
        x.parent = None

        CommandsTestTree()._left_rotate(x)

        assert b.parent is x
        assert x.parent is y
        assert c.parent is y
        assert y.parent is None

        assert b.left is None
        assert x.left is None
        assert c.left is None
        assert y.left is x

        assert b.right is None
        assert x.right is b
        assert c.right is None
        assert y.right is c


class TestRightRotate:
    def test_if_x_does_not_have_parent(self, patch_singleton: Config) -> None:
        a = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        b = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        c = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        y = Node(
            parent=None,
            left=b,
            right=c,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        x = Node(
            parent=None,
            left=y,
            right=a,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )

        a.parent = x
        b.parent = y
        c.parent = y
        y.parent = x

        CommandsTestTree()._right_rotate(x)

        assert a.parent is x
        assert b.parent is y
        assert x.parent is y
        assert c.parent is x
        assert y.parent is None

        assert a.left is None
        assert b.left is None
        assert x.left is c
        assert c.left is None
        assert y.left is b

        assert a.right is None
        assert b.right is None
        assert x.right is a
        assert c.right is None
        assert y.right is x

    def test_if_x_is_left_node_of_parent(self, patch_singleton: Config) -> None:
        a = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        b = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        c = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        y = Node(
            parent=None,
            left=b,
            right=c,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        x = Node(
            parent=None,
            left=y,
            right=a,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        d = Node(
            parent=None,
            left=x,
            right=None,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )

        a.parent = x
        b.parent = y
        c.parent = y
        y.parent = x
        x.parent = d

        CommandsTestTree()._right_rotate(x)

        assert a.parent is x
        assert b.parent is y
        assert x.parent is y
        assert c.parent is x
        assert y.parent is d
        assert d.parent is None

        assert a.left is None
        assert b.left is None
        assert x.left is c
        assert c.left is None
        assert y.left is b
        assert d.left is y

        assert a.right is None
        assert b.right is None
        assert x.right is a
        assert c.right is None
        assert y.right is x
        assert d.right is None

    def test_if_x_is_right_node_of_parent(self, patch_singleton: Config) -> None:
        a = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        b = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        c = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        y = Node(
            parent=None,
            left=b,
            right=c,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        x = Node(
            parent=None,
            left=y,
            right=a,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        d = Node(
            parent=None,
            left=None,
            right=x,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )

        a.parent = x
        b.parent = y
        c.parent = y
        y.parent = x
        x.parent = d

        CommandsTestTree()._right_rotate(x)

        assert a.parent is x
        assert b.parent is y
        assert x.parent is y
        assert c.parent is x
        assert y.parent is d
        assert d.parent is None

        assert a.left is None
        assert b.left is None
        assert x.left is c
        assert c.left is None
        assert y.left is b
        assert d.left is None

        assert a.right is None
        assert b.right is None
        assert x.right is a
        assert c.right is None
        assert y.right is x
        assert d.right is y

    def test_if_y_does_not_have_left_node(self, patch_singleton: Config) -> None:
        b = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        c = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        y = Node(
            parent=None,
            left=b,
            right=c,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        x = Node(
            parent=None,
            left=y,
            right=None,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )

        b.parent = y
        c.parent = y
        y.parent = x

        CommandsTestTree()._right_rotate(x)

        assert b.parent is y
        assert x.parent is y
        assert c.parent is x
        assert y.parent is None

        assert b.left is None
        assert x.left is c
        assert c.left is None
        assert y.left is b

        assert b.right is None
        assert x.right is None
        assert c.right is None
        assert y.right is x


@patch("src.tree.CommandsTestTree._fixup")
class TestAppend:
    def test_if_z_less_than_x(self, mock_fixup: Mock, patch_singleton: Config) -> None:
        x = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("b", "", None, [], None),
        )
        z = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )

        tree = CommandsTestTree()
        tree.root = x
        tree.append(z)

        assert x.parent is None
        assert z.parent is x

        assert x.left is z
        assert z.left is None

        assert x.right is None
        assert z.right is None

        mock_fixup.assert_called_once_with(z)

    def test_if_z_greater_than_x(
        self, mock_fixup: Mock, patch_singleton: Config
    ) -> None:
        x = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("b", "", None, [], None),
        )
        z = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("c", "", None, [], None),
        )

        tree = CommandsTestTree()
        tree.root = x
        tree.append(z)

        assert x.parent is None
        assert z.parent is x

        assert x.left is None
        assert z.left is None

        assert x.right is z
        assert z.right is None

        mock_fixup.assert_called_once_with(z)

    def test_if_x_equals_z(self, mock_fixup: Mock, patch_singleton: Config) -> None:
        x = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("b", "", None, [], None),
        )
        z = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("b", "", None, [], None),
        )

        tree = CommandsTestTree()
        tree.root = x
        tree.append(z)

        assert x.parent is None
        assert z.parent is x

        assert x.left is None
        assert z.left is None

        assert x.right is z
        assert z.right is None

        mock_fixup.assert_called_once_with(z)

    def test_if_tree_is_empty(self, mock_fixup: Mock, patch_singleton: Config) -> None:
        z = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("b", "", None, [], None),
        )

        tree = CommandsTestTree()
        tree.append(z)

        assert tree.root is z
        assert z.parent is None
        assert z.left is None
        assert z.right is None

        mock_fixup.assert_called_once_with(z)


class TestChangeTree:
    def test_first_situation(self, patch_singleton: Config) -> None:
        a = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("d", "", None, [], None),
        )
        b = Node(
            parent=None,
            left=a,
            right=None,
            color=ColorTree.RED,
            key=Test("e", "", None, [], None),
        )
        c = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("h", "", None, [], None),
        )
        d = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.BLACK,
            key=Test("a", "", None, [], None),
        )
        e = Node(
            parent=None,
            left=b,
            right=c,
            color=ColorTree.BLACK,
            key=Test("g", "", None, [], None),
        )
        f = Node(
            parent=None,
            left=d,
            right=e,
            color=ColorTree.RED,
            key=Test("b", "", None, [], None),
        )
        h = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("o", "", None, [], None),
        )
        g = Node(
            parent=None,
            left=None,
            right=h,
            color=ColorTree.BLACK,
            key=Test("n", "", None, [], None),
        )
        x = Node(
            parent=None,
            left=f,
            right=g,
            color=ColorTree.BLACK,
            key=Test("k", "", None, [], None),
        )

        a.parent = b
        b.parent = e
        c.parent = e
        d.parent = f
        e.parent = f
        f.parent = x
        g.parent = x
        h.parent = g

        tree = CommandsTestTree()
        tree.root = x
        tree._change_tree(a)

        assert a.parent is b
        assert b.parent is e
        assert c.parent is e
        assert d.parent is f
        assert e.parent is f
        assert f.parent is x
        assert g.parent is x
        assert h.parent is g
        assert x.parent is None

        assert a.left is None
        assert b.left is a
        assert c.left is None
        assert d.left is None
        assert e.left is b
        assert f.left is d
        assert h.left is None
        assert g.left is None
        assert x.left is f

        assert a.right is None
        assert b.right is None
        assert c.right is None
        assert d.right is None
        assert e.right is c
        assert f.right is e
        assert h.right is None
        assert g.right is h
        assert x.right is g

        assert a.color.value == "red"
        assert b.color.value == "black"
        assert c.color.value == "black"
        assert d.color.value == "black"
        assert e.color.value == "red"
        assert f.color.value == "red"
        assert h.color.value == "red"
        assert g.color.value == "black"
        assert x.color.value == "black"

    def test_second_situation(self, patch_singleton: Config) -> None:
        a = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("d", "", None, [], None),
        )
        b = Node(
            parent=None,
            left=a,
            right=None,
            color=ColorTree.BLACK,
            key=Test("e", "", None, [], None),
        )
        c = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.BLACK,
            key=Test("h", "", None, [], None),
        )
        d = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.BLACK,
            key=Test("a", "", None, [], None),
        )
        e = Node(
            parent=None,
            left=b,
            right=c,
            color=ColorTree.RED,
            key=Test("g", "", None, [], None),
        )
        f = Node(
            parent=None,
            left=d,
            right=e,
            color=ColorTree.RED,
            key=Test("b", "", None, [], None),
        )
        h = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("o", "", None, [], None),
        )
        g = Node(
            parent=None,
            left=None,
            right=h,
            color=ColorTree.BLACK,
            key=Test("n", "", None, [], None),
        )
        x = Node(
            parent=None,
            left=f,
            right=g,
            color=ColorTree.BLACK,
            key=Test("k", "", None, [], None),
        )

        a.parent = b
        b.parent = e
        c.parent = e
        d.parent = f
        e.parent = f
        f.parent = x
        g.parent = x
        h.parent = g

        tree = CommandsTestTree()
        tree.root = x
        left_rotate = tree._left_rotate
        with patch("src.tree.CommandsTestTree._left_rotate") as mock_left_rotate:

            def _mock_left_rotate(z: Node) -> None:
                left_rotate(z)

                assert a.parent is b
                assert b.parent is f
                assert c.parent is e
                assert d.parent is f
                assert e.parent is x
                assert f.parent is e
                assert g.parent is x
                assert h.parent is g
                assert x.parent is None

                assert a.left is None
                assert b.left is a
                assert c.left is None
                assert d.left is None
                assert e.left is f
                assert f.left is d
                assert h.left is None
                assert g.left is None
                assert x.left is e

                assert a.right is None
                assert b.right is None
                assert c.right is None
                assert d.right is None
                assert e.right is c
                assert f.right is b
                assert h.right is None
                assert g.right is h
                assert x.right is g

                assert a.color.value == "red"
                assert b.color.value == "black"
                assert c.color.value == "black"
                assert d.color.value == "black"
                assert e.color.value == "red"
                assert f.color.value == "red"
                assert h.color.value == "red"
                assert g.color.value == "black"
                assert x.color.value == "black"

            mock_left_rotate.side_effect = _mock_left_rotate
            tree._change_tree(e)

    def test_third_situation(self, patch_singleton: Config) -> None:
        a = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("d", "", None, [], None),
        )
        b = Node(
            parent=None,
            left=a,
            right=None,
            color=ColorTree.BLACK,
            key=Test("e", "", None, [], None),
        )
        c = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.BLACK,
            key=Test("h", "", None, [], None),
        )
        d = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.BLACK,
            key=Test("a", "", None, [], None),
        )
        f = Node(
            parent=None,
            left=d,
            right=b,
            color=ColorTree.RED,
            key=Test("b", "", None, [], None),
        )
        e = Node(
            parent=None,
            left=f,
            right=c,
            color=ColorTree.RED,
            key=Test("g", "", None, [], None),
        )
        h = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("o", "", None, [], None),
        )
        g = Node(
            parent=None,
            left=None,
            right=h,
            color=ColorTree.BLACK,
            key=Test("n", "", None, [], None),
        )
        x = Node(
            parent=None,
            left=e,
            right=g,
            color=ColorTree.BLACK,
            key=Test("k", "", None, [], None),
        )

        a.parent = b
        b.parent = f
        c.parent = e
        d.parent = f
        e.parent = x
        f.parent = e
        g.parent = x
        h.parent = g

        tree = CommandsTestTree()
        tree.root = x
        tree._change_tree(f)

        assert a.parent is b
        assert b.parent is f
        assert c.parent is x
        assert d.parent is f
        assert e.parent is None
        assert f.parent is e
        assert g.parent is x
        assert h.parent is g
        assert x.parent is e

        assert a.left is None
        assert b.left is a
        assert c.left is None
        assert d.left is None
        assert e.left is f
        assert f.left is d
        assert h.left is None
        assert g.left is None
        assert x.left is c

        assert a.right is None
        assert b.right is None
        assert c.right is None
        assert d.right is None
        assert e.right is x
        assert f.right is b
        assert h.right is None
        assert g.right is h
        assert x.right is g

        assert a.color.value == "red"
        assert b.color.value == "black"
        assert c.color.value == "black"
        assert d.color.value == "black"
        assert e.color.value == "black"
        assert f.color.value == "red"
        assert h.color.value == "red"
        assert g.color.value == "black"
        assert x.color.value == "red"

    def test_fourth_situation(self, patch_singleton: Config) -> None:
        a = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("q", "", None, [], None),
        )
        b = Node(
            parent=None,
            left=None,
            right=a,
            color=ColorTree.RED,
            key=Test("p", "", None, [], None),
        )
        c = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("l", "", None, [], None),
        )
        d = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.BLACK,
            key=Test("s", "", None, [], None),
        )
        e = Node(
            parent=None,
            left=c,
            right=b,
            color=ColorTree.BLACK,
            key=Test("o", "", None, [], None),
        )
        f = Node(
            parent=None,
            left=e,
            right=d,
            color=ColorTree.RED,
            key=Test("r", "", None, [], None),
        )
        h = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("g", "", None, [], None),
        )
        g = Node(
            parent=None,
            left=h,
            right=None,
            color=ColorTree.BLACK,
            key=Test("h", "", None, [], None),
        )
        x = Node(
            parent=None,
            left=g,
            right=f,
            color=ColorTree.BLACK,
            key=Test("k", "", None, [], None),
        )

        a.parent = b
        b.parent = e
        c.parent = e
        d.parent = f
        e.parent = f
        f.parent = x
        g.parent = x
        h.parent = g

        tree = CommandsTestTree()
        tree.root = x
        tree._change_tree(a)

        assert a.parent is b
        assert b.parent is e
        assert c.parent is e
        assert d.parent is f
        assert e.parent is f
        assert f.parent is x
        assert g.parent is x
        assert h.parent is g
        assert x.parent is None

        assert a.left is None
        assert b.left is None
        assert c.left is None
        assert d.left is None
        assert e.left is c
        assert f.left is e
        assert h.left is None
        assert g.left is h
        assert x.left is g

        assert a.right is None
        assert b.right is a
        assert c.right is None
        assert d.right is None
        assert e.right is b
        assert f.right is d
        assert h.right is None
        assert g.right is None
        assert x.right is f

        assert a.color.value == "red"
        assert b.color.value == "black"
        assert c.color.value == "black"
        assert d.color.value == "black"
        assert e.color.value == "red"
        assert f.color.value == "red"
        assert h.color.value == "red"
        assert g.color.value == "black"
        assert x.color.value == "black"

    def test_fifth_situation(self, patch_singleton: Mock) -> None:
        a = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("q", "", None, [], None),
        )
        b = Node(
            parent=None,
            left=None,
            right=a,
            color=ColorTree.BLACK,
            key=Test("p", "", None, [], None),
        )
        c = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.BLACK,
            key=Test("l", "", None, [], None),
        )
        d = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.BLACK,
            key=Test("s", "", None, [], None),
        )
        e = Node(
            parent=None,
            left=c,
            right=b,
            color=ColorTree.RED,
            key=Test("o", "", None, [], None),
        )
        f = Node(
            parent=None,
            left=e,
            right=d,
            color=ColorTree.RED,
            key=Test("r", "", None, [], None),
        )
        h = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("g", "", None, [], None),
        )
        g = Node(
            parent=None,
            left=h,
            right=None,
            color=ColorTree.BLACK,
            key=Test("h", "", None, [], None),
        )
        x = Node(
            parent=None,
            left=g,
            right=f,
            color=ColorTree.BLACK,
            key=Test("k", "", None, [], None),
        )

        a.parent = b
        b.parent = e
        c.parent = e
        d.parent = f
        e.parent = f
        f.parent = x
        g.parent = x
        h.parent = g

        tree = CommandsTestTree()
        tree.root = x
        right_rotate = tree._right_rotate
        with patch("src.tree.CommandsTestTree._right_rotate") as mock_right_rotate:

            def _mock_right_rotate(z: Node) -> None:
                right_rotate(z)

                assert a.parent is b
                assert b.parent is f
                assert c.parent is e
                assert d.parent is f
                assert e.parent is x
                assert f.parent is e
                assert g.parent is x
                assert h.parent is g
                assert x.parent is None

                assert a.left is None
                assert b.left is None
                assert c.left is None
                assert d.left is None
                assert e.left is c
                assert f.right is d
                assert h.left is None
                assert g.left is h
                assert x.left is g

                assert a.right is None
                assert b.right is a
                assert c.right is None
                assert d.right is None
                assert e.right is f
                assert f.right is d
                assert h.right is None
                assert g.right is None
                assert x.right is e

                assert a.color.value == "red"
                assert b.color.value == "black"
                assert c.color.value == "black"
                assert d.color.value == "black"
                assert e.color.value == "red"
                assert f.color.value == "red"
                assert h.color.value == "red"
                assert g.color.value == "black"
                assert x.color.value == "black"

            mock_right_rotate.side_effect = _mock_right_rotate
            tree._change_tree(e)

    def test_sixth_situation(self, patch_singleton: Config) -> None:
        a = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("q", "", None, [], None),
        )
        b = Node(
            parent=None,
            left=None,
            right=a,
            color=ColorTree.BLACK,
            key=Test("p", "", None, [], None),
        )
        c = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.BLACK,
            key=Test("l", "", None, [], None),
        )
        d = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.BLACK,
            key=Test("s", "", None, [], None),
        )
        f = Node(
            parent=None,
            left=b,
            right=d,
            color=ColorTree.RED,
            key=Test("r", "", None, [], None),
        )
        e = Node(
            parent=None,
            left=c,
            right=f,
            color=ColorTree.BLACK,
            key=Test("o", "", None, [], None),
        )
        h = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("g", "", None, [], None),
        )
        g = Node(
            parent=None,
            left=h,
            right=None,
            color=ColorTree.BLACK,
            key=Test("h", "", None, [], None),
        )
        x = Node(
            parent=None,
            left=g,
            right=e,
            color=ColorTree.BLACK,
            key=Test("k", "", None, [], None),
        )

        a.parent = b
        b.parent = f
        c.parent = e
        d.parent = f
        e.parent = x
        f.parent = e
        g.parent = x
        h.parent = g

        tree = CommandsTestTree()
        tree.root = x
        tree._change_tree(f)

        assert a.parent is b
        assert b.parent is f
        assert c.parent is x
        assert d.parent is f
        assert e.parent is None
        assert f.parent is e
        assert g.parent is x
        assert h.parent is g
        assert x.parent is e

        assert a.left is None
        assert b.left is None
        assert c.left is None
        assert d.left is None
        assert e.left is x
        assert f.left is b
        assert h.left is None
        assert g.left is h
        assert x.left is g

        assert a.right is None
        assert b.right is a
        assert c.right is None
        assert d.right is None
        assert e.right is f
        assert f.right is d
        assert h.right is None
        assert g.right is None
        assert x.right is c

        assert a.color.value == "red"
        assert b.color.value == "black"
        assert c.color.value == "black"
        assert d.color.value == "black"
        assert e.color.value == "black"
        assert f.color.value == "red"
        assert h.color.value == "red"
        assert g.color.value == "black"
        assert x.color.value == "red"

    def test_right_uncle_is_None(self, patch_singleton: Config) -> None:
        a = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.BLACK,
            key=Test("k", "", None, [], None),
        )
        b = Node(
            parent=None,
            left=None,
            right=a,
            color=ColorTree.RED,
            key=Test("l", "", None, [], None),
        )
        x = Node(
            parent=None,
            left=None,
            right=b,
            color=ColorTree.RED,
            key=Test("m", "", None, [], None),
        )

        a.parent = b
        b.parent = x

        tree = CommandsTestTree()
        tree.root = x
        tree._change_tree(a)

    def test_left_uncle_is_None(self, patch_singleton: Config) -> None:
        a = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.BLACK,
            key=Test("k", "", None, [], None),
        )
        b = Node(
            parent=None,
            left=a,
            right=None,
            color=ColorTree.RED,
            key=Test("h", "", None, [], None),
        )
        x = Node(
            parent=None,
            left=b,
            right=None,
            color=ColorTree.RED,
            key=Test("g", "", None, [], None),
        )

        a.parent = b
        b.parent = x

        tree = CommandsTestTree()
        tree.root = x
        tree._change_tree(a)


class TestFixup:
    def test_if_node_is_root(self, patch_singleton: Config) -> None:
        x = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("k", "", None, [], None),
        )
        tree = CommandsTestTree()
        tree.root = x
        tree._fixup(x)

        assert x.parent is None
        assert x.left is None
        assert x.right is None
        assert x.color.value == "black"

    def test_node_parent_is_black(self, patch_singleton: Config) -> None:
        a = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("d", "", None, [], None),
        )
        x = Node(
            parent=None,
            left=a,
            right=None,
            color=ColorTree.BLACK,
            key=Test("k", "", None, [], None),
        )
        a.parent = x

        tree = CommandsTestTree()
        tree.root = x
        tree._fixup(a)

        assert x.parent is None
        assert a.parent

        assert x.left is a
        assert a.left is None

        assert x.right is None
        assert a.right is None

        assert x.color.value == "black"
        assert a.color.value == "red"

    def test_while_statement_is_true(self, patch_singleton: Config) -> None:
        a = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("i", "", None, [], None),
        )
        b = Node(
            parent=None,
            left=a,
            right=None,
            color=ColorTree.RED,
            key=Test("j", "", None, [], None),
        )
        x = Node(
            parent=None,
            left=b,
            right=None,
            color=ColorTree.BLACK,
            key=Test("k", "", None, [], None),
        )
        a.parent = b
        b.parent = x

        tree = CommandsTestTree()
        tree.root = x

        change_tree = tree._change_tree

        with patch("src.tree.CommandsTestTree._change_tree") as mock_change_tree:
            mock_change_tree.side_effect = change_tree
            tree._fixup(a)
            mock_change_tree.assert_called_once_with(a)


class TestSearch:
    def test_root_is_None(self, patch_singleton: Config) -> None:
        assert CommandsTestTree().search(Node(Test("b", "", None, [], None))) is None

    def test_y_equals_x(self, patch_singleton: Config) -> None:
        x = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("e", "", None, [], None),
        )

        tree = CommandsTestTree()
        tree.root = x

        assert tree.search(Node(Test("e", "", None, [], None))) == x

    def test_y_less_than_x_key(self, patch_singleton: Config) -> None:
        y = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("c", "", None, [], None),
        )
        x = Node(
            parent=None,
            left=y,
            right=None,
            color=ColorTree.RED,
            key=Test("e", "", None, [], None),
        )
        y.parent = x

        tree = CommandsTestTree()
        tree.root = x

        assert tree.search(Node(Test("c", "", None, [], None))) == y

    def test_y_greater_than_x_key(self, patch_singleton: Config) -> None:
        y = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("g", "", None, [], None),
        )
        x = Node(
            parent=None,
            left=None,
            right=y,
            color=ColorTree.RED,
            key=Test("e", "", None, [], None),
        )
        y.parent = x

        tree = CommandsTestTree()
        tree.root = x

        assert tree.search(Node(Test("g", "", None, [], None))) == y


@patch("src.tree.CommandsTestTree._inorder_tree_walk")
class TestSort:
    def test_sort(self, mock_inorder_tree_walk: Mock, patch_singleton: Config) -> None:
        x = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )

        tree = CommandsTestTree()
        tree.root = x
        tree.sort()

        mock_inorder_tree_walk.assert_called_once_with(x, [])


class TestInorderTreeWalk:
    def test_inorder_tree_walk(self, patch_singleton: Config) -> None:
        first_test = Test("c", "", None, [], None)
        second_test = Test("e", "", None, [], None)
        third_test = Test("d", "", None, [], None)

        a = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=first_test,
        )
        b = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=second_test,
        )
        x = Node(
            parent=None,
            left=a,
            right=b,
            color=ColorTree.BLACK,
            key=third_test,
        )
        a.parent = x
        b.parent = x

        result: list[str] = []
        tree = CommandsTestTree()
        tree.root = x
        tree._inorder_tree_walk(x, result)

        assert result == [
            first_test.command + " - " + first_test.name,
            third_test.command + " - " + third_test.name,
            second_test.command + " - " + second_test.name,
        ]


class TestTreeMinimum:
    def test_left_is_None(self, patch_singleton: Config) -> None:
        x = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.BLACK,
            key=Test("d", "", None, [], None),
        )

        assert CommandsTestTree()._tree_minimum(x) == x

    def test_tree_minimum(self, patch_singleton: Config) -> None:
        a = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.BLACK,
            key=Test("c", "", None, [], None),
        )
        x = Node(
            parent=None,
            left=a,
            right=None,
            color=ColorTree.BLACK,
            key=Test("d", "", None, [], None),
        )
        a.parent = x

        assert CommandsTestTree()._tree_minimum(x) == a


class TestTransplant:
    def test_u_parent_is_None(self, patch_singleton: Config) -> None:
        u = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.BLACK,
            key=Test("d", "", None, [], None),
        )
        v = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.BLACK,
            key=Test("c", "", None, [], None),
        )
        tree = CommandsTestTree()
        tree._transplant(u, v)

        assert u.parent is None
        assert v.parent is None

        assert u.left is None
        assert v.left is None

        assert u.right is None
        assert v.right is None

        assert u.color.value == "black"
        assert v.color.value == "black"

        assert tree.root is v

    def test_u_is_left_of_parent(self, patch_singleton: Config) -> None:
        v = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("e", "", None, [], None),
        )
        u = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.BLACK,
            key=Test("g", "", None, [], None),
        )
        x = Node(
            parent=None,
            left=u,
            right=None,
            color=ColorTree.BLACK,
            key=Test("k", "", None, [], None),
        )

        u.parent = x
        CommandsTestTree()._transplant(u, v)

        assert v.parent is x
        assert u.parent is x
        assert x.parent is None

        assert v.left is None
        assert u.left is None
        assert x.left is v

        assert v.right is None
        assert u.right is None
        assert x.right is None

        assert v.color.value == "red"
        assert u.color.value == "black"
        assert x.color.value == "black"

    def test_u_is_right_of_parent(self, patch_singleton: Config) -> None:
        v = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("o", "", None, [], None),
        )
        u = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.BLACK,
            key=Test("m", "", None, [], None),
        )
        x = Node(
            parent=None,
            left=None,
            right=u,
            color=ColorTree.BLACK,
            key=Test("k", "", None, [], None),
        )

        u.parent = x
        CommandsTestTree()._transplant(u, v)

        assert v.parent is x
        assert u.parent is x
        assert x.parent is None

        assert v.left is None
        assert u.left is None
        assert x.left is None

        assert v.right is None
        assert u.right is None
        assert x.right is v

        assert v.color.value == "red"
        assert u.color.value == "black"
        assert x.color.value == "black"


@patch("src.tree.CommandsTestTree._delete_fixup")
class TestDelete:
    def test_z_left_is_None(
        self, mock_delete_fixup: Mock, patch_singleton: Config
    ) -> None:
        a = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("t", "", None, [], None),
        )
        z = Node(
            parent=None,
            left=None,
            right=a,
            color=ColorTree.BLACK,
            key=Test("o", "", None, [], None),
        )
        a.parent = z

        CommandsTestTree().delete(z)

        assert a.parent is None
        assert a.left is None
        assert a.right is None
        assert a.color.value == "red"

        mock_delete_fixup.assert_called_once_with(a)

    def test_z_right_is_None(
        self, mock_delete_fixup: Mock, patch_singleton: Config
    ) -> None:
        a = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("j", "", None, [], None),
        )
        z = Node(
            parent=None,
            left=a,
            right=None,
            color=ColorTree.BLACK,
            key=Test("o", "", None, [], None),
        )
        a.parent = z

        CommandsTestTree().delete(z)

        assert a.parent is None
        assert a.left is None
        assert a.right is None
        assert a.color.value == "red"

        mock_delete_fixup.assert_called_once_with(a)

    def test_y_parent_is_z(
        self, mock_delete_fixup: Mock, patch_singleton: Config
    ) -> None:
        b = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("y", "", None, [], None),
        )
        a = Node(
            parent=None,
            left=None,
            right=b,
            color=ColorTree.RED,
            key=Test("t", "", None, [], None),
        )
        c = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("j", "", None, [], None),
        )
        z = Node(
            parent=None,
            left=c,
            right=a,
            color=ColorTree.BLACK,
            key=Test("o", "", None, [], None),
        )
        a.parent = z
        b.parent = a
        c.parent = z

        CommandsTestTree().delete(z)

        assert a.parent is None
        assert b.parent is a

        assert a.left is c
        assert b.left is None

        assert a.right is b
        assert b.right is None

        assert a.color.value == "black"
        assert b.color.value == "red"

        mock_delete_fixup.assert_not_called()

    def test_y_parent_is_not_z(
        self, mock_delete_fixup: Mock, patch_singleton: Config
    ) -> None:
        a = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("j", "", None, [], None),
        )
        d = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("r", "", None, [], None),
        )
        c = Node(
            parent=None,
            left=None,
            right=d,
            color=ColorTree.RED,
            key=Test("q", "", None, [], None),
        )
        b = Node(
            parent=None,
            left=c,
            right=None,
            color=ColorTree.RED,
            key=Test("t", "", None, [], None),
        )
        z = Node(
            parent=None,
            left=a,
            right=b,
            color=ColorTree.BLACK,
            key=Test("o", "", None, [], None),
        )
        a.parent = z
        b.parent = z
        c.parent = b
        d.parent = c

        CommandsTestTree().delete(z)

        assert a.parent is c
        assert b.parent is c
        assert c.parent is None

        assert a.left is None
        assert b.left is d
        assert c.left is a

        assert a.right is None
        assert b.right is None
        assert c.right is b

        assert a.color.value == "red"
        assert b.color.value == "red"
        assert c.color.value == "black"

        mock_delete_fixup.assert_not_called()


class TestDeleteFixup:
    def test_delete_fixup(self, patch_singleton: Config) -> None:
        q = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("a", "", None, [], None),
        )
        w = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("b", "", None, [], None),
        )
        r = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("c", "", None, [], None),
        )
        t = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("d", "", None, [], None),
        )
        y = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("e", "", None, [], None),
        )
        u = Node(
            parent=None,
            left=None,
            right=None,
            color=ColorTree.RED,
            key=Test("f", "", None, [], None),
        )
        a = Node(
            parent=None,
            left=q,
            right=w,
            color=ColorTree.BLACK,
            key=Test("j", "", None, [], None),
        )
        c = Node(
            parent=None,
            left=r,
            right=t,
            color=ColorTree.BLACK,
            key=Test("r", "", None, [], None),
        )
        e = Node(
            parent=None,
            left=y,
            right=u,
            color=ColorTree.BLACK,
            key=Test("y", "", None, [], None),
        )
        d = Node(
            parent=None,
            left=c,
            right=e,
            color=ColorTree.RED,
            key=Test("t", "", None, [], None),
        )
        b = Node(
            parent=None,
            left=a,
            right=d,
            color=ColorTree.BLACK,
            key=Test("o", "", None, [], None),
        )

        a.parent = b
        c.parent = d
        d.parent = b
        e.parent = d
        q.parent = a
        w.parent = a
        r.parent = c
        t.parent = c
        y.parent = e
        u.parent = e

        CommandsTestTree()._change_delete(a)

        assert a.parent is b
        assert b.parent is c
        assert c.parent is d
        assert d.parent is None
        assert e.parent is d

        assert a.left is q
        assert b.left is a
        assert c.left is b
        assert d.left is c
        assert e.left is y

        assert a.right is w
        assert b.right is r
        assert c.right is t
        assert d.right is e
        assert e.right is u

        assert a.color.value == "black"
        assert b.color.value == "black"
        assert c.color.value == "red"
        assert d.color.value == "black"
        assert e.color.value == "black"
