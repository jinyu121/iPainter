# -*- coding: utf-8 -*-

import numpy as np
from .base_tool import BaseTool
from algorithms.algorithm_bresenham import Bresenham


class ToolEraser(BaseTool):
    is_keep = True
    tool_name = "橡皮"

    def __init__(self):
        super(ToolEraser, self).__init__()

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
        y0 = environment.point_old.x()
        x0 = environment.point_old.y()
        y1 = environment.point_now.x()
        x1 = environment.point_now.y()
        color = [environment.background_color.red() / 255,
                 environment.background_color.green() / 255,
                 environment.background_color.blue() / 255]

        return Bresenham.draw_line(np.array(image),
                                   x0=x0, y0=y0,
                                   x1=x1, y1=y1,
                                   max_x=environment.paper.height(),
                                   max_y=environment.paper.width(),
                                   color=color)
