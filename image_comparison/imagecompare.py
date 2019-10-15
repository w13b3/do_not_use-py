#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# imagecompare.py

import numpy as np


def gaussian2d(shape: tuple = (5,), sigma: tuple = (1.5,)) -> np.ndarray:
    """
    create a gaussian 2d array
    shape and sigma tuples with diferent values can create an asymmetric gauss array
    """
    size_x, size_y = (shape[0], shape[0]) if len(shape) == 1 else shape[:2]
    sigma_x, sigma_y = (sigma[0], sigma[0]) if len(sigma) == 1 else sigma[:2]

    # faster than np.meshgrid
    x = np.arange(0, size_x, dtype=float)
    y = np.arange(0, size_y, dtype=float)[:, np.newaxis]

    x = np.subtract(x, (size_x // 2))
    y = np.subtract(y, (size_y // 2))

    sigma_x_sq = sigma_x ** 2
    sigma_y_sq = sigma_y ** 2

    exp_part = x ** 2 / (2 * sigma_x_sq) + y ** 2 / (2 * sigma_y_sq)
    return 1 / (2 * np.pi * sigma_x * sigma_y) * np.exp(-exp_part)


def convolve_array(arr: np.ndarray, conv_filter: np.ndarray) -> np.ndarray:
    """
    Convolves array with conv_filter, over all channels
    acknowledgement:
    https://songhuiming.github.io/pages/2017/04/16/convolve-correlate-and-image-process-in-numpy/
    """
    if len(arr.shape) <= 2:  # no `depth` and probably 2d array
        return convolve2d(arr, conv_filter)

    arr_stack = []
    for dimension in range(arr.ndim):
        arr_slice = arr[:, :, dimension]
        convolve_dimension = convolve2d(arr_slice, conv_filter)
        arr_stack.append(convolve_dimension)

    return np.stack(arr_stack, axis=2)  # -> np.ndarray


def convolve2d(arr: np.ndarray, conv_filter: np.ndarray) -> np.ndarray:
    """
    convole2d function
    acknowledgement:
    https://stackoverflow.com/users/7567938/allosteric
    """
    if len(arr.shape) > 2:
        raise ValueError("Please input the arr with 2 dimensions")

    view_shape = tuple(np.subtract(arr.shape, conv_filter.shape) + 1) + conv_filter.shape
    as_strided = np.lib.stride_tricks.as_strided
    sub_matrices = as_strided(arr, shape = view_shape, strides = arr.strides * 2)
    return np.einsum('ij,ijkl->kl', conv_filter, sub_matrices.transpose()).transpose()


def structural_similarity(array1: np.ndarray, array2: np.ndarray, filter_size: int = 11, filter_sigma: float = 1.5,
                          k1: float = 0.01, k2: float = 0.03, max_val: int = 255) -> (np.float64, np.ndarray):
    """
    calculates the Structural SIMilarity Index (SSIM)
    returns a score of the image difference -1 to 1 where 1 is identical
            and a diff index array

    grayscale and color images can be used
    color images take more time to calculate

    acknowledgement:
    https://en.wikipedia.org/wiki/Structural_similarity
    https://scikit-image.org/docs/dev/auto_examples/transform/plot_ssim.html
    Zhou Wang: https://github.com/obartra/ssim/blob/master/assets/ssim.pdf
    https://blog.csdn.net/weixin_42096901/article/details/90172534
    https://github.com/tensorflow/models/blob/master/research/compression/image_encoder/msssim.py

    :param array1: pixel value array to compare against `array2`
    :type array1: np.ndarray
    :param array2: pixel value array to compare against `array1`
    :type array2: np.ndarray
    :param filter_size: kernel size for the gaussian blur
    :type filter_size: int
    :param filter_sigma: standard deviation for the gaussian blur
    :type filter_sigma: float
    :param k1: constant for stability
    :type k1: float
    :param k2: constant for stability
    :type k2: float
    :param max_val: dynamic range of the given pixel value array  255 for 8-bit images
    :type max_val:int
    :return: score, diff array
    :rtype: (np.float64, np.ndarray)
    :raises: ValueError if given arrays are not the same shape
    """
    if array1.shape != array2.shape:
        raise ValueError('Input arrays must have the same shape')

    array1 = array1.astype(np.float64)
    array2 = array2.astype(np.float64)
    height, width = array1.shape[:2]

    if filter_size:  # is 1 or more
        # filter size can't be larger than height or width of arrays.
        size = min(filter_size, height, width)

        # scale down sigma if a smaller filter size is used.
        sigma = size * filter_sigma / filter_size if filter_size else 0

        window = gaussian2d(shape=(size,), sigma=(sigma,))
        # compute weighted means
        mu1 = convolve_array(array1, window)
        mu2 = convolve_array(array2, window)

        # compute weighted covariances
        sigma_11 = convolve_array(np.multiply(array1, array1), window)
        sigma_22 = convolve_array(np.multiply(array2, array2), window)
        sigma_12 = convolve_array(np.multiply(array1, array2), window)
    else:  # Empty blur kernel so no need to convolve.
        mu1, mu2 = array1, array2
        sigma_11 = np.multiply(array1, array1)
        sigma_22 = np.multiply(array2, array2)
        sigma_12 = np.multiply(array1, array2)

    # compute weighted variances
    mu_11 = np.multiply(mu1, mu1)
    mu_22 = np.multiply(mu2, mu2)
    mu_12 = np.multiply(mu1, mu2)
    sigma_11 = np.subtract(sigma_11, mu_11)
    sigma_22 = np.subtract(sigma_22, mu_22)
    sigma_12 = np.subtract(sigma_12, mu_12)

    # constants to avoid numerical instabilities close to zero
    c1 = (k1 * max_val) ** 2
    c2 = (k2 * max_val) ** 2
    v1 = 2.0 * sigma_12 + c2
    v2 = sigma_11 + sigma_22 + c2

    # Numerator of SSIM
    num_ssim = (2 * mu_12 + c1) * v1   # -> np.ndarray

    # Denominator of SSIM
    den_ssim = (mu_11 + mu_22 + c1) * v2   # -> np.ndarray

    # SSIM (contrast sensitivity)
    ssim = num_ssim / den_ssim  # -> np.ndarray

    # MeanSSIM
    mssim = np.mean(ssim)  # -> np.float64
    return mssim, ssim  # -> (np.float64, np.ndarray)


def mean_absolute_error(array1, array2):
    return np.abs(np.subtract(array1, array2)).mean()


mae = mean_absolute_error


def mean_squared_error(array1, array2):
    return np.square(np.subtract(array1, array2)).mean()


mse = mean_squared_error


def root_mean_squared_error(array1, array2):
    return np.sqrt(mean_squared_error(array1, array2))


rmse = root_mean_squared_error


if __name__ == '__main__':
    print("start\n")

    import logging
    logging.basicConfig(level=logging.DEBUG)
    # logging.getLogger("logging").setLevel(logging.DEBUG)
    logging.captureWarnings(True)

    blue = np.zeros((100, 100, 3))
    blue[:, :, 0] = 255

    green = np.zeros((100, 100, 3))
    green[:, :, 1] = 255

    red = np.zeros((100, 100, 3))
    red[:, :, 2] = 255

    fill128 = np.zeros((100, 100))
    fill128[:, :, ] = 128

    fill255 = np.zeros((100, 100))
    fill255[:, :, ] = 255

    score, diff = structural_similarity(blue, blue)
    print(f"blue <-> blue score: {score}")

    score, diff = structural_similarity(red, blue)
    print(f"red <-> blue score: {score}")

    score, diff = structural_similarity(red, green)
    print(f"red <-> green score: {score}")

    score, diff = structural_similarity(fill128, fill128)
    print(f"fill128 <-> fill128 score: {score}")

    score, diff = structural_similarity(fill128, fill255)
    print(f"fill128 <-> fill255 score: {score}")
