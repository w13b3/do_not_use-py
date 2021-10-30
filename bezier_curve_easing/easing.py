#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# easing.py

# https://easings.net/
# https://en.wikipedia.org/wiki/Inbetweening

import math

__all__ = ["Easing"]


class Easing:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __dir__(self):
        """ return all the easing methods in this class if dir(Easing()) is used """
        _dir = ["linear",
                "ease_in_quad",    "ease_out_quad",    "ease_in_out_quad",
                "ease_in_sine",    "ease_out_sine",    "ease_in_out_sine",
                "ease_in_expo",    "ease_out_expo",    "ease_in_out_expo",
                "ease_in_circ",    "ease_out_circ",    "ease_in_out_circ",
                "ease_in_back",    "ease_out_back",    "ease_in_out_back",
                "ease_in_cubic",   "ease_out_cubic",   "ease_in_out_cubic",
                "ease_in_quart",   "ease_out_quart",   "ease_in_out_quart",
                "ease_in_quint",   "ease_out_quint",   "ease_in_out_quint",
                "ease_in_bounce",  "ease_out_bounce",  "ease_in_out_bounce",
                "ease_in_elastic", "ease_out_elastic", "ease_in_out_elastic"]
        return _dir

    @staticmethod
    def linear(n, *args, **kwargs) -> float:
        """
        Returns what is given
        :param n: (float) between 0.0 and 1.0
        :param args: to prevent TypeError
        :param kwargs: to prevent TypeError
        :return: (float)
        """
        assert 0.0 <= n <= 1.0, "Value must be between 0.0 and 1.0. Received: {0}".format(n)
        return n

    @staticmethod
    def ease_in_quad(n, *args, **kwargs) -> float:
        """
        https://easings.net/en#easeInQuad
        :param n: (float) between 0.0 and 1.0
        :param args: to prevent TypeError
        :param kwargs: to prevent TypeError
        :return: (float)
        """
        assert 0.0 <= n <= 1.0, "Value must be between 0.0 and 1.0. Received: {0}".format(n)
        return n ** 2

    @staticmethod
    def ease_out_quad(n, *args, **kwargs) -> float:
        """
        https://easings.net/en#easeOutQuad
        :param n: (float) between 0.0 and 1.0
        :param args: to prevent TypeError
        :param kwargs: to prevent TypeError
        :return: (float)
        """
        assert 0.0 <= n <= 1.0, "Value must be between 0.0 and 1.0. Received: {0}".format(n)
        return -n * (n - 2)

    @staticmethod
    def ease_in_out_quad(n, *args, **kwargs) -> float:
        """
        https://easings.net/en#easeInOutQuad
        :param n: (float) between 0.0 and 1.0
        :param args: to prevent TypeError
        :param kwargs: to prevent TypeError
        :return: (float)
        """
        assert 0.0 <= n <= 1.0, "Value must be between 0.0 and 1.0. Received: {0}".format(n)
        if n < 0.5:
            return 2 * n ** 2
        else:
            n = n * 2 - 1
            return -0.5 * (n * (n-2) - 1)

    @staticmethod
    def ease_in_cubic(n, *args, **kwargs) -> float:
        """
        https://easings.net/en#easeInCubic
        :param n: (float) between 0.0 and 1.0
        :param args: to prevent TypeError
        :param kwargs: to prevent TypeError
        :return: (float)
        """
        assert 0.0 <= n <= 1.0, "Value must be between 0.0 and 1.0. Received: {0}".format(n)
        return n ** 3

    @staticmethod
    def ease_out_cubic(n, *args, **kwargs) -> float:
        """
        https://easings.net/en#easeOutCubic
        :param n: (float) between 0.0 and 1.0
        :param args: to prevent TypeError
        :param kwargs: to prevent TypeError
        :return: (float)
        """
        assert 0.0 <= n <= 1.0, "Value must be between 0.0 and 1.0. Received: {0}".format(n)
        n = n - 1
        return n ** 3 + 1

    @staticmethod
    def ease_in_out_cubic(n, *args, **kwargs) -> float:
        """
        https://easings.net/en#easeInOutCubic
        :param n: (float) between 0.0 and 1.0
        :param args: to prevent TypeError
        :param kwargs: to prevent TypeError
        :return: (float)
        """
        assert 0.0 <= n <= 1.0, "Value must be between 0.0 and 1.0. Received: {0}".format(n)
        n = 2 * n
        if n < 1:
            return 0.5 * n**3
        else:
            n = n - 2
            return 0.5 * (n ** 3 + 2)

    @staticmethod
    def ease_in_quart(n, *args, **kwargs) -> float:
        """
        https://easings.net/en#easeInQuart
        :param n: (float) between 0.0 and 1.0
        :param args: to prevent TypeError
        :param kwargs: to prevent TypeError
        :return: (float)
        """
        assert 0.0 <= n <= 1.0, "Value must be between 0.0 and 1.0. Received: {0}".format(n)
        return n ** 4

    @staticmethod
    def ease_out_quart(n, *args, **kwargs) -> float:
        """
        https://easings.net/en#easeOutQuart
        :param n: (float) between 0.0 and 1.0
        :param args: to prevent TypeError
        :param kwargs: to prevent TypeError
        :return: (float)
        """
        assert 0.0 <= n <= 1.0, "Value must be between 0.0 and 1.0. Received: {0}".format(n)
        n = n - 1
        return -(n ** 4 - 1)

    @staticmethod
    def ease_in_out_quart(n, *args, **kwargs) -> float:
        """
        https://easings.net/en#easeInOutQuart
        :param n: (float) between 0.0 and 1.0
        :param args: to prevent TypeError
        :param kwargs: to prevent TypeError
        :return: (float)
        """
        assert 0.0 <= n <= 1.0, "Value must be between 0.0 and 1.0. Received: {0}".format(n)
        n = 2 * n
        if n < 1:
            return 0.5 * n ** 4
        else:
            n = n - 2
            return -0.5 * (n ** 4 - 2)

    @staticmethod
    def ease_in_quint(n, *args, **kwargs) -> float:
        """
        https://easings.net/en#easeInQuint
        :param n: (float) between 0.0 and 1.0
        :param args: to prevent TypeError
        :param kwargs: to prevent TypeError
        :return: (float)
        """
        assert 0.0 <= n <= 1.0, "Value must be between 0.0 and 1.0. Received: {0}".format(n)
        return n ** 5

    @staticmethod
    def ease_out_quint(n, *args, **kwargs) -> float:
        """
        https://easings.net/en#easeOutQuint
        :param n: (float) between 0.0 and 1.0
        :param args: to prevent TypeError
        :param kwargs: to prevent TypeError
        :return: (float)
        """
        assert 0.0 <= n <= 1.0, "Value must be between 0.0 and 1.0. Received: {0}".format(n)
        n = n - 1
        return n ** 5 + 1

    @staticmethod
    def ease_in_out_quint(n, *args, **kwargs) -> float:
        """
        https://easings.net/en#easeInOutQuint
        :param n: (float) between 0.0 and 1.0
        :param args: to prevent TypeError
        :param kwargs: to prevent TypeError
        :return: (float)
        """
        assert 0.0 <= n <= 1.0, "Value must be between 0.0 and 1.0. Received: {0}".format(n)
        n = 2 * n
        if n < 1:
            return 0.5 * n**5
        else:
            n = n - 2
            return 0.5 * (n ** 5 + 2)

    @staticmethod
    def ease_in_sine(n, *args, **kwargs) -> float:
        """
        https://easings.net/en#easeInSine
        :param n: (float) between 0.0 and 1.0
        :param args: to prevent TypeError
        :param kwargs: to prevent TypeError
        :return: (float)
        """
        assert 0.0 <= n <= 1.0, "Value must be between 0.0 and 1.0. Received: {0}".format(n)
        return -1 * math.cos(n * math.pi / 2) + 1

    @staticmethod
    def ease_out_sine(n, *args, **kwargs) -> float:
        """
        https://easings.net/en#easeOutSine
        :param n: (float) between 0.0 and 1.0
        :param args: to prevent TypeError
        :param kwargs: to prevent TypeError
        :return: (float)
        """
        assert 0.0 <= n <= 1.0, "Value must be between 0.0 and 1.0. Received: {0}".format(n)
        return math.sin(n * math.pi / 2)

    @staticmethod
    def ease_in_out_sine(n, *args, **kwargs) -> float:
        """
        https://easings.net/en#easeInOutSine
        :param n: (float) between 0.0 and 1.0
        :param args: to prevent TypeError
        :param kwargs: to prevent TypeError
        :return: (float)
        """
        assert 0.0 <= n <= 1.0, "Value must be between 0.0 and 1.0. Received: {0}".format(n)
        return -0.5 * (math.cos(math.pi * n) - 1)

    @staticmethod
    def ease_in_expo(n, *args, **kwargs) -> float:
        """
        https://easings.net/en#easeInExpo
        :param n: (float) between 0.0 and 1.0
        :param args: to prevent TypeError
        :param kwargs: to prevent TypeError
        :return: (float)
        """
        assert 0.0 <= n <= 1.0, "Value must be between 0.0 and 1.0. Received: {0}".format(n)
        if n == 0:
            return 0
        else:
            return 2**(10 * (n - 1))

    @staticmethod
    def ease_out_expo(n, *args, **kwargs) -> float:
        """
        https://easings.net/en#easeOutExpo
        :param n: (float) between 0.0 and 1.0
        :param args: to prevent TypeError
        :param kwargs: to prevent TypeError
        :return: (float)
        """
        assert 0.0 <= n <= 1.0, "Value must be between 0.0 and 1.0. Received: {0}".format(n)
        if n == 1:
            return 1
        else:
            return -(2 ** (-10 * n)) + 1

    @staticmethod
    def ease_in_out_expo(n, *args, **kwargs) -> float:
        """
        https://easings.net/en#easeInOutExpo
        :param n: (float) between 0.0 and 1.0
        :param args: to prevent TypeError
        :param kwargs: to prevent TypeError
        :return: (float)
        """
        assert 0.0 <= n <= 1.0, "Value must be between 0.0 and 1.0. Received: {0}".format(n)
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            n = n * 2
            if n < 1:
                return 0.5 * 2 ** (10 * (n - 1))
            else:
                n -= 1
                # 0.5 * (-() + 2)
                return 0.5 * (-1 * (2 ** (-10 * n)) + 2)

    @staticmethod
    def ease_in_circ(n, *args, **kwargs) -> float:
        """
        https://easings.net/en#easeInCirc
        :param n: (float) between 0.0 and 1.0
        :param args: to prevent TypeError
        :param kwargs: to prevent TypeError
        :return: (float)
        """
        assert 0.0 <= n <= 1.0, "Value must be between 0.0 and 1.0. Received: {0}".format(n)
        return -1 * (math.sqrt(1 - n * n) - 1)

    @staticmethod
    def ease_out_circ(n, *args, **kwargs) -> float:
        """
        https://easings.net/en#easeOutCirc
        :param n: (float) between 0.0 and 1.0
        :param args: to prevent TypeError
        :param kwargs: to prevent TypeError
        :return: (float)
        """
        assert 0.0 <= n <= 1.0, "Value must be between 0.0 and 1.0. Received: {0}".format(n)
        n -= 1
        return math.sqrt(1 - (n * n))

    @staticmethod
    def ease_in_out_circ(n, *args, **kwargs) -> float:
        """
        https://easings.net/en#easeInOutCirc
        :param n: (float) between 0.0 and 1.0
        :param args: to prevent TypeError
        :param kwargs: to prevent TypeError
        :return: (float)
        """
        assert 0.0 <= n <= 1.0, "Value must be between 0.0 and 1.0. Received: {0}".format(n)
        n = n * 2
        if n < 1:
            return -0.5 * (math.sqrt(1 - n**2) - 1)
        else:
            n = n - 2
            return 0.5 * (math.sqrt(1 - n**2) + 1)

    def ease_in_elastic(self, n, amplitude=1, period=0.3, *args, **kwargs) -> float:
        """
        https://easings.net/en#easeInElastic
        :param n: (float) between 0.0 and 1.0
        :param amplitude: (float)
        :param period: (float)
        :param args: to prevent TypeError
        :param kwargs: to prevent TypeError
        :return: (float)
        """
        assert 0.0 <= n <= 1.0, "Value must be between 0.0 and 1.0. Received: {0}".format(n)
        return 1 - self.ease_out_elastic(1-n, amplitude=amplitude, period=period)

    @staticmethod
    def ease_out_elastic(n, amplitude=1, period=0.3, *args, **kwargs) -> float:
        """
        https://easings.net/en#easeOutElastic
        :param n: (float) between 0.0 and 1.0
        :param amplitude: (float)
        :param period: (float)
        :param args: to prevent TypeError
        :param kwargs: to prevent TypeError
        :return: (float)
        """
        assert 0.0 <= n <= 1.0, "Value must be between 0.0 and 1.0. Received: {0}".format(n)
        if amplitude < 1:
            amplitude = 1
            s = period / 4
        else:
            s = period / (2 * math.pi) * math.asin(1 / amplitude)

        return amplitude * 2 ** (-10 * n) * math.sin((n - s) * (2 * math.pi / period)) + 1

    def ease_in_out_elastic(self, n, amplitude=1, period=0.5, *args, **kwargs) -> float:
        """
        https://easings.net/en#easeInOutElastic
        :param n: (float) between 0.0 and 1.0
        :param amplitude: (float)
        :param period: (float)
        :param args: to prevent TypeError
        :param kwargs: to prevent TypeError
        :return: (float)
        """
        assert 0.0 <= n <= 1.0, "Value must be between 0.0 and 1.0. Received: {0}".format(n)
        n *= 2
        if n < 1:
            return self.ease_in_elastic(n, amplitude=amplitude, period=period) / 2
        else:
            return self.ease_out_elastic(n - 1, amplitude=amplitude, period=period) / 2 + 0.5

    @staticmethod
    def ease_in_back(n, s=1.70158, *args, **kwargs) -> float:
        """
        https://easings.net/en#easeInBack
        :param n: (float) between 0.0 and 1.0
        :param s: (float) overshoot  10%: 1.70154198866824  100%: 8.443535601593252
        :param args: to prevent TypeError
        :param kwargs: to prevent TypeError
        :return: (float)
        """
        assert 0.0 <= n <= 1.0, "Value must be between 0.0 and 1.0. Received: {0}".format(n)
        return n * n * ((s + 1) * n - s)

    @staticmethod
    def ease_out_back(n, s=1.70158, *args, **kwargs) -> float:
        """
        https://easings.net/en#easeOutBack
        :param n: (float) between 0.0 and 1.0
        :param s: (float) overshoot  10%: 1.70154198866824  100%: 8.443535601593252
        :param args: to prevent TypeError
        :param kwargs: to prevent TypeError
        :return: (float)
        """
        assert 0.0 <= n <= 1.0, "Value must be between 0.0 and 1.0. Received: {0}".format(n)
        n = n - 1
        return n * n * ((s + 1) * n + s) + 1

    @staticmethod
    def ease_in_out_back(n, s=1.70158, *args, **kwargs) -> float:
        """
        https://easings.net/en#easeInOutBack
        :param n: (float) between 0.0 and 1.0
        :param s: (float) overshoot  10%: 1.70154198866824  100%: 8.443535601593252
        :param args: to prevent TypeError
        :param kwargs: to prevent TypeError
        :return: (float)
        """
        assert 0.0 <= n <= 1.0, "Value must be between 0.0 and 1.0. Received: {0}".format(n)
        n = n * 2
        if n < 1:
            s *= 1.525
            return 0.5 * (n * n * ((s + 1) * n - s))
        else:
            n -= 2
            s *= 1.525
            return 0.5 * (n * n * ((s + 1) * n + s) + 2)

    def ease_in_bounce(self, n, *args, **kwargs) -> float:
        """
        https://easings.net/en#easeInBounce
        :param n: (float) between 0.0 and 1.0
        :param args: to prevent TypeError
        :param kwargs: to prevent TypeError
        :return: (float)
        """
        assert 0.0 <= n <= 1.0, "Value must be between 0.0 and 1.0. Received: {0}".format(n)
        return 1 - self.ease_out_bounce(1 - n)

    @staticmethod
    def ease_out_bounce(n, *args, **kwargs) -> float:
        """
        https://easings.net/en#easeOutBounce
        :param n: (float) between 0.0 and 1.0
        :param args: to prevent TypeError
        :param kwargs: to prevent TypeError
        :return: (float)
        """
        assert 0.0 <= n <= 1.0, "Value must be between 0.0 and 1.0. Received: {0}".format(n)
        if n < (1 / 2.75):
            return 7.5625 * n * n
        elif n < (2 / 2.75):
            n -= (1.5 / 2.75)
            return 7.5625 * n * n + 0.75
        elif n < (2.5 / 2.75):
            n -= (2.25 / 2.75)
            return 7.5625 * n * n + 0.9375
        else:
            n -= (2.65 / 2.75)
            return 7.5625 * n * n + 0.984375

    def ease_in_out_bounce(self, n, *args, **kwargs) -> float:
        """
        https://easings.net/en#easeInOutBounce
        :param n: (float) between 0.0 and 1.0
        :param args: to prevent TypeError
        :param kwargs: to prevent TypeError
        :return: (float)
        """
        assert 0.0 <= n <= 1.0, "Value must be between 0.0 and 1.0. Received: {0}".format(n)
        if n < 0.5:
            return self.ease_in_bounce(n * 2) * 0.5
        else:
            return self.ease_out_bounce(n * 2 - 1) * 0.5 + 0.5
