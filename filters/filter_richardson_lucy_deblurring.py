# -*- coding: utf-8 -*-

import numpy as np
from .base_filter import BaseFilter
import skimage.restoration


class FilterRichardsonLucyDeblurring(BaseFilter):
    filter_name = "去模糊效果"

    def __init__(self):
        super(FilterRichardsonLucyDeblurring, self).__init__()

    @classmethod
    def render(cls, image, environment):
        image = skimage.img_as_float(image)
        width = (environment.slider_stroke_width_select.value() // 10) + 1
        psf = np.ones((5, width, 3))
        image = skimage.restoration.richardson_lucy(image, psf, iterations=10)
        return image
