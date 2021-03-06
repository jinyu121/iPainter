# -*- coding: utf-8 -*-

import numpy as np
from .base_tool import BaseTool
from algorithms.algorithm_bresenham import Bresenham
from common.utils import q_color_ro_rgb


class ToolPencil(BaseTool):
    """
    铅笔类
    鼠标移动过程中，轨迹直接作为输出
    """
    is_keep = True
    tool_name = "铅笔"

    def __init__(self):
        super(ToolPencil, self).__init__()

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

        # 目前暂时不管粗细
        y1 = environment.point_now.x()
        x1 = environment.point_now.y()
        y0 = environment.point_old.x()
        x0 = environment.point_old.y()

        color = q_color_ro_rgb(environment.foreground_color)

        return Bresenham.draw_line(np.array(image),
                                   x0=x0, y0=y0,
                                   x1=x1, y1=y1,
                                   max_x=environment.paper.height(),
                                   max_y=environment.paper.width(),
                                   color=color)
