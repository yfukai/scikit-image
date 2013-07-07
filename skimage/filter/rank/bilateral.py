"""Approximate bilateral rank filter for local (custom kernel) mean.

The local histogram is computed using a sliding window similar to the method
described in [1]_.

The pixel neighborhood is defined by:

* the given structuring element
* an interval [g-s0, g+s1] in greylevel around g the processed pixel greylevel

The kernel is flat (i.e. each pixel belonging to the neighborhood contributes
equally).

References
----------

.. [1] Huang, T. ,Yang, G. ;  Tang, G.. "A fast two-dimensional
       median filtering algorithm", IEEE Transactions on Acoustics, Speech and
       Signal Processing, Feb 1979. Volume: 27 , Issue: 1, Page(s): 13 - 18.

"""

import numpy as np
from skimage import img_as_ubyte

from . import bilateral_cy
from .generic import _handle_input


__all__ = ['bilateral_mean', 'bilateral_pop']


def _apply(func, image, selem, out, mask, shift_x, shift_y, s0, s1):

    image, selem, out, mask, max_bin = _handle_input(image, selem, out, mask)

    func(image, selem, shift_x=shift_x, shift_y=shift_y, mask=mask,
         out=out, max_bin=max_bin, s0=s0, s1=s1)

    return out


def bilateral_mean(image, selem, out=None, mask=None, shift_x=False,
                   shift_y=False, s0=10, s1=10):
    """Apply a flat kernel bilateral filter.

    This is an edge-preserving and noise reducing denoising filter. It averages
    pixels based on their spatial closeness and radiometric similarity.

    Spatial closeness is measured by considering only the local pixel
    neighborhood given by a structuring element (selem).

    Radiometric similarity is defined by the greylevel interval [g-s0, g+s1]
    where g is the current pixel greylevel. Only pixels belonging to the
    structuring element AND having a greylevel inside this interval are
    averaged. Return greyscale local bilateral_mean of an image.

    Parameters
    ----------
    image : ndarray (uint8, uint16)
        Image array.
    selem : ndarray
        The neighborhood expressed as a 2-D array of 1's and 0's.
    out : ndarray (same dtype as input)
        If None, a new array will be allocated.
    mask : ndarray
        Mask array that defines (>0) area of the image included in the local
        neighborhood. If None, the complete image is used (default).
    shift_x, shift_y : int
        Offset added to the structuring element center point. Shift is bounded
        to the structuring element sizes (center must be inside the given
        structuring element).
    s0, s1 : int
        Define the [s0, s1] interval around the greyvalue of the center pixel
        to be considered for computing the value.

    Returns
    -------
    out : ndarray (same dtype as input image)
        Output image.

    See also
    --------
    skimage.filter.denoise_bilateral for a gaussian bilateral filter.

    Examples
    --------
    >>> from skimage import data
    >>> from skimage.morphology import disk
    >>> from skimage.filter.rank import bilateral_mean
    >>> # Load test image / cast to uint16
    >>> ima = data.camera().astype(np.uint16)
    >>> # bilateral filtering of cameraman image using a flat kernel
    >>> bilat_ima = bilateral_mean(ima, disk(20), s0=10,s1=10)

    """

    return _apply(bilateral_cy._mean, image, selem, out=out,
                  mask=mask, shift_x=shift_x, shift_y=shift_y, s0=s0, s1=s1)


def bilateral_pop(image, selem, out=None, mask=None, shift_x=False,
                  shift_y=False, s0=10, s1=10):
    """Return the number (population) of pixels actually inside the bilateral
    neighborhood, i.e. being inside the structuring element AND having a gray
    level inside the interval [g-s0, g+s1].

    Parameters
    ----------
    image : ndarray (uint8, uint16)
        Image array.
    selem : ndarray
        The neighborhood expressed as a 2-D array of 1's and 0's.
    out : ndarray (same dtype as input)
        If None, a new array will be allocated.
    mask : ndarray
        Mask array that defines (>0) area of the image included in the local
        neighborhood. If None, the complete image is used (default).
    shift_x, shift_y : int
        Offset added to the structuring element center point. Shift is bounded
        to the structuring element sizes (center must be inside the given
        structuring element).
    s0, s1 : int
        Define the [s0, s1] interval around the greyvalue of the center pixel
        to be considered for computing the value.

    Returns
    -------
    out : ndarray (same dtype as input image)
        Output image.

    Examples
    --------
    >>> # Local mean
    >>> from skimage.morphology import square
    >>> import skimage.filter.rank as rank
    >>> ima16 = 255 * np.array([[0, 0, 0, 0, 0],
    ...                         [0, 1, 1, 1, 0],
    ...                         [0, 1, 1, 1, 0],
    ...                         [0, 1, 1, 1, 0],
    ...                         [0, 0, 0, 0, 0]], dtype=np.uint16)
    >>> rank.bilateral_pop(ima16, square(3), s0=10,s1=10)
    array([[3, 4, 3, 4, 3],
           [4, 4, 6, 4, 4],
           [3, 6, 9, 6, 3],
           [4, 4, 6, 4, 4],
           [3, 4, 3, 4, 3]], dtype=uint16)

    """

    return _apply(bilateral_cy._pop, image, selem, out=out,
                  mask=mask, shift_x=shift_x, shift_y=shift_y, s0=s0, s1=s1)
