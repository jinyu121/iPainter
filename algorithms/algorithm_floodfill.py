# -*- coding: utf-8 -*-

import numpy as np
import queue


class FloodFill:
    @classmethod
    def fill(cls, image, x, y, max_x, max_y, color):
        if not (0 <= x < max_x and 0 <= y < max_y):
            return image

        color_now = np.array(image[x, y, :])
        if (color_now == color).all():
            return image

        direction = np.array([[1, 0, -1, 0],
                              [0, 1, 0, -1]])
        image = np.array(image)
        visited = np.zeros(image.shape[:2], dtype=np.bool)
        q = queue.Queue()
        q.put((x, y))
        visited[x, y] = True

        while not q.empty():
            p = q.get()
            image[p[0], p[1], :] = color
            for ind in range(4):
                xx = p[0] + direction[0][ind]
                yy = p[1] + direction[1][ind]
                if 0 <= xx < max_x and 0 <= yy < max_y:
                    if not visited[xx, yy]:
                        visited[xx, yy] = True
                        if (image[xx, yy, :] == color_now).all():
                            q.put((xx, yy))

        return image

    @classmethod
    def fill_scan_line(cls, image, x, y, max_x, max_y, color):

        return image
