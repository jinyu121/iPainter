# -*- coding: utf-8 -*-

import numpy as np
from .base_tool import BaseTool


class ToolText(BaseTool):
    is_keep = True
    tool_name = "文字"

    def __init__(self):
        super(ToolText, self).__init__()

    @classmethod
    def draw(cls, image, environment):
        return image
