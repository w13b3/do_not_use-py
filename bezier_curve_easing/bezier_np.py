#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# bezier_curve.py

from typing import Callable
import numpy as np

# https://en.wikipedia.org/wiki/B%C3%A9zier_curve

__all__ = ["Bezier"]


class Bezier:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __dir__(self):
        """return all the easing methods in this class if dir(Bezier()) is used"""
        _dir = ["binomial", "bernstein_poly", "bezier", "bezier_path"]
        return _dir

    @staticmethod
    def binomial(n, i) -> float:
        """Binomial coefficient
           scipy.special.comb replacement
        :param n: (int) number of things
        :param i: (int) number of elements
        """
        _f = np.math.factorial
        return _f(n) / float(_f(i) * _f(n - i))

    @classmethod
    def bernstein_poly(cls, n, i, t) -> float:
        """Bernstein polynom
        :param n: (int) polynom degree
        :param i: (int)
        :param t: (float)
        :return: (float)
        """
        return cls.binomial(n, i) * (t ** i) * ((1 - t) ** (n - i))

    @classmethod
    def bezier(cls, t, control_points) -> np.ndarray:
        """Return one point on the bezier curve
        :param t: (float) number in [0, 1]
        :param control_points: (numpy array)
        :return: (numpy ndarray) Coordinates of the point [x y]
        """
        n = len(control_points) - 1
        return np.sum([cls.bernstein_poly(n, i, t) * control_points[i] for i in range(n + 1)], axis=0)

    @classmethod
    def bezier_path(cls,
                    n_points: int,
                    control_points: np.ndarray,
                    easing: Callable[[float], float] = None,
                    *args, **kwargs) -> np.ndarray:
        """ Compute bezier path (trajectory) given control points
        :param n_points: (int) number of points in the trajectory
        :param control_points: (numpy array)
        :param easing: (str) (callable from Easing)
        :return: (numpy ndarray) [[x y], [x y], ... [x y]]
        """
        if easing is None or not callable(easing):
            easing = lambda n, *_, **__: n

        np_arr = np.array([cls.bezier(easing(t, *args, **kwargs), control_points)
                           for t in np.linspace(0, 1, int(n_points))])
        return np.concatenate(([control_points[0]], np_arr, [control_points[-1]]))


if __name__ == '__main__':
    from time import sleep
    from pynput.mouse import Controller  # pip install pynput
    from easing import Easing

    mouse = Controller()  # pynput

    easing = Easing()
    easing = getattr(easing, np.random.choice(dir(easing)))  # randomly choose easing method
    print(f"chosen easing: {easing.__name__}")

    cur_x, cur_y = mouse.position   # pynput:  get mouse-pointer position
    points = np.array([[cur_x, cur_y], [800, 800], [200, 200]])  # control points

    for pos in Bezier.bezier_path(100, points, easing):
        mouse.position = pos   # pynput:  set mouse-pointer position
        sleep(0.0275)

    sleep(0.2)
    mouse.position = (cur_x, cur_y)   # pynput:  set mouse-pointer position
