from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtWidgets import *
from PyQt5 import uic

import guildParser as GP
import ImageLoad as IML

import pandas
import os

#UI파일 연결
form_class = uic.loadUiType("./src/UI/main.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class MainWindow(QMainWindow, form_class) :
    members = []
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Maple Guild Manager V1.1.0')

        #버튼 객체에 함수 연결
        self.searchBtn.clicked.connect(self.search)
        self.imgBtn.clicked.connect(self.setImage)
        self.saveBtn.clicked.connect(self.exportExel)

        #배경화면 설정
        try:
            qPixmapVar = QPixmap()
            qPixmapVar.load("src/img/background1.png")
            self.background.setPixmap(qPixmapVar)
        except:
            print("background image err")

        #아이콘 설정
        try:
            self.setWindowIcon(QIcon('src/img/icon3.jpg'))
        except:
            print('Icon err')

    def search(self):
        SearchWindow(self)

    def setImage(self):
        self.imload = IML.AppDemo(self)
        self.imload.show()

    def setData(self, members):
        self.members = members
        self.updateTable()

    #members 배열의 정보를 윈도우 테이블에 반영
    def updateTable(self):
        tb = self.table
        tb.clearContents()

        # item = QTableWidgetItem('hello')
        tb.setRowCount(len(self.members))

        # 테이블에 배열 정보대로 출력
        for i in range(len(self.members)):
            # print(members[i])
            name = QTableWidgetItem(self.members[i][0])
            position = QTableWidgetItem(self.members[i][1])
            level = QTableWidgetItem(self.members[i][2])
            mission = QTableWidgetItem(self.members[i][-3])
            suro = QTableWidgetItem(self.members[i][-2])
            flag = QTableWidgetItem(self.members[i][-1])
            tb.setItem(i, 0, name)
            tb.setItem(i, 1, position)
            tb.setItem(i, 2, level)
            tb.setItem(i, 3, mission)
            tb.setItem(i, 4, suro)
            tb.setItem(i, 5, flag)
        print('updated Table')


    def exportExel(self):
        colHeader = []

        if self.table.model().rowCount()==0:
            print('입력된 데이터가 없습니다')
            reply = QMessageBox.question(self, 'nothing', '데이터를 입력 후 저장해주세요', QMessageBox.Yes)
            return;

        # 열의 헤더 리스트
        for i in range(self.table.model().columnCount()):
            colHeader.append(self.table.horizontalHeaderItem(i).text())

        # 데이터프레임 생성
        df = pandas.DataFrame(columns=colHeader)

        for  row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                df.at[row, colHeader[col]] = self.table.item(row, col).text()

        createFolder('scores')
        rename = renameFile("scores/flag_score.csv")
        try:
            df.to_csv(rename, encoding='utf-8-sig', index=False)
            reply = QMessageBox.question(self, '무야호~', '저장이 완료되었습니다', QMessageBox.Yes)
        except OSError:
            print('err')

    #화면 크기에 따른 UI배치의 변화
    def resizeEvent(self, *args, **kwargs):
        self.table.resize(self.width()*0.9, self.height()*0.7)
        self.imgBtn.move(self.width()*0.55,self.height()*0.9)
        self.saveBtn.move(self.width() * 0.75, self.height() * 0.9)


#폴더 생성
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

#중복된 파일 이름 방지위해 새로운 파일명 반환, 파일이름 뒤에 알맞은 숫자 추가
def renameFile(fpath):
    try:
        n=0
        rename = fpath
        fname, ext = os.path.splitext(fpath) #경로 및 이름, 확장자
        while os.path.isfile(rename):
            n+=1
            rename = fname+'_'+str(n)+ext
        print(rename)
        return rename
    except OSError:
        print('Error: Creating file. ' + fname)



#길드 검색 화면 클래스
class SearchWindow(QDialog):
    def __init__(self, parent):
        super(SearchWindow, self).__init__(parent)
        guild_search = './src/UI/guild_search.ui'
        uic.loadUi(guild_search, self)
        self.show()

        self.parent = parent

        #이벤트 연결
        self.searchTxt.returnPressed.connect(self.search)
        self.searchBtn.clicked.connect(self.search)
        self.guildList.itemDoubleClicked.connect(self.selected)
        self.getMembers.clicked.connect(self.selected)

        #리스트트리 루트 설정
        self.root = self.guildList.invisibleRootItem()

    #길드 검색
    def search(self):
        guildName = self.searchTxt.text()
        self.guildList.clear()

        #길드 검색
        self.searched = GP.search(guildName)

        #길드 리스트에 추가
        for guild in self.searched:
            item = QTreeWidgetItem()
            item.setText(0, guild[2])
            item.setText(1, guildName)
            item.setText(2, guild[1])
            self.root.addChild(item)
            #print(guild)

    #길드 선택
    def selected(self):
        #현재 선택된 항목의 인덱스
        current = self.guildList.currentItem()
        index = self.guildList.indexOfTopLevelItem(current)
        #print(self.searched[index])
        code = self.searched[index][0]
        reply = QMessageBox.question(self, '아잉의 경고', '정말로 길드원 정보를 불러오시겠습니까? '
                                                      '\n (저장되지 않은 정보는 초기화 됩니다)',
                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            members = GP.find_all_page(code)
            self.parent.setData(members)
            self.close()
        else:
            print('do nothing')
