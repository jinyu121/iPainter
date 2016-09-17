# -*- coding: utf-8 -*-

import numpy as np
from .base_tool import BaseTool
from algorithms.algorithm_bresenham import Bresenham


class ToolRectangle(BaseTool):
    is_keep = False
    tool_name = "矩形"

    def __init__(self):
        super(ToolRectangle, self).__init__()

    @classmethod
    def draw(cls, image, environment):
        """
                使用Bresenham算法，从点A到点B，用颜色C画四条粗细为R的直线，组成一个矩形
                :param
                    image: numpy 3d-array
                :param
                    environment:
                :return:
                    numpy 3d-array
                """
        y1 = environment.point_now.x()
        x1 = environment.point_now.y()
        y0 = environment.point_start.x()
        x0 = environment.point_start.y()

        max_x = environment.paper.height()
        max_y = environment.paper.width()

        color = [environment.foreground_color.red(),
                 environment.foreground_color.green(),
                 environment.foreground_color.blue()]
        image = np.array(image)

        image = Bresenham.draw_line(image, x0=x0, y0=y0, x1=x0, y1=y1,
                                    max_x=max_x, max_y=max_y, color=color)
        image = Bresenham.draw_line(image, x0=x0, y0=y0, x1=x1, y1=y0,
                                    max_x=max_x, max_y=max_y, color=color)
        image = Bresenham.draw_line(image, x0=x1, y0=y1, x1=x0, y1=y1,
                                    max_x=max_x, max_y=max_y, color=color)
        image = Bresenham.draw_line(image, x0=x1, y0=y1, x1=x1, y1=y0,
                                    max_x=max_x, max_y=max_y, color=color)
        return image
