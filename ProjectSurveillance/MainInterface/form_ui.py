# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QComboBox, QGraphicsView, QGridLayout,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QTabWidget, QToolBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(700, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 671, 521))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.gridLayoutWidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.CameraTab = QWidget()
        self.CameraTab.setObjectName(u"CameraTab")
        self.verticalLayoutWidget_2 = QWidget(self.CameraTab)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(-1, -1, 671, 461))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.graphicsView = QGraphicsView(self.verticalLayoutWidget_2)
        self.graphicsView.setObjectName(u"graphicsView")

        self.verticalLayout_2.addWidget(self.graphicsView)

        self.label = QLabel(self.verticalLayoutWidget_2)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.comboBox = QComboBox(self.verticalLayoutWidget_2)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.verticalLayout_2.addWidget(self.comboBox)

        self.label_2 = QLabel(self.verticalLayoutWidget_2)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.comboBox_2 = QComboBox(self.verticalLayoutWidget_2)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.verticalLayout_2.addWidget(self.comboBox_2)

        self.tabWidget.addTab(self.CameraTab, "")
        self.MapTab = QWidget()
        self.MapTab.setObjectName(u"MapTab")
        self.verticalLayoutWidget = QWidget(self.MapTab)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 671, 491))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.MapWebView = QWebEngineView(self.verticalLayoutWidget)
        self.MapWebView.setObjectName(u"MapWebView")
        self.MapWebView.setUrl(QUrl(u"about:blank"))

        self.verticalLayout.addWidget(self.MapWebView)

        self.MapRestart = QPushButton(self.verticalLayoutWidget)
        self.MapRestart.setObjectName(u"MapRestart")

        self.verticalLayout.addWidget(self.MapRestart)

        self.tabWidget.addTab(self.MapTab, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.ToolBarArea.RightToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Choose Drone Serial", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Serial 11520", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Serial 9600", None))

        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Choose Camera Input", None))
        self.comboBox_2.setItemText(0, QCoreApplication.translate("MainWindow", u"Camera 1", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("MainWindow", u"Camera 2", None))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.CameraTab), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.MapRestart.setText(QCoreApplication.translate("MainWindow", u"Restart", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.MapTab), QCoreApplication.translate("MainWindow", u"Tab 2", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

