# -*- coding: utf-8 -*-


class BaseTool:
    """
    工具基类
    """
    # 是否在移动过程中就直接作为最终输出
    is_keep = False
    tool_name = "未知工具"

    def __init__(self):
        pass

    @classmethod
    def draw(cls, image, environment):
        return image
