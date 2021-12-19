import sys
from PyQt5.QtWidgets import*
import sqlite3
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class FilmBase(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Film base")
        self.resize(300, 270)

        database = sqlite3.connect('films_database.db')
        self.films_cur = database.cursor()

        self.film_table = QTableView()
        self.model = QStandardItemModel()
        self.film_table.setModel(self.model)

        self.add_button = QPushButton("Добавить")

        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.film_table, 0, 0, 1, 10)
        self.main_layout.addWidget(self.add_button, 1, 0, -1, 1)
        self.setLayout(self.main_layout)

        self.setup_table()

    def setup_table(self):
        query = "PRAGMA table_info(films)"
        columns = []
        for column in self.films_cur.execute(query):
            columns.append(column[1])

        self.model.setRowCount(len(columns))
        self.model.setHorizontalHeaderLabels(columns)

        query = "SELECT * FROM films"
        count = 0
        for film in self.films_cur.execute(query):
            count += 1
        self.model.setRowCount(count)
        count = 0
        for film in self.films_cur.execute(query):
            for j in range(len(film)):
                self.model.setItem(count, j, QStandardItem(str(film[j])))
            count += 1

        for i in range(len(columns)):
            if i != 2 and i != 10:
                self.film_table.resizeColumnToContents(i)

        self.film_table.verticalHeader().setVisible(False)
        self.film_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = FilmBase()
    win.show()
    sys.exit(app.exec_())