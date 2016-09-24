# -*- coding: utf-8 -*-

from common.consts import DIRECTORIES
from common.utils import load_ui
from common.utils import reflect_get_class
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget
import logging
import skimage.io
import skimage.color
import numpy as np
from common.utils import numpy_image_2_qt_image
from PyQt5.QtWidgets import QSizePolicy

# Define the .ui file, and load it.
# We will get the UI class and the base class
ui_file = 'mainwindow.ui'
(class_ui, class_basic_class) = load_ui([DIRECTORIES['UI_BASE_PATH'], ui_file])


# Modifi the UI class
class MainWindow(class_basic_class, class_ui):
    """
    The main window of iPainter
    """

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        # 常量
        self.UNDO_MAX_STEP = 30
        # 初始化参数
        self.paper.setMouseTracking(True)
        self.raw_data = None
        self.raw_data_tmp = None
        self.stroke_width = 1
        self.background_color = QColor(255, 255, 255)
        self.foreground_color = QColor(0, 0, 0)
        self.point_start = None
        self.point_old = None
        self.point_now = None
        self.tool_now = None
        self.action_stack_undo = list()
        self.action_stack_redo = list()
        # 初始化信号槽
        self.__init_connections()
        # 初始化显示
        self.__init_components()

    def __init_connections(self):
        # menu
        self.action__file_open.triggered.connect(self.do_file__open_picture)
        self.action__file_new.triggered.connect(self.do_file__new)
        self.action__file_save.triggered.connect(self.do_file__save_picture)
        self.action__file_quit.triggered.connect(lambda: self.close())
        self.action__action_undo.triggered.connect(self.do_action__undo)
        self.action__action_redo.triggered.connect(self.do_action__redo)
        self.action__filter_blur.triggered.connect(lambda: self.do_filter('blur'))
        # buttons
        self.label_color_foreground_show.clicked.connect(
            lambda: self.set_foreground_color(QColorDialog.getColor(self.foreground_color)))
        self.label_color_background_show.clicked.connect(
            lambda: self.set_background_color(QColorDialog.getColor(self.background_color)))
        self.btn_tool_pencil.clicked.connect(lambda: self.do_switch_tool('pencil'))
        self.btn_tool_eraser.clicked.connect(lambda: self.do_switch_tool('eraser'))
        self.btn_tool_line.clicked.connect(lambda: self.do_switch_tool('line'))
        self.btn_tool_airbrush.clicked.connect(lambda: self.do_switch_tool('airbrush'))
        self.btn_tool_rectangle.clicked.connect(lambda: self.do_switch_tool('rectangle'))
        self.btn_tool_circle.clicked.connect(lambda: self.do_switch_tool('circle'))
        self.btn_tool_filler.clicked.connect(lambda: self.do_switch_tool('filler'))
        self.btn_tool_text.clicked.connect(lambda: self.do_switch_tool('text'))
        # widgets
        self.slider_stroke_width_select.valueChanged.connect(self.do_change_stroke_width)
        self.paper.installEventFilter(self)

    def __init_components(self):
        self.do_file__new()
        self.set_background_color(self.background_color)
        self.set_foreground_color(self.foreground_color)
        self.do_switch_tool('pencil')
        self.statusBar.showMessage('就绪')

    # ========== ========== ==========
    # Events
    # ========== ========== ==========
    def closeEvent(self, event):
        if self.raw_data is None:
            event.accept()
            return

        reply = QMessageBox.question(self, 'Quit?', "确定退出？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            logging.info("System Quit")
            event.accept()
        else:
            event.ignore()

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseMove:
            # 鼠标移动
            # 可能是平常的划过，也可能是正在拖动鼠标
            # 记录“上一个点”
            self.point_old = self.point_now
            # self.point_old = self.point_start
            # 记录“当前点”
            self.point_now = event.pos()
            # 显示到 status bar 上
            self.statusBar.showMessage("({},{})".format(self.point_now.x(), self.point_now.y()))
            # 如果是拖动鼠标，那么做一些东西
            if self.point_start is not None:
                self.do_tool_moving()
        elif event.type() == QEvent.MouseButtonPress:
            # 点击鼠标
            self.point_start = event.pos()
            self.point_now = event.pos()
            self.point_old = event.pos()
            self.confitm_action()
        elif event.type() == QEvent.MouseButtonRelease:
            # 鼠标放开，确认绘图
            self.point_now = event.pos()
            if self.point_old is None:
                self.point_old = event.pos()
            if self.point_start is None:
                self.point_start = event.pos()

            self.do_tool()

            self.point_start = None
            self.point_old = None
        elif event.type() == QEvent.Leave:
            self.statusBar.showMessage("")
        else:
            pass

        return QWidget.eventFilter(self, source, event)

    # ========== ========== ==========
    # Menu
    # ========== ========== ==========

    def do_file__new(self):
        "新建文件"
        self.raw_data = np.ndarray((400, 500, 3), dtype=np.uint8)
        self.raw_data.fill(255)
        self.show_picture()

    def do_file__open_picture(self):
        "打开文件"
        file_name, btn = QFileDialog.getOpenFileName(self, 'Open file')
        if file_name:
            logging.info("Selected file: {}".format(file_name))
            try:
                self.statusBar.showMessage('图片加载中')
                self.raw_data = skimage.img_as_ubyte(skimage.io.imread(file_name))
                logging.info("Read file: {}".format(file_name))
                if 4 == self.raw_data.shape[2]:
                    self.raw_data = skimage.color.rgba2rgb(self.raw_data)
                elif 2 == self.raw_data.shape[2]:
                    self.raw_data = skimage.color.gray2rgb(self.raw_data)

                self.show_picture(self.raw_data)
                self.statusBar.showMessage('图片加载完成')

            except Exception as e:
                logging.error(str(e))
                QMessageBox.warning(self, 'Error', "图片不支持", QMessageBox.Yes)

    def do_filter(self, filter_name):
        pass

    def do_file__save_picture(self):
        "保存文件"
        if self.raw_data is None:
            QMessageBox.warning(self, 'Error', "没有图片可供保存", QMessageBox.Yes)
        else:
            file_name, btn = QFileDialog.getSaveFileName(self, 'Save file')
            if file_name:
                try:
                    skimage.io.imsave(file_name, self.raw_data)
                    self.statusBar.showMessage('图片保存完成')
                except Exception as e:
                    QMessageBox.warning(self, 'Error', "图片保存失败", QMessageBox.Yes)
                    logging.error(str(e))

    def do_action__undo(self):
        "“撤销”动作"
        if len(self.action_stack_undo) > 0:
            self.action_stack_redo.append(self.raw_data)
            self.raw_data = self.action_stack_undo.pop()
            self.show_picture()

    def do_action__redo(self):
        "“重做”动作"
        if len(self.action_stack_redo) > 0:
            self.action_stack_undo.append(self.raw_data)
            self.raw_data = self.action_stack_redo.pop()
            self.show_picture()

    # ========== ========== ==========
    # Tool box
    # ========== ========== ==========


    def do_change_stroke_width(self):
        self.stroke_width = self.slider_stroke_width_select.value()
        self.statusBar.showMessage('画笔宽度：{}'.format(self.stroke_width))

    def do_tool_moving(self):
        self.raw_data_tmp = self.tool_now.draw(self.raw_data, self)
        if self.tool_now.is_keep:
            self.raw_data = self.raw_data_tmp
        self.show_picture(self.raw_data_tmp)

    def do_tool(self):
        "鼠标松开，确认绘图。"
        self.raw_data = self.tool_now.draw(self.raw_data, self)
        self.show_picture(self.raw_data)

    def do_switch_tool(self, tool_name):
        "切换工具"
        tool_full_name = "tools.tool_{}.Tool{}".format(tool_name.lower(), tool_name.capitalize())
        self.tool_now = reflect_get_class(tool_full_name)
        self.statusBar.showMessage('切换到工具：{}'.format(self.tool_now.tool_name))

    # ========== ========== ==========
    # Functions
    # ========== ========== ==========

    def set_background_color(self, color):
        if color.isValid():
            logging.debug("Change background color into {}".format(color.name()))
            self.background_color = color
            self.label_color_background_show.setStyleSheet("QWidget { background-color: %s }" % color.name())
        else:
            logging.error("Color is not valid")

    def set_foreground_color(self, color):
        if color.isValid():
            logging.debug("Change foreground color into {}".format(color.name()))
            self.foreground_color = color
            self.label_color_foreground_show.setStyleSheet("QWidget { background-color: %s }" % color.name())
        else:
            logging.error("Color is not valid")

    def show_picture(self, picture=None):
        "显示图像"
        if picture is None:
            picture = self.raw_data
        self.paper.setFixedWidth(picture.shape[1])
        self.paper.setFixedHeight(picture.shape[0])
        self.paper.setPixmap(numpy_image_2_qt_image(picture))

    def confitm_action(self):
        "当前显示图像压栈"
        self.action_stack_undo.append(self.raw_data)
        if len(self.action_stack_undo) > self.UNDO_MAX_STEP:
            self.action_stack_undo.pop(0)
        self.action_stack_redo = list()
