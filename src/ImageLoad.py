import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

import KakaoOCR as OCR
from PIL import ImageGrab

import ArrCompare

#이미지 뷰어 클래스
class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Drop Image Here\n(Ctrl+V) \n\n')
        self.setStyleSheet('''
            QLabel{
                border: 2px dashed #aaa;
                font: 12pt "Bahnschrift SemiLight";
            }
            
        ''')

    def setPixmap(self, image):
        super().setPixmap(image)

#이미지 호출 버튼 클래스
class LoadImage(QPushButton):
    def __init__(self):
        super().__init__()

        self.setText('Load Image')

#이미지 로드의 메인 화면
class AppDemo(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.resize(300, 300)
        self.setWindowTitle("이미지를 추가하세요")
        self.setAcceptDrops(True)
        self.file_path = ""
        self.parent = parent
        self.setStyleSheet('''
                    QWidget {
                        background-color: rgb(240, 240, 255);
                    }
                ''')

        mainLayout = QVBoxLayout()

        #뷰어
        self.photoviewer = ImageLabel()
        mainLayout.addWidget((self.photoviewer))

        #이미지 호출 버튼
        self.loadBtn = LoadImage()
        self.loadBtn.setStyleSheet('''
            QPushButton {
                background-color: rgb(240, 240, 255);
	            border: 1px solid rgb(225, 225, 235);
	            height: 30px;
            }
            QPushButton::hover {
                background-color: rgb(230, 230, 250);
	            border: 2px solid rgb(245, 245, 255);
            }
        ''')
        self.loadBtn.clicked.connect(self.load_image)
        mainLayout.addWidget((self.loadBtn))

        self.setLayout(mainLayout)

    #이미지 드래그 앤 드롭 함수들
    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            self.file_path = event.mimeData().urls()[0].toLocalFile()
            self.set_image(self.file_path)

            event.accept()
        else:
            event.ignore()

    def set_image(self, file_path):
        self.photoviewer.setPixmap(QPixmap(file_path))

    def load_image(self):
        if self.file_path == "": return
        elif len(self.parent.members) == 0:
            reply = QMessageBox.question(self, '아잉의 경고', "길드 정보를 불러온 후 실행해 주세요", QMessageBox.Yes)

        try:
            img_path = self.file_path
            members = OCR.test(img_path)
            conv = ArrCompare.compare(members, self.parent.members)
            self.parent.setData(conv)
            self.close()
        except:
            print("err")

    #Ctrl + V 함수들
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Control:
            self.ctrl_flag = True

        if e.key() == Qt.Key_V and self.ctrl_flag == True:
            try:
                img = ImageGrab.grabclipboard()
                img.save('captured.png', 'png')
                self.file_path = 'captured.png'
                self.set_image(self.file_path)
                print('Crtl + V')
            except:
                print('err')

    def keyReleaseEvent(self, e):
        if e.key() == Qt.Key_Control:
            self.ctrl_flag = False


#테스트 실행용 함수
def exec():
    app = QApplication(sys.argv)
    demo = AppDemo()
    demo.show()
    sys.exit(app.exec_())


