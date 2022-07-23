from hashlib import sha256

from avlgo.data_structures.utils import BinaryTreeNode, Direction


class SparseMerkleTree:
    """
    Sparse Merkle Tree Data Structure.

    U - hash universe range size
    Time Complexity: O(log^2(U)) for all operations
    Space Complexity: O(#marked_elements + log^2(U))
    """
    NON_EXISTING_LEAF_DATA = b'0'
    EXISTING_LEAF_DATA = b'1'

    def __init__(self, hash_alg=sha256):
        """
        Generate new sparse merkle tree on a given hash.

        Time Complexity: O(log^2(U))
        Space Complexity: O(log^2(U))

        :param hash_alg: hash algorithm to generate the tree with (e.g. hashlib.sha256)
        """
        self._hash_alg = hash_alg
        self._hash_size = 4 * len(hash_alg().hexdigest())
        self._dummy_hashes = self._generate_dummy_hashes()

        self._root = _SparseMerkleNode.create_root(hash_size=self._hash_size)

    def mark_leaf(self, digest):
        """
        In order to mark a digest to be exist in the tree, we are creating the full path
        from the root to the representing node (without dummy nodes in the direct path).
        :param digest: leaf representing digest
        :type digest: bytes
        """
        scanner = direction = None
        for scanner, direction in self._tree_navigator(digest):
            if not scanner.is_leaf:
                continue

            scanner.right = _SparseMerkleNode.create_node(
                parent=scanner,
                is_dummy=(direction != Direction.RIGHT),
                dummy_hashes=self._dummy_hashes
            )
            scanner.left = _SparseMerkleNode.create_node(
                parent=scanner,
                is_dummy=(direction != Direction.LEFT),
                dummy_hashes=self._dummy_hashes
            )

        # now child contains the digest leaf, mark child as existing and update the tree hashes
        scanner.child(direction).mark()
        scanner.update_data(self._hash_alg)

    def is_marked(self, digest):
        """
        Determine whether a given leaf is marked in the sparse merkle tree.

        Time Complexity: O(log(U))
        Space Complexity: O(log(U))

        :param digest: leaf representing digest
        :type digest: bytes
        :rtype: bool
        """
        scanner = direction = None
        for scanner, direction in self._tree_navigator(digest):
            pass

        # child can be None only if we stopped at the middle of the navigation
        return scanner.child(direction) is not None

    # TODO: proof & validate

    def _generate_dummy_hashes(self):
        """
        Generate known hashes of the initial sparse merkle tree.

        Time Complexity: O(log^2(U))
        Space Complexity: O(log^2(U))

        :rtype: list[bytes]
        """
        dummy_hashes = [self.NON_EXISTING_LEAF_DATA]
        for _ in range(self._hash_size):
            next_level_dummy = 2 * dummy_hashes[-1]
            dummy_hashes.append(
                self._hash_alg(next_level_dummy).hexdigest().encode()
            )

        return dummy_hashes

    def _tree_navigator(self, digest):
        """
        Generator which yields the next node|direction to navigate in the tree, based on digest binary representation.

        Time Complexity: O(log(U))
        Space Complexity: O(log(U))
        """
        digest_value = int(digest, 0x10)
        digest_bin = bin(digest_value)[2:]
        digest_bin += '0' * (self._hash_size - len(digest_bin))

        scanner = self._root
        for bit in digest_bin:
            if scanner is None:
                return

            direction = Direction(int(bit))
            yield scanner, direction
            scanner = scanner.child(direction)

    @property
    def root(self):
        return self._root

    @property
    def bits(self):
        return self._hash_size

    @property
    def tree_digest(self):
        return self._root.data


class _SparseMerkleNode(BinaryTreeNode):
    def __init__(self, height, is_dummy, parent=None, data=None):
        super(_SparseMerkleNode, self).__init__(parent=parent, data=data)

        self.height = height
        self.is_dummy = is_dummy

    @classmethod
    def create_root(cls, hash_size):
        """
        Creates new dummy root node in the sparse merkle tree.
        """
        return cls(
            height=hash_size,
            is_dummy=True,
            data=SparseMerkleTree.NON_EXISTING_LEAF_DATA
        )

    @classmethod
    def create_node(cls, parent, is_dummy, dummy_hashes):
        """
        Creates new dummy leaf node in the sparse merkle tree.
        """
        height = parent.height - 1
        data = dummy_hashes[height] if is_dummy else None

        return cls(
            height=height,
            is_dummy=is_dummy,
            parent=parent,
            data=data
        )

    def mark(self):
        if self.is_absolute_leaf:
            self.data = SparseMerkleTree.EXISTING_LEAF_DATA
        else:
            raise InternalNodeCannotBeMarkedException()

    def update_data(self, hash_alg):
        children_data = self.left.data + self.right.data
        self.data = hash_alg(children_data).hexdigest().encode()

        if self.parent:
            self.parent.update_data(hash_alg)

    @property
    def is_absolute_leaf(self):
        return self.height == 0


class InternalNodeCannotBeMarkedException(Exception):
    pass
