# -*- coding: utf-8 -*-

import PyQt5.uic
import os
from functools import reduce
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap


def load_ui(file_path):
    """
    Load ui from .ui file
    :param
        file_path: list
    :return:
        class_ui: QObject
        class_basic_class: QObject
    """
    ui_path = reduce((lambda pre, now: os.path.join(pre, now)), file_path)
    return PyQt5.uic.loadUiType(os.path.join(ui_path))


def numpy_image_2_qt_image(image):
    """

    :param image:
        image: numpy ndarray
    :return:
        QPixmap
    """
    image = QImage(image, image.shape[1], image.shape[0], image.shape[1] * image.shape[2], QImage.Format_RGB888)
    return QPixmap(image)


def reflect_get_class(class_full_name):
    """
    Give a class' full name, this function will auto import it, and return the class itself.
    :param class_full_name: string
    :return: class
    """
    parts = class_full_name.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m
