from avlgo.data_structures.merkle import MerkleTree
from avlgo.data_structures.utils import Direction
from avlgo.profiler import object_memory_dword, TimeContext


def test_add_node_simple():
    mt = MerkleTree()
    assert mt.tree_digest is None
    assert len(mt) == 0

    mt.add_node(b'0')
    assert mt.tree_digest == b'5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9'
    assert len(mt) == 1

    mt.add_node(b'1')
    assert mt.tree_digest == b'fa13bb36c022a6943f37c638126a2c88fc8d008eb5a9fe8fcde17026807feae4'
    assert len(mt) == 2


def test_add_node_advanced():
    mt = MerkleTree()
    for i in range(2 ** 8):
        mt.add_node(b'0')

    assert mt.tree_digest == b'53efe33f4a8c94df247471670cfd59cce8797365e9b41138fc8b44fb394b30c8'
    assert len(mt) == 256


def test_proof():
    mt = MerkleTree()
    for i in range(2 ** 8):
        mt.add_node(b'0')

    mt.add_node(b'1')

    proof_0 = mt.proof(0)
    assert proof_0.hashes == [
        b'5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9',
        b'984ec4499b3a6b90bbcd8e05efe985a1c3c8f75a657cf0d70049ffd111f90b8d',
        b'5dea0672f7952996746a0dc5637ae56ac349ceb2df0f48358ef0dca9981b9823',
        b'77e2e435abc70734a0b3b211d8a33f8ceb98599a03f58b22e3f99c28cd4027e5',
        b'601e615a178c275f7df2be8bdb2b4d84deafb2dc45956b2e12217a550ad15a7b',
        b'9e95619889c8b61cb559a4e153379c3a136a55f79232e28973df8bcb11f9b57f',
        b'cd03b83e7676779cc20a6a9c941f43cce1c6f86b3892192a8450f6e416ca20b4',
        b'244e798844fab737eb491ebb23e7cef7f90abd361cb3c7fdb1d95524b7c3dc25',
        b'6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b'
    ]
    assert proof_0.directions == 9 * [Direction.RIGHT]

    proof_1 = mt.proof(256)
    assert proof_1.hashes == [b'53efe33f4a8c94df247471670cfd59cce8797365e9b41138fc8b44fb394b30c8']
    assert proof_1.directions == [Direction.LEFT]


test_proof()


def test_validate():
    mt = MerkleTree()

    for i in range(1000):
        data = str(i % 2).encode()
        mt.add_node(data)
        proof = mt.proof(i)
        assert mt.validate(mt.tree_digest, data, proof)

    for i in range(1000):
        data = str(i % 2).encode()
        proof = mt.proof(i)
        assert mt.validate(mt.tree_digest, data, proof)


def test_time():
    timer = TimeContext()
    mt = MerkleTree()

    with timer:
        for i in range(2 ** 17):
            mt.add_node(b'0')

    assert timer.time.total_seconds() < 4

    with timer:
        for i in range(2 ** 17):
            mt.proof(i)

    assert timer.time.total_seconds() < 2


def test_storage():
    mt = MerkleTree()
    for i in range(2 ** 10):
        data = str(i % 2).encode()
        mt.add_node(data)

    assert object_memory_dword(mt) < 30000
