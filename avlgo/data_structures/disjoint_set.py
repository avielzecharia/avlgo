

class DisjointSet:
    """
    This class implements the `Disjoint Set` Data Structure.
    This DS is implemented using trees & node ranks, with additional optimization of tree flattening of find.
    Each Disjoint Set described as a tree rooted with the set leader.

    Complexity: n = number of elements, m = number of operations of union or find
        Total Time Complexity:  O(m * Ackermann^[-1](n)).
        Total Space Complexity: O(n)
    """
    def __init__(self):
        """
        Creating new empty Disjoint Set.

        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self._elements = list()

    def make_set(self, value):
        """
        Creating a new isolated set containing a given value.

        Time Complexity: O(1)
        Space Complexity: O(1)

        :param value: value to be inserted.
        :rtype: DisjointSetElement
        """
        element_set = DisjointSetElement(value)
        self._elements.append(element_set)
        return element_set

    @staticmethod
    def find(element):
        """
        Searching for the element set leader.

        Time Complexity: O(Ackermann^[-1](n)) amortized
        Space Complexity: O(1)

        :param element: element to be search for his leader.
        :type element: DisjointSetElement
        :return: element related set leader.
        :rtype: DisjointSetElement
        """
        leader_scanner = element
        while not leader_scanner.is_leader:
            # Leader has not reached yet.
            leader_scanner = leader_scanner.parent

        # Basically, we got the answer, but we are flattening the tree for future searching optimization.
        # Note that the rank field is not updated, although it is getting smaller.
        while not element.is_leader:
            temp_element = element
            element = element.parent
            temp_element.parent = leader_scanner

        return leader_scanner

    @classmethod
    def union(cls, *elements):
        """
        Union a given set of elements into a the same set.

        Time Complexity: O(#elements * Ackermann^[-1](n)) amortized
        Space Complexity: O(1)

        :param elements: element to union.
        :type elements: DisjointSetElement
        """
        if len(elements) < 2:
            return

        leaders = [cls.find(element) for element in elements]
        for f_leader, s_leader in zip(leaders, leaders[1:]):
            cls._union_leaders(f_leader, s_leader)

    @staticmethod
    def _union_leaders(first_leader, second_leader):
        if first_leader == second_leader:
            # same leaders -> same disjoint set.
            return

        # first disjoint set height is smaller than the second one, make the second as the first parent.
        # in this way we promise to rank up iff the number of nodes at least doubled.
        if first_leader.rank < second_leader.rank:
            first_leader.parent = second_leader
        else:
            second_leader.parent = first_leader

        if first_leader.rank == second_leader.rank:
            # in case we got the same rank, we define the first to be the parent of the second.
            first_leader.rank += 1

    @property
    def elements(self):
        return self._elements

    @property
    def leaders(self):
        """
        Get the number of current disjoint sets.

        Time Complexity: O(n)
        Space Complexity: O(n)

        :return: all DS leaders.
        :rtype: list[DisjointSetElement]
        """
        return [element for element in self._elements if element.is_leader]

    def __len__(self):
        return len(self._elements)


class DisjointSetElement:
    """
    Represent an element in the disjoint set data structure.
    """
    def __init__(self, value):
        self._value = value         # element data to store.
        self._rank = 1              # the `maximal` height of the element node in his related tree.
        self._parent = self         # the parent of the element node in his related tree.

    @property
    def is_leader(self):
        """
        Checking whether element is a leader.
        :return: True if the element is a set leader.
        :rtype: bool
        """
        return self._parent == self

    @property
    def value(self):
        return self._value

    @property
    def rank(self):
        return self._rank

    @property
    def parent(self):
        return self._parent
