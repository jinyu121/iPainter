# -*- coding: utf-8 -*-

import numpy as np
from .base_filter import BaseFilter
import skimage.filters


class FilterGaussianBlur(BaseFilter):
    filter_name = "模糊效果"

    def __init__(self):
        super(FilterGaussianBlur, self).__init__()

    @classmethod
    def render(cls, image, environment):
        image = skimage.img_as_float(image)
        sigma = environment.slider_stroke_width_select.value() / environment.slider_stroke_width_select.maximum()
        sigma = min(sigma, 0.99)
        sigma = max(sigma, 0.01)
        image = skimage.filters.gaussian(image, sigma, multichannel=False)
        return image
