# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

import skimage.io
import numpy as np
import skimage.filters
import os.path
import math
import skimage.draw
import numba
import random


class SeamCarving:
    @classmethod
    def __helper_energy_rgb(cls, image_rgb):
        ans = np.zeros(image_rgb.shape[:2], dtype=np.float)
        # 每个通道分别计算
        for i in range(0, image_rgb.shape[2]):
            ans += cls.__helper_energy_gray(image_rgb[:, :, i])
        # 补个边
        ans[0, :] = 1
        ans[-1, :] = 1
        ans[:, 0] = 1
        ans[:, -1] = 1
        return ans

    @classmethod
    def __helper_energy_gray(cls, image_gray):
        # 由于找不到imfilter，只能使用prewitt这个比较像的东西了
        energy_gray = np.abs(skimage.filters.prewitt(image_gray))
        return energy_gray

    @classmethod
    def __helper_find_route(cls, map_trace, initial_position):
        route = np.zeros(map_trace.shape[0], dtype=np.integer)
        past = initial_position

        for ith in range(map_trace.shape[0] - 1, -1, -1):
            route[ith] = past
            past = past + map_trace[ith][past]
            # route.reverse()
        return route

    @classmethod
    def __helper_find_carving_route(cls, image, ith):
        energy = cls.__helper_energy_rgb(image)
        image_shape = energy.shape
        map_sum = np.zeros(image_shape, dtype=np.float)
        map_trace = np.zeros(image_shape, dtype=np.int8)

        map_sum[0] = energy[0]
        for i in range(1, image_shape[0]):
            # 初始化一行
            temp_sum = np.vstack([energy[i], energy[i], energy[i]])
            # 左边的
            temp_sum[0, 1:] += map_sum[i - 1, : - 1]
            # 上面的
            temp_sum[1, :] += map_sum[i - 1, :]
            # 右边的
            temp_sum[2, : - 1] += map_sum[i - 1, 1:]
            # 单独处理左上角和右下角
            temp_sum[0, 0] += map_sum[i - 1, 0]
            temp_sum[2, - 1] += map_sum[i - 1, -1]
            # 从哪里来最小？
            map_trace[i] = temp_sum.argmin(axis=0)
            # 最小值是多少？
            map_sum[i] = temp_sum.min(axis=0)

        # 将(0,1,2)转变为(-1,0,1)
        map_sum -= 1
        # 找到最小值所在地
        map_sum_last = map_sum[-1, :]
        map_sum_sort = map_sum_last.argsort()

        map_trace[:, 0] = np.max(map_trace[:, 0], 0)
        map_trace[:, -1] = np.min(map_trace[:, -1], 0)

        if not isinstance(ith, int):
            total_min = np.sum(map_sum_last == map_sum_last.min())
            ith = random.randint(0, total_min)

        # 找到路径
        route = cls.__helper_find_route(map_trace, map_sum_sort[ith])
        return route

    @classmethod
    def __helper_make_image_mask(cls, image_shape, carving_route):
        image_mask = np.zeros((image_shape[0], image_shape[1], 3), dtype=np.bool)
        # 制作一个多边形
        image_mask_rows = np.append(np.array(0), np.arange(image_shape[0]))
        image_mask_rows = np.append(image_mask_rows, image_shape[0])
        image_mask_rows = np.append(image_mask_rows, np.array(0))

        image_mask_cols = np.append(np.array(0), carving_route.copy())
        image_mask_cols = np.append(image_mask_cols, np.array(0))
        image_mask_cols = np.append(image_mask_cols, np.array(0))
        # 将多边形变成Mask
        mask_polygon_x, mask_polygon_y = skimage.draw.polygon(image_mask_rows,
                                                              image_mask_cols,
                                                              shape=image_mask.shape)
        image_mask[mask_polygon_x, mask_polygon_y, :] = True
        # image_mask[:, :, 1] = image_mask[:, :, 0]
        # image_mask[:, :, 2] = image_mask[:, :, 0]
        return image_mask

    @classmethod
    def __helper_make_trace_mask(cls, image_shape, carving_route):
        trace_mask = np.zeros((image_shape[0], image_shape[1], 3), dtype=np.bool)
        # 制作一个多边形
        trace_mask[np.arange(image_shape[0]), carving_route, :] = True
        return trace_mask

    @classmethod
    @numba.jit()
    def __helper_do_carving(cls, image, carving_route, is_decrease):
        # 本函数只增减宽度
        old_shape = list(image.shape)
        new_shape = old_shape.copy()

        if is_decrease:
            new_shape[1] -= 1
        else:
            new_shape[1] += 1

        image_new = np.zeros(new_shape, dtype=np.float)

        # 顺手制作一个 image mask 用于加快计算速度
        image_mask = cls.__helper_make_image_mask(old_shape, carving_route)
        trace_mask = cls.__helper_make_trace_mask(old_shape, carving_route)
        # 掩模
        image_masked_left = image * image_mask
        image_masked_right = image * (~image_mask)
        image_masked_trace = image * trace_mask
        # 填充
        if is_decrease:
            image_new[:, :, :] = image_masked_left[:, :-1, :]
            # image_new[:, :, :] -= image_masked_trace[:, :-1, :]
            image_new[:, :, :] += image_masked_right[:, :-1, :]
        else:
            image_new[:, :-1, :] = image_masked_left[:, :, :]
            image_new[:, :-1, :] += image_masked_trace[:, :, :]
            image_new[:, 1:, :] += image_masked_right[:, :, :]
        return image_new

    @classmethod
    @numba.jit()
    def __seam_carving(cls, image, num):
        # 本函数只增减宽度
        is_decrease = num < 0
        num = abs(num)

        # 分批进行计算（特别是用于__增加__宽度的时候）
        total_width = image.shape[1]
        batch_size = total_width // 3
        batch_num = math.ceil(num / batch_size)
        batches = ([batch_size] * (batch_num - 1)) + [num - batch_size * (batch_num - 1)]
        for one_batch in batches:
            for i in range(one_batch):
                if is_decrease:
                    carving_route = cls.__helper_find_carving_route(image, 'random')
                else:
                    carving_route = cls.__helper_find_carving_route(image, (i - 1) * 2)
                image = cls.__helper_do_carving(image, carving_route, is_decrease)
        return image

    @classmethod
    @numba.jit()
    def seam_carving(cls, image, new_shape):
        # Shape为“(高度,宽度)”
        reduce_shape = np.array(new_shape) - image.shape[:2]

        if reduce_shape[0] != 0:
            image = np.transpose(image, (1, 0, 2))
            image = cls.__seam_carving(image, num=reduce_shape[0])
            image = np.transpose(image, (1, 0, 2))
        if reduce_shape[1] != 0:
            image = cls.__seam_carving(image, num=reduce_shape[1])

        return image
