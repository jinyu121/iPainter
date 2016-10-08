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

        # Removing seams horizontally will decrease the height.
        if reduce_shape[0] > 0:
            image = skimage.transform.rotate(image, 90, resize=True)
            image = skimage.transform.seam_carve(image,
                                                 cls.__helper_energy_rgb(image),
                                                 mode='vertical',
                                                 num=reduce_shape[0])
            image = skimage.transform.rotate(image, -90, resize=True)
            if image.shape[0] > new_shape[0]:
                image = image[:new_shape[0], :, :]

        # Removing seams vertically will decrease the width.
        if reduce_shape[1] > 0:
            image = skimage.transform.seam_carve(image,
                                                 cls.__helper_energy_rgb(image),
                                                 mode='vertical',
                                                 num=reduce_shape[1])
        return image
