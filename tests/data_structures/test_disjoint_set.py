from avlgo.data_structures.disjoint_set import DisjointSet
from avlgo.profiler import object_memory_dword, TimeContext


def test_make_set():
    ds = DisjointSet()
    e1 = ds.make_set(1)
    e2 = ds.make_set(2)
    e3 = ds.make_set(3)

    assert len(ds) == 3
    assert e1.is_leader
    assert e2.is_leader
    assert e3.is_leader


def test_simple_union():
    ds = DisjointSet()
    e1 = ds.make_set(1)
    e2 = ds.make_set(2)
    e3 = ds.make_set(3)
    ds.union(e1, e3)

    assert ds.find(e1) == ds.find(e3)
    assert ds.find(e2) != ds.find(e3)
    assert ds.find(e1) != ds.find(e2)


def test_advanced_union():
    ds = DisjointSet()

    for i in range(10 ** 6):
        ds.make_set(i)

    for i in range(10 ** 6):
        ds.union(ds.elements[i], ds.elements[(i + 2) % 10 ** 6])

    for i in range(10 ** 6):
        assert ds.find(ds.elements[i]) == ds.find(ds.elements[i % 2])


def test_memory():
    ds = DisjointSet()
    for i in range(10 ** 4):
        ds.make_set(i)

    assert object_memory_dword(ds) < 10 ** 5


def test_time():
    timer = TimeContext()
    ds = DisjointSet()

    with timer:
        for i in range(10 ** 6):
            ds.make_set(i)

    assert timer.time.total_seconds() < 1

    with timer:
        for i in range(1, 10 ** 6):
            ds.union(ds.elements[0], ds.elements[i])

    assert timer.time.total_seconds() < 2

    with timer:
        for i in range(1, 10 ** 6):
            ds.find(ds.elements[i])

    assert timer.time.total_seconds() < 1


test_advanced_union()
