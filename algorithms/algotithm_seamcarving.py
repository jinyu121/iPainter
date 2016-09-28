# -*- coding: utf-8 -*-

import skimage.transform
import numpy as np
import skimage.filters


class SeamCarving:
    @classmethod
    def __helper_energy_rgb(cls, image_rgb):
        ans = np.zeros(image_rgb.shape[:2])
        # 每个通道分别计算
        for i in range(0, image_rgb.shape[2]):
            ans += cls.__helper_energy_gray(image_rgb[:, :, i])
        return ans

    @classmethod
    def __helper_energy_gray(cls, image_gray):
        # 由于找不到imfilter，只能使用prewitt这个比较像的东西了
        return np.abs(skimage.filters.prewitt(image_gray))

    @classmethod
    def seam_carving(cls, image, new_shape):
        reduce_shape = image.shape[:2] - np.array(new_shape)
        direction = ['horizontal', 'vertical']
        for i in range(len(direction)):
            if reduce_shape[i] > 0:
                image = skimage.transform.seam_carve(image,
                                                     cls.__helper_energy_rgb(image),
                                                     mode=direction[i],
                                                     num=reduce_shape[i])
        return image
