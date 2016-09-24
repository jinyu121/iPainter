# -*- coding: utf-8 -*-


class BaseFilter:
    """
    滤镜基类
    """
    filter_name = "未知滤镜或效果"

    def __init__(self):
        pass

    @classmethod
    def render(cls, image, environment):
        pass
