from enum import Enum


class Direction(Enum):
    LEFT = 0
    RIGHT = 1


class BinaryTreeNode:
    """
    Represent a generic node in a binary tree structure.
    """
    def __init__(self, parent=None, left=None, right=None, data=None):
        self.parent = parent
        self.left = left
        self.right = right
        self.data = data

    def child_sibling(self, child):
        """
        Retrieve the other child of the node.
        :type child: BinaryTreeNode
        :return: right for left child, left for right child.
        :rtype: BinaryTreeNode
        """
        if self.left == child:
            return self.right
        elif self.right == child:
            return self.left
        else:
            raise InvalidChildException("child is not one of node children")

    def child_direction(self, child):
        """
        Retrieve the child binary direction.
        :type child: BinaryTreeNode
        :rtype: Direction
        """
        if self.left == child:
            return Direction.LEFT
        elif self.right == child:
            return Direction.RIGHT
        else:
            raise InvalidChildException("child is not one of node children")

    def child(self, direction):
        """
        Retrieve the suitable child by direction.
        :type direction: Direction
        """
        if direction == Direction.LEFT:
            return self.left
        elif  direction == Direction.RIGHT:
            return self.right
        else:
            raise InvalidDirection()

    @property
    def direction(self):
        return self.parent.child_direction(self)

    @property
    def is_leaf(self):
        return self.left is None and self.right is None


class InvalidChildException(Exception):
    pass


class InvalidDirection(Exception):
    pass
