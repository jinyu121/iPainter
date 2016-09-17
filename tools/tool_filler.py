# -*- coding: utf-8 -*-

import numpy as np
from .base_tool import BaseTool
from algorithms.algorithm_floodfill import FloodFill


class ToolFiller(BaseTool):
    is_keep = True
    tool_name = "填充"

    def __init__(self):
        super(ToolFiller, self).__init__()

    @classmethod
    def draw(cls, image, environment):
        color = [environment.foreground_color.red(),
                 environment.foreground_color.green(),
                 environment.foreground_color.blue()]
        return FloodFill.fill(np.array(image),
                              x=environment.point_now.y(),
                              y=environment.point_now.x(),
                              max_x=environment.paper.height(),
                              max_y=environment.paper.width(),
                              color=color)
