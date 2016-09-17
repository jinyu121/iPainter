# -*- coding: utf-8 -*-

import numpy as np


class Bresenham:
    @classmethod
    def draw_line(cls, image, x0, y0, x1, y1, max_x, max_y, color):
        # 画端点
        image = cls.__helper_point1(image, x0, y0, max_x, max_y, color)
        image = cls.__helper_point1(image, x1, y1, max_x, max_y, color)
        # 画连接点
        steep = np.abs(y1 - y0) > np.abs(x1 - x0)
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        delta_x = x1 - x0
        delta_y = np.abs(y1 - y0)
        error = delta_x / 2
        y = y0
        y_step = 1 if y0 < y1 else -1
        for x in range(x0, x1):
            if steep:
                x_true, y_true = y, x
            else:
                x_true, y_true = x, y

            image = cls.__helper_point1(image, x_true, y_true, max_x, max_y, color)

            error = error - delta_y
            if error < 0:
                y += y_step
                error += delta_x
        return image

    @classmethod
    def draw_ellipse(cls, image, xc, yc, a, b, max_x, max_y, color):
        sqa = np.power(a, 2)
        sqb = np.power(b, 2)
        x = 0
        y = b
        d = 2 * sqb - 2 * b * sqa + sqa
        image = cls.__helper_point4(image, xc, yc, x, y, max_x, max_y, color)
        P_x = np.round(sqa / np.sqrt(sqa + sqb))
        while x <= P_x:
            if d < 0:
                d += 2 * sqb * (2 * x + 3)
            else:
                d += 2 * sqb * (2 * x + 3) - 4 * sqa * (y - 1)
                y -= 1
            x += 1
            image = cls.__helper_point4(image, xc, yc, x, y, max_x, max_y, color)
        d = sqb * (x * x + x) + sqa * (y * y - y) - sqa * sqb
        while y >= 0:
            image = cls.__helper_point4(image, xc, yc, x, y, max_x, max_y, color)
            y -= 1
            if d < 0:
                x += 1
                d = d - 2 * sqa * y - sqa + 2 * sqb * x + 2 * sqb
            else:
                d = d - 2 * sqa * y - sqa
        return image

    @classmethod
    def __helper_point1(cls, image, x, y, max_x, max_y, color):
        if 0 <= x < max_x and 0 <= y < max_y:
            image[x, y, :] = color
        return image

    @classmethod
    def __helper_point4(cls, image, xc, yc, dx, dy, max_x, max_y, color):
        for op_x in [-1, 1]:
            for op_y in [-1, 1]:
                x = xc + op_x * dx
                y = yc + op_y * dy
                if 0 <= x < max_x and 0 <= y < max_y:
                    image[x, y, :] = color
        # if 0 <= xc + dx < max_x and 0 <= yc + dy < max_y:
        #     image[xc + dx, yc + dy, :] = color
        # if 0 <= xc - dx < max_x and 0 <= yc + dy < max_y:
        #     image[xc - dx, yc + dy, :] = color
        # if 0 <= xc - dx < max_x and 0 <= yc - dy < max_y:
        #     image[xc - dx, yc - dy, :] = color
        # if 0 <= xc + dx < max_x and 0 <= yc - dy < max_y:
        #     image[xc + dx, yc - dy, :] = color

        return image
