# -*- coding: utf-8 -*-

import numpy as np
from .base_tool import BaseTool
from common.utils import q_color_ro_rgb


class ToolAirbrush(BaseTool):
    is_keep = True
    tool_name = "喷笔"

    def __init__(self):
        super(ToolAirbrush, self).__init__()

    @classmethod
    def draw(cls, image, environment):
        image = np.array(image)
        color = q_color_ro_rgb(environment.foreground_color)

        a = environment.point_now.y()
        b = environment.point_now.x()
        max_x = environment.paper.height()
        max_y = environment.paper.width()

        radius = environment.slider_stroke_width_select.value()
        size_cluster = int(radius * np.log(radius))

        raw_data = np.random.randn(2, size_cluster) * radius
        points = np.array([(radius - raw_data[0, 0:size_cluster]) * np.cos(np.pi * raw_data[1, 0:size_cluster]) + a,
                           (radius - raw_data[0, 0:size_cluster]) * np.sin(np.pi * raw_data[1, 0:size_cluster]) + b],
                          dtype=np.int)
        points_index = [ith for ith in range(points.shape[1]) if
                        0 <= points[0, ith] < max_x and 0 <= points[1, ith] < max_y]
        points = points[:, points_index]
        image[points[0], points[1], :] = color

        return image
