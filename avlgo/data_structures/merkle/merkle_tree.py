from hashlib import sha256
from collections import namedtuple

from avlgo.data_structures.utils import BinaryTreeNode, Direction

LeafProof = namedtuple("LeafProof", ["tree_digest", "hash_alg", "hashes", "directions"])


class MerkleTree:
    """
    Merkle Tree Data Structure.

    Time Complexity: O(logn) for all operations.
    Space Complexity: O(n)
    """
    def __init__(self, hash_alg=sha256):
        """
        :param hash_alg: hash algorithm to generate the tree with (e.g. hashlib.sha256)
        """
        self._root = None
        self._leaves = list()

        self._hash_alg = hash_alg

    def add_node(self, data):
        """
        Insert new node to the Merkle Tree.

        Time Complexity: O(logn)

        :param data: data to store in a new node
        :type data: bytes
        :return: inserted node id (index)
        :rtype: int
        """
        if self.is_empty:
            new_node = _MerkleNode.create_leaf(data, self._hash_alg)
            self._root = new_node
        else:
            split_node = self._find_split_node(self._root)
            _, new_node = self._split_node(split_node, data)

        self._leaves.append(new_node)
        return len(self._leaves) - 1

    def proof_leaf(self, leaf_id):
        """
        Generate a proof for leaf existence in the merkle tree.

        Time Complexity: O(logn)
        Space Complexity: O(logn)

        :param leaf_id: leaf identifier
        :type leaf_id: int
        :return: leaf existence proof "down-to-top"
        :rtype: LeafProof
        """
        if leaf_id < 0 or leaf_id >= len(self.leaves):
            raise RuntimeError("Invalid leaf index")

        directions = list()
        hashes = list()

        node_scanner = self._leaves[leaf_id]
        while node_scanner.parent:
            sibling_child = node_scanner.parent.child_sibling(node_scanner)
            hashes.append(sibling_child.data_hash)
            directions.append(sibling_child.direction)

            node_scanner = node_scanner.parent

        return LeafProof(
            tree_digest=self.tree_digest,
            hash_alg=self._hash_alg,
            directions=directions,
            hashes=hashes
        )

    @staticmethod
    def validate_proof(tree_digest, data, leaf_proof):
        """
        Verify whether a given generated leaf proof sis valid in the merkle tree.

        Time Complexity: O(logn)

        :param tree_digest: merkle tree hash to verify with
        :type tree_digest: bytes
        :param data: daa to verify if exists
        :type data: bytes
        :param leaf_proof: leaf proof to verify
        :type leaf_proof: LeafProof
        :rtype: bool
        """
        if leaf_proof.tree_digest != tree_digest:
            return False

        verification_hash = leaf_proof.hash_alg(data).hexdigest().encode()
        for node_hash, direction in zip(leaf_proof.hashes, leaf_proof.directions):
            if direction == Direction.RIGHT:
                to_hash = verification_hash + node_hash
            else:
                to_hash = node_hash + verification_hash

            verification_hash = leaf_proof.hash_alg(to_hash).hexdigest().encode()

        return verification_hash == tree_digest

    def is_root(self, node):
        return self._root == node

    @property
    def is_empty(self):
        return self._root is None

    @property
    def root(self):
        return self._root

    @property
    def leaves(self):
        return self._leaves

    @property
    def tree_digest(self):
        if not self.is_empty:
            return self._root.data_hash

    def _split_node(self, split_node, data):
        """
        Given a split node and data to insert, connect a new node to the split node with the given data.
           PARENT_NODE                        PARENT_NODE
                  \\                 ->              \\
                SPILT_NODE                          MERGE_NODE
                 //    \\                           //      \\
                ?        ?                      SPLIT_NODE  NEW_NODE
        """
        parent_node = split_node.parent
        new_node = _MerkleNode.create_leaf(data, self._hash_alg)
        merge_node = _MerkleNode.create_node(left=split_node, right=new_node, hash_alg=self._hash_alg)

        if split_node.parent:
            split_node.parent.update_child(split_node, merge_node)
        split_node.parent = merge_node

        if self.is_root(split_node):
            self._root = merge_node
        else:
            parent_node.update_child(merge_node, split_node)

        return merge_node, new_node

    @staticmethod
    def _find_split_node(node):
        """
        Find the next node to be split on insertion.
        """
        if node.is_full:
            return node

        # The left node must be full by construction rules
        return MerkleTree._find_split_node(node.right)


class _MerkleNode(BinaryTreeNode):
    """
    Store necessary information for binary merkle tree maintenance.
    """
    def __init__(self, data, height, leaves_counter, hash_alg, left=None, right=None):
        super(_MerkleNode, self).__init__(data=data, left=left, right=right)

        self.height = height
        self.leaves_counter = leaves_counter
        self.hash_alg = hash_alg
        self.data_hash = self.hash_alg(self.data).hexdigest().encode()

    @classmethod
    def create_leaf(cls, data, hash_alg):
        """
        Create new merkle leaf node.
        :param data: data to store
        :type data: bytes
        :param hash_alg: hash algorithm
        :rtype: _MerkleNode
        """
        return cls(
            data=data,
            height=0,
            leaves_counter=1,
            hash_alg=hash_alg
        )

    @classmethod
    def create_node(cls, left, right, hash_alg):
        """
        Creates new merkle internal node.
        :param left: left child
        :type left: _MerkleNode
        :param right: right child
        :type right: _MerkleNode
        :param hash_alg: hash algorithm
        :rtype: _MerkleNode
        """
        node = cls(
            data=left.data_hash + right.data_hash,
            height=max(left.height, right.height) + 1,
            leaves_counter=left.leaves_counter + right.leaves_counter,
            hash_alg=hash_alg,
            left=left,
            right=right
        )
        left.parent = node
        right.parent = node

        return node

    def update_child(self, new_child, old_child):
        """
        Update child of a given merkle tree node.
        :param new_child: child to set.
        :type new_child: _MerkleNode
        :param old_child: child to override.
        :type old_child: _MerkleNode
        """
        if self.right == old_child:
            self.right = new_child
        else:
            self.left = new_child

        self.height = max(self.left.height, self.right.height) + 1,
        self.leaves_counter = self.left.leaves_counter + self.right.leaves_counter,
        self.data = self.left.data_hash + self.right.data_hash
        self.data_hash = self.hash_alg(self.data).hexdigest().encode()

        if self.parent:
            self.parent.update_child(self, self)

    @property
    def capacity(self):
        return 2 ** self.height

    @property
    def is_full(self):
        return self.capacity == self.leaves_counter

    @property
    def is_leaf(self):
        return self.left is None and self.right is None
