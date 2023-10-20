from abc import ABCMeta, abstractmethod


class FrequencyMoment(metaclass=ABCMeta):
    """
    This abstract class describes a general API for the `Frequency Moments` streaming problem.
    """
    def __init__(self, approximation_rate, approximation_probability):
        """
        :param approximation_rate: promised multiplicative approximation bounds (known as epsilon).
        :param approximation_probability: probability that the promised approximation will be in bound (known as delta).
        """
        self._approximation_rate = approximation_rate
        self._approximation_probability = approximation_probability

    @abstractmethod
    def event(self, element):
        """
        Trigger count for event of a specific element

        :param element: element occurred event
        """
        raise NotImplementedError()

    @abstractmethod
    def get_approximation(self):
        """
        Get the final approximation of the frequency moment.

        :return: approximation for the frequency moment.
        :rtype: float
        """
        raise NotImplementedError()

    @property
    def approximation_probability(self):
        """
        Get the probability that the promised approximation will be in bound (known as delta).

        :return: delta
        :rtype: float
        """
        return self._approximation_probability

    @property
    def approximation_rate(self):
        """
        Get the promised multiplicative approximation bounds (known as delta).

        :return: epsilon
        :rtype: float
        """
        return self._approximation_rate
