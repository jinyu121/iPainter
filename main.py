# -*- coding: utf-8 -*-

import logging
import sys

from PyQt5.QtWidgets import QApplication

from components.windows.mainwindow import MainWindow

if __name__ == '__main__':
    logging.basicConfig(filename='iPaint.log', level=logging.ERROR)
    app = QApplication(sys.argv)
    main_window = MainWindow()

    main_window.show()
    sys.exit(app.exec_())
