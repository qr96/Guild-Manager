# 메이플 길드 관리 도구
import sys

from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import *
import GUI

if __name__ == "__main__" :

    app = QApplication(sys.argv)

    fontDB = QFontDatabase()
    fontDB.addApplicationFont("./src/font/NanumGothic Light.ttf")
    app.setFont(QFont("NanumGothic Light"))

    mainWindow = GUI.MainWindow()
    mainWindow.show()
    app.exec_()
