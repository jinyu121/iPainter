# -*- coding: utf-8 -*-

import numpy as np
from .base_tool import BaseTool


class ToolAirbrush(BaseTool):
    is_keep = True
    tool_name = "喷笔"

    def __init__(self):
        super(ToolAirbrush, self).__init__()

    @classmethod
    def draw(cls, image, environment):
        return image
