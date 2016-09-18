# -*- coding: utf-8 -*-

import numpy as np
from .base_tool import BaseTool
from algorithms.algorithm_bresenham import Bresenham


class ToolCircle(BaseTool):
    is_keep = False
    tool_name = "椭圆"

    def __init__(self):
        super(ToolCircle, self).__init__()

    @classmethod
    def draw(cls, image, environment):
        yc = environment.point_start.x()
        xc = environment.point_start.y()
        b = np.abs(environment.point_now.x() - environment.point_start.x())
        a = np.abs(environment.point_now.y() - environment.point_start.y())
        color = [environment.foreground_color.red(),
                 environment.foreground_color.green(),
                 environment.foreground_color.blue()]

        return Bresenham.draw_ellipse(np.array(image),
                                      xc=xc, yc=yc,
                                      a=a, b=b,
                                      max_x=environment.paper.height(),
                                      max_y=environment.paper.width(),
                                      color=color)
