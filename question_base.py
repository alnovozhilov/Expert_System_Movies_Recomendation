import sys
from PyQt5.QtWidgets import*
from PyQt5.QtGui import QPixmap
from urllib import request
import sqlite3

class QuestionBase(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Question base")
        self.resize(300, 270)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QuestionBase()
    win.show()
    sys.exit(app.exec_())