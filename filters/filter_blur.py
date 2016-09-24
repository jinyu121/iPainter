# -*- coding: utf-8 -*-

import numpy as np
from .base_filter import BaseFilter
import skimage.filters


class FilterBlur(BaseFilter):
    filter_name = "模糊效果"

    def __init__(self):
        super(FilterBlur, self).__init__()

    @classmethod
    def render(cls, image, environment):
        image = skimage.img_as_float(image)
        image = skimage.filters.gaussian(image, 0.8, multichannel=False)
        image = skimage.img_as_ubyte(image)
        return image
