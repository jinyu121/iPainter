# -*- coding: utf-8 -*-

import numpy as np
from .base_tool import BaseTool
from algorithms.algorithm_bresenham import Bresenham


class ToolLine(BaseTool):
    is_keep = False
    tool_name = "直线"

    def __init__(self):
        super(ToolLine, self).__init__()

    @classmethod
    def draw(cls, image, environment):
        """
                使用Bresenham算法，从点A到点B，用颜色C画一条粗细为R的直线
                :param
                    image: numpy 3d-array
                :param
                    environment:
                :return:
                    numpy 3d-array
                """
        y0 = environment.point_start.x()
        x0 = environment.point_start.y()
        y1 = environment.point_now.x()
        x1 = environment.point_now.y()
        color = [environment.foreground_color.red() / 255,
                 environment.foreground_color.green() / 255,
                 environment.foreground_color.blue() / 255]

        return Bresenham.draw_line(np.array(image),
                                   x0=x0, y0=y0,
                                   x1=x1, y1=y1,
                                   max_x=environment.paper.height(),
                                   max_y=environment.paper.width(),
                                   color=color)
