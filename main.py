import sys
from PyQt5.QtWidgets import*
from consulting_window import ConsultingWindow
from films_base import FilmBase
from question_base import QuestionBase


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.w = object

        self.consulting_button = QPushButton("Режим консультирования")
        self.film_button = QPushButton("Редактировать базу фильмов")
        self.questions_button = QPushButton("Редактировать базу вопросов")

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.consulting_button)
        self.main_layout.addWidget(self.film_button)
        self.main_layout.addWidget(self.questions_button)

        self.setLayout(self.main_layout)

        self.setWindowTitle("Menu")
        self.resize(300, 270)

        self.consulting_button.clicked.connect(self.open_consulting_window)
        self.film_button.clicked.connect(self.open_film_window)
        self.questions_button.clicked.connect(self.open_question_window)

    def open_consulting_window(self):
        self.w = ConsultingWindow()
        self.w.show()

    def open_film_window(self):
        self.w = FilmBase()
        self.w.show()

    def open_question_window(self):
        self.w = QuestionBase()
        self.w.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
