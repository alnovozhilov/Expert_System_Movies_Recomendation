import sys
from PyQt5.QtWidgets import*
from PyQt5.QtGui import QPixmap
from urllib import request


class ResultWindow(QDialog):
    def __init__(self, root, title, overview, genres, rating, year, director, actors, poster_url):
        super().__init__(root)

        self.setWindowTitle("Result")
        self.resize(300, 270)

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet('''font-size: 30px''')
        self.title_label.setFixedHeight(40)

        self.overview_label = QLabel(overview)
        self.overview_label.setWordWrap(True)
        self.overview_label.setMaximumWidth(self.width())

        self.genres_label = QLabel("Genres: " + genres)
        self.rating_label = QLabel(str(rating))
        self.year_label = QLabel("Year: " + str(year))
        self.director_label = QLabel("Director: " + director)
        self.actors_label = QLabel("Actors: " + actors)
        self.actors_label.setWordWrap(True)

        self.pixmap = QPixmap()
        self.img_label = QLabel(self)

        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.overview_label)
        self.main_layout.addWidget(self.genres_label)
        self.main_layout.addWidget(self.year_label)
        self.main_layout.addWidget(self.director_label)
        self.main_layout.addWidget(self.actors_label)
        self.main_layout.addWidget(self.img_label)
        self.setLayout(self.main_layout)

        self.setup_image(poster_url)

    def setup_image(self, url):
        print(url)
        data = request.urlopen(url).read()
        self.pixmap.loadFromData(data)
        self.pixmap = self.pixmap.scaledToHeight(400)
        self.img_label.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ResultWindow(None, 'ass', 'we can asdsadasdasf dfefrgggggggggg gggggggggggg ggggggggggg ggggggggg ggggggg gdsd asdasd', 'fist,ass', 10, 1999, 'Wan', 'Gook', 'https://m.media-amazon.com/images/M/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFmNTEtODM1ZmRlYWMwMWFmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_UX67_CR0,0,67,98_AL_.jpg')
    win.show()
    sys.exit(app.exec_())