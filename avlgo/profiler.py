from contextlib import contextmanager
from datetime import timedelta
from datetime import datetime


@contextmanager
def context_time_profiler():
    """
    Context manager which eventually prints the amount of inner execution time.
    """
    start_time = datetime.now()
    yield
    print(datetime.now() - start_time)


def time_profiler(logic, *args, **kwargs):
    """
    Profile a given function logic execution time.

    :return: logic execution time
    :rtype: timedelta
    """
    start_time = datetime.now()
    logic(*args, **kwargs)
    return datetime.now() - start_time


def compare_avg_time(logic1, args1_list, kwargs1_list, logic2, args2_list, kwargs2_list):
    """
    Profile a given function logic execution time.

    :return: average logic execution time of each logic.
    :rtype: tuple[timedelta, timedelta]
    """
    logic1_time = timedelta(0)
    logic2_time = timedelta(0)
    for args1, kwargs1, args2, kwargs2 in zip(args1_list, kwargs1_list, args2_list, kwargs2_list):
        logic1_time += time_profiler(logic1, *args1, **kwargs1)
        logic2_time += time_profiler(logic2, *args2, **kwargs2)

    return logic1_time / len(args1_list), logic2_time / len(args2_list)