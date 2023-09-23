from math import ceil

from avlgo.data_structures.succinct.compact_rank import CompactRank
from avlgo.profiler import object_memory_dword, TimeContext


def test_simple_rank():
    elements = [1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1]
    cr = CompactRank(elements)
    for i in range(len(elements)):
        assert cr.rank(i) == sum(elements[:i])


def test_advanced_rank():
    elements = [i % 3 == 0 for i in range(10 ** 6)]
    cr = CompactRank(elements)
    for i in range(len(elements)):
        assert cr.rank(i) == ceil(i / 3)


def test_time():
    timer = TimeContext()
    elements = [i % 5 == 0 for i in range(10 ** 7)]

    with timer:
        cr = CompactRank(elements)

    assert timer.time.total_seconds() < 8

    with timer:
        for i in range(len(elements)):
            cr.rank(i)

    assert timer.time.total_seconds() < 25


def test_space():
    elements = [i % 7 == 0 for i in range(10 ** 5)]
    cr = CompactRank(elements)

    assert object_memory_dword(cr) < 20000
