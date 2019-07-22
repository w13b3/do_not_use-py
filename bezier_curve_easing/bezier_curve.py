# !/usr/bin/env python3
import numpy as np

# https://easings.net/
# https://en.wikipedia.org/wiki/Inbetweening
# https://en.wikipedia.org/wiki/B%C3%A9zier_curve

__all__ = ["Easing", "Bezier"]


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
        return n**2

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
        return -n * (n-2)

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
            return 2 * n**2
        else:
            n = n * 2 - 1
            return -0.5 * (n*(n-2) - 1)

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
        return n**3

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
        return n**3 + 1

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
            return 0.5 * (n**3 + 2)

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
        return n**4

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
        return -(n**4 - 1)

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
            return 0.5 * n**4
        else:
            n = n - 2
            return -0.5 * (n**4 - 2)

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
        return n**5

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
        return n**5 + 1

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
            return 0.5 * (n**5 + 2)

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
        return -1 * np.math.cos(n * np.pi / 2) + 1

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
        return np.math.sin(n * np.pi / 2)

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
        return -0.5 * (np.math.cos(np.pi * n) - 1)

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
                return 0.5 * 2**(10 * (n - 1))
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
        return -1 * (np.math.sqrt(1 - n * n) - 1)

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
        return np.math.sqrt(1 - (n * n))

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
            return -0.5 * (np.math.sqrt(1 - n**2) - 1)
        else:
            n = n - 2
            return 0.5 * (np.math.sqrt(1 - n**2) + 1)

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
            s = period / (2 * np.pi) * np.math.asin(1 / amplitude)

        return amplitude * 2**(-10*n) * np.math.sin((n-s)*(2*np.pi / period)) + 1

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
            return self.ease_out_elastic(n-1, amplitude=amplitude, period=period) / 2 + 0.5

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
        if n < (1/2.75):
            return 7.5625 * n * n
        elif n < (2/2.75):
            n -= (1.5/2.75)
            return 7.5625 * n * n + 0.75
        elif n < (2.5/2.75):
            n -= (2.25/2.75)
            return 7.5625 * n * n + 0.9375
        else:
            n -= (2.65/2.75)
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


class Bezier(Easing):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __dir__(self):
        """ return all the easing methods in this class if dir(Bezier()) is used """
        _dir = ["binomial", "bernstein_poly", "bezier", "calc_bezier_path"]
        return _dir

    @staticmethod
    def binomial(n, i) -> float:
        """ Binomial coefficient
            scipy.special.comb replacement
        :param n: (int) number of things
        :param i: (int) number of elements
        """
        _f = np.math.factorial
        return _f(n) / float(_f(i) * _f(n - i))

    def bernstein_poly(self, n, i, t) -> float:
        """ Bernstein polynom.
        :param n: (int) polynom degree
        :param i: (int)
        :param t: (float)
        :return: (float)
        """
        return self.binomial(n, i) * (t ** i) * ((1 - t) ** (n - i))

    def bezier(self, t, control_points) -> np.ndarray:
        """ Return one point on the bezier curve.
        :param t: (float) number in [0, 1]
        :param control_points: (numpy array)
        :return: (numpy ndarray) Coordinates of the point [x y]
        """
        n = len(control_points) - 1
        return np.sum([self.bernstein_poly(n, i, t) * control_points[i] for i in range(n + 1)], axis=0)

    def calc_bezier_path(self, control_points, n_points=100, easing="linear", *args, **kwargs) -> np.ndarray:
        """ Compute bezier path (trajectory) given control points.
        :param control_points: (numpy array)
        :param n_points: (int) number of points in the trajectory
        :param easing: (str) (callable from Easing)
        :return: (numpy ndarray) [[x y], [x y], ... [x y]]
        """
        assert int(n_points) > 0, "keyword: `n_points` should be at least 1"
        assert callable(getattr(self, str(easing))), "keyword: `easing` should be a callable from class Easing"
        assert isinstance(control_points, np.ndarray), "keyword: `control_points` should be a numpy ndarray"
        np_arr = np.array([self.bezier(getattr(self, str(easing))(t, *args, **kwargs), control_points)
                           for t in np.linspace(0, 1, int(n_points))])
        return np.concatenate(([control_points[0]], np_arr, [control_points[-1]]))


if __name__ == '__main__':
    from time import sleep
    from pynput.mouse import Controller
    mouse = Controller()  # pynput
    bezier = Bezier()

    easing = np.random.choice(dir(Easing()))  # randomly choose easing method
    print(f"chosen easing: {easing}")

    cur_x, cur_y = mouse.position   # pynput:  get mouse-pointer position
    points = np.array([[cur_x, cur_y], [200, 800], [200, 200]])  # control points

    for pos in bezier.calc_bezier_path(points, 75, easing):
        mouse.position = pos   # pynput:  set mouse-pointer position
        sleep(0.0275)

    sleep(0.2)
    mouse.position = (cur_x, cur_y)   # pynput:  set mouse-pointer position
