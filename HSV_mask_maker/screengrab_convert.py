#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# screengrab_convert.py

# pypi.org/project/numpy/
import numpy as np

# pypi.org/project/opencv-python/
try:
    import cv2.cv2 as cv
except ImportError:
    import cv2 as cv


def bytes_to_cv(data: bytes, flag: cv = cv.IMREAD_ANYCOLOR) -> np.ndarray:
    np_png_arr = np.frombuffer(data, dtype=np.uint8)  # make array from bytes
    return_val: np.ndarray = cv.imdecode(np_png_arr, flag)  # array to img
    return return_val


def cv_to_bytes(cv2arr: np.ndarray, ext: str = '.png') -> bytes:
    ext = ext if ext.startswith('.') else '.{0}'.format(ext)
    _, buf = cv.imencode(ext, cv2arr)  # 1 dimension array
    return_val: bytes = buf.tobytes()  # change array to bytes
    return return_val
