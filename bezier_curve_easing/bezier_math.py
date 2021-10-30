#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# bezier_math.py

from typing import Callable, Iterable, Tuple, Collection
import math

# https://en.wikipedia.org/wiki/B%C3%A9zier_curve

__all__ = ["Bezier"]


class Bezier:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __dir__(self):
        """ return all the easing methods in this class if dir(Bezier()) is used """
        _dir = ["binomial", "bernstein_poly", "bezier", "bezier_path"]
        return _dir

    @staticmethod
    def binomial(i, n) -> float:
        """Binomial coefficient"""
        return math.factorial(n) / float(math.factorial(i) * math.factorial(n - i))

    @classmethod
    def bernstein_poly(cls, t, i, n) -> float:
        """Bernstein polynom"""
        return cls.binomial(i, n) * (t ** i) * ((1 - t) ** (n - i))

    @classmethod
    def bezier(cls, t, points) -> Tuple[float, float]:
        """Calculate coordinate of a point in the bezier curve"""
        n = len(points) - 1
        x = y = 0
        for i, (pos_x, pos_y) in enumerate(points):
            bern = cls.bernstein_poly(t, i, n)
            x += pos_x * bern
            y += pos_y * bern
        return x, y

    @classmethod
    def bezier_path(cls,
                    n_points: int,
                    points: Collection[Tuple[int, int]],
                    easing: Callable[[float], float] = None
                    ) -> Iterable[Tuple[float, float]]:
        """Compute bezier path (trajectory) given control points"""
        if easing is None or not callable(easing):
            easing = lambda n: n
        linspace = (t / (n_points - 1) for t in range(n_points))
        yield from (cls.bezier(easing(t), points) for t in linspace)


if __name__ == '__main__':
    from time import sleep
    from random import choice
    from pynput.mouse import Controller  # pip install pynput
    from easing import Easing

    mouse = Controller()  # pynput

    easing = Easing()
    easing = getattr(easing, choice(dir(easing)))  # randomly choose easing method
    print(f"chosen easing: {easing.__name__}")

    cur_x, cur_y = mouse.position  # pynput:  get mouse-pointer position
    points = ((cur_x, cur_y), (800, 800), (200, 200))  # control points

    for pos in Bezier.bezier_path(100, points, easing):
        mouse.position = pos  # pynput:  set mouse-pointer position
        sleep(0.0275)

    sleep(0.2)
    mouse.position = (cur_x, cur_y)  # pynput:  set mouse-pointer position
