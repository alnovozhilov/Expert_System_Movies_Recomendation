import sys
from PyQt5.QtWidgets import*
import sqlite3
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import*
from PyQt5.QtGui import QKeyEvent


class FilmBase(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Film base")
        self.resize(1200, 600)

        database = sqlite3.connect('films_database.db')
        self.films_cur = database.cursor()

        self.film_table = TableView(self)
        self.model = QStandardItemModel()
        self.film_table.setModel(self.model)

        self.add_button = QPushButton("Добавить")

        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.film_table, 0, 0, 1, 10)
        self.main_layout.addWidget(self.add_button, 1, 0, -1, 1)
        self.setLayout(self.main_layout)

        self.add_button.clicked.connect(self.open_add_dialog)

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

    def open_add_dialog(self):
        ad = AddDialog(self)
        ad.show()


class TableView(QTableView):
    def __init__(self, root):
        QWidget.__init__(self, root)
        self.main = root

    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.key() == Qt.Key_Delete:
            id = self.model().index(self.currentIndex().row(), 0).data()
            self.delete_data(id)
        elif e.key() == Qt.Key_Return:
            id = self.model().index(self.currentIndex().row(), 0).data()
            column = self.model().headerData(self.currentIndex().column(), Qt.Horizontal)
            data = self.currentIndex().data()
            self.update_data(id, column, data)

    def delete_data(self, id):
        database = sqlite3.connect('films_database.db')
        films_cur = database.cursor()
        query = "DELETE FROM films WHERE id = " + id + ";"
        films_cur.execute(query)
        database.commit()
        self.main.setup_table()
        print("success!")

    def update_data(self, id, column, data):
        database = sqlite3.connect('films_database.db')
        films_cur = database.cursor()
        query = "UPDATE films SET " + column + " = \'" + data + "\' WHERE id = " + id + ";"
        print(query)
        films_cur.execute(query)
        database.commit()



class AddDialog(QDialog):
    def __init__(self, root):
        QWidget.__init__(self, root)
        self.main = root
        self.cameras_label = QLabel("Введите информацию о фильме:")

        self.title_label = QLabel("Title: ")
        self.title_edit = QLineEdit()

        self.overview_label = QLabel("Overview:")
        self.overview_edit = QLineEdit()

        self.genres_label = QLabel("Genres:")
        self.genres_edit = QLineEdit()

        self.rating_label = QLabel("Rating: ")
        self.rating_edit = QLineEdit()

        self.year_label = QLabel("Year:")
        self.year_edit = QLineEdit()

        self.certificate_label = QLabel("Certificate:")
        self.certificate_edit = QLineEdit()

        self.runtime_label = QLabel("Runtime:")
        self.runtime_edit = QLineEdit()

        self.director_label = QLabel("Director: ")
        self.director_edit = QLineEdit()

        self.stars_label = QLabel("Stars:")
        self.stars_edit = QLineEdit()

        self.poster_link_label = QLabel("Poster link:")
        self.poster_link_edit = QLineEdit()

        self.label_layout = QVBoxLayout()
        self.label_layout.addWidget(self.title_label)
        self.label_layout.addWidget(self.overview_label)
        self.label_layout.addWidget(self.genres_label)
        self.label_layout.addWidget(self.rating_label)
        self.label_layout.addWidget(self.year_label)
        self.label_layout.addWidget(self.certificate_label)
        self.label_layout.addWidget(self.runtime_label)
        self.label_layout.addWidget(self.director_label)
        self.label_layout.addWidget(self.stars_label)
        self.label_layout.addWidget(self.poster_link_label)

        self.edit_layout = QVBoxLayout()
        self.edit_layout.addWidget(self.title_edit)
        self.edit_layout.addWidget(self.overview_edit)
        self.edit_layout.addWidget(self.genres_edit)
        self.edit_layout.addWidget(self.rating_edit)
        self.edit_layout.addWidget(self.year_edit)
        self.edit_layout.addWidget(self.certificate_edit)
        self.edit_layout.addWidget(self.runtime_edit)
        self.edit_layout.addWidget(self.director_edit)
        self.edit_layout.addWidget(self.stars_edit)
        self.edit_layout.addWidget(self.poster_link_edit)

        self.apply_button = QPushButton("Применить")
        self.apply_button.setMaximumWidth(100)

        self.line_layout = QHBoxLayout()
        self.line_layout.addLayout(self.label_layout)
        self.line_layout.addLayout(self.edit_layout)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.line_layout)
        self.main_layout.addWidget(self.apply_button)

        self.setLayout(self.main_layout)

        self.apply_button.clicked.connect(self.insert_film_and_close)

    def insert_film_and_close(self):
        database = sqlite3.connect('films_database.db')
        films_cur = database.cursor()
        query = '''INSERT INTO films (Title, Overview, Genres, Rating, Year, Certificate, Runtime, Director, Stars, Poster_link)
                            VALUES (\"''' + self.title_edit.text() + '\",\"' + self.overview_edit.text() + \
                                    '\",\"' + self.genres_edit.text() + '\",' + self.rating_edit.text() + \
                                    ',' + self.year_edit.text() + ',\"' + self.certificate_edit.text() + \
                                    '\",' + self.runtime_edit.text() + ',\"' + self.director_edit.text() + \
                                    '\",\"' + self.stars_edit.text() + '\",\"' + self.poster_link_edit.text() + '\");'
        films_cur.execute(query)
        database.commit()
        self.main.setup_table()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = FilmBase()
    win.show()
    sys.exit(app.exec_())