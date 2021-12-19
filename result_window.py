import sys
from PyQt5.QtWidgets import*
from PyQt5.QtGui import QPixmap
from urllib import request
import sqlite3


class ResultWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Result")
        self.resize(300, 270)

        self.title_label = QLabel("Title")
        self.title_label.setStyleSheet('''font-size: 30px''')
        self.title_label.setFixedHeight(40)
        self.overview_label = QLabel("overview")
        self.genres_label = QLabel("Gen1, gen2, gen3")
        self.rating_label = QLabel("Rating: 8.9")
        self.year_label = QLabel("Year: 1999")
        self.director_label = QLabel("Director: Ivan Ivanov")
        self.actors_label = QLabel("Actors: Ivan Ivanov, Ivan Ivanov, Ivan Ivanov")

        self.pixmap = QPixmap()
        self.img_label = QLabel(self)

        self.description_layout = QVBoxLayout()
        self.description_layout.addWidget(self.overview_label)
        self.description_layout.addWidget(self.genres_label)
        self.description_layout.addWidget(self.rating_label)
        self.description_layout.addWidget(self.year_label)
        self.description_layout.addWidget(self.director_label)
        self.description_layout.addWidget(self.actors_label)

        self.description_and_img_layout = QHBoxLayout()
        self.description_and_img_layout.addLayout(self.description_layout)
        self.description_and_img_layout.addWidget(self.img_label)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addLayout(self.description_and_img_layout)
        self.setLayout(self.main_layout)

        database = sqlite3.connect('films_database.db')
        self.films_cur = database.cursor()
        self.query = "SELECT * FROM films WHERE Title = \'The Thing\';"
        for film in self.films_cur.execute(self.query):
            self.title_label.setText(film[1])
            self.overview_label.setText(film[2])
            self.genres_label.setText(film[3])
            self.rating_label.setText(str(film[4]))
            self.year_label.setText(str(film[5]))
            self.director_label.setText(film[8])
            self.actors_label.setText(film[9])
            self.setup_image(film[10])
            print(film)

    def setup_image(self, url):
        data = request.urlopen(url).read()
        self.pixmap.loadFromData(data)
        self.pixmap = self.pixmap.scaledToHeight(400)
        self.img_label.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ResultWindow()
    win.show()
    sys.exit(app.exec_())