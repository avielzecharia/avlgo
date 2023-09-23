import pytest

from avlgo.data_structures.succinct.compact_select import CompactSelect
from avlgo.profiler import object_memory_dword, TimeContext


def test_advanced_rank():
    elements = [i % 3 == 0 for i in range(10 ** 6 - 1)]
    cs = CompactSelect(elements)
    for i in range(1, len(elements) // 3):
        assert cs.select(i) == 3 * (i - 1)

    for i in range(len(elements) // 3 + 1, len(elements)):
        with pytest.raises(IndexError):
            cs.select(i)


def test_time():
    timer = TimeContext()
    elements = [i % 5 == 0 for i in range(10 ** 7)]

    with timer:
        cs = CompactSelect(elements)

    assert timer.time.total_seconds() < 6

    with timer:
        for i in range(1, len(elements) // 5):
            cs.select(i)

    assert timer.time.total_seconds() < 10


def test_space():
    elements = [i % 5 == 0 for i in range(10 ** 5)]
    cs = CompactSelect(elements)

    assert object_memory_dword(cs) < 25000
