import PyQt5
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QRegExp
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QLineEdit
from PyQt5 import uic
import sys

import Schedule
import PrimitiveJSONParser
import PrimitiveXMLParser



class MainWindow(QMainWindow):
    def __init__(self):
        super(QWidget, self).__init__()
        uic.loadUi("MainWindow.ui", self)
        self.setValidator()
        self.downloadSchedule.clicked.connect(self.setReadable)
        self.download.clicked.connect(self.downloadS)
        self.Convert.clicked.connect(self.parse)
        

    def setValidator(self):
        regExp = QRegExp(r"[A-Za-z]\d{4,6}")
        val = QtGui.QRegExpValidator(regExp, self)
        self.Group.setValidator(val)

    def setReadable(self):
        self.Group.setReadOnly(not self.downloadSchedule.isChecked())
        if not self.downloadSchedule.isChecked():
            self.Group.clear()
        self.Day.setEnabled(self.downloadSchedule.isChecked())
        self.download.setEnabled(self.downloadSchedule.isChecked())
    
    def downloadS(self):
        self.textTo.clear()
        s = Schedule.Schedule(self.Group.text())
        if self.From.currentText() == "JSON":
            Schedule.convertToJSON(s, self.Day.currentText())
            file = open("Schedule.json", "r")
            text = file.read()
            self.textFrom.setText(text)
        if self.From.currentText() == "XML":
            Schedule.convertToXML(s, self.Day.currentText())
            file = open("Schedule.xml", "r")
            text = file.read()
            self.textFrom.setText(text)

    def parseJSON(self):
        text = self.textFrom.toPlainText()
        p = PrimitiveJSONParser.deserialize(text)
        text = PrimitiveXMLParser.serialize(p)
        self.textTo.setText(text)

    def parseXML(self):
        text = self.textFrom.toPlainText()
        p = PrimitiveXMLParser.deserialize(text)
        text = PrimitiveJSONParser.serialize(p)
        self.textTo.setText(text)

    def parse(self):
        if self.From.currentText() == "XML" and self.To.currentText() == "JSON":
            self.parseXML()
            return
        if self.From.currentText() == "JSON" and self.To.currentText() == "XML":
            self.parseJSON()
            return
        self.textTo.setText(self.textFrom.toPlainText())
        




def application():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


application()