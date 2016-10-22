# -*- coding: utf-8 -*-

import numpy as np
from .base_filter import BaseFilter
import skimage.restoration


class FilterWienerDeblurring(BaseFilter):
    filter_name = "去模糊效果"

    def __init__(self):
        super(FilterWienerDeblurring, self).__init__()

    @classmethod
    def render(cls, image, environment):
        image = skimage.img_as_ubyte(image)
        psf = np.ones((5, 5, 3))
        image[:, :, 0] = skimage.restoration.unsupervised_wiener(image[:, :, 0], psf)
        image[:, :, 1] = skimage.restoration.unsupervised_wiener(image[:, :, 1], psf)
        image[:, :, 2] = skimage.restoration.unsupervised_wiener(image[:, :, 2], psf)
        return image
