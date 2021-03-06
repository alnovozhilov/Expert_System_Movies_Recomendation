import sys
from PyQt5.QtWidgets import*
import sqlite3
from result_window import ResultWindow


class ConsultingWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.w = object
        self.setWindowTitle("Consulting")
        self.resize(300, 270)
        self.option_id = ''

        database = sqlite3.connect('films_database.db')
        self.films_cur = database.cursor()
        self.query = "SELECT * FROM films"

        database = sqlite3.connect('questions_database.db')
        self.questions_cur = database.cursor()

        self.question_textEdit = QTextEdit()
        self.current_id = 1

        self.combo = QComboBox()
        self.option_ids = []

        self.btn = QPushButton("Далее")

        self.details_label = QLabel("Детали опроса:")
        self.details_textEdit = QTextEdit()
        self.restart_button = QPushButton("Начать опрос заново")

        self.details_layout = QVBoxLayout()
        self.details_layout.addWidget(self.details_label)
        self.details_layout.addWidget(self.details_textEdit)
        self.details_layout.addWidget(self.restart_button)

        self.answer_layout = QHBoxLayout()
        self.answer_layout.addWidget(self.combo)
        self.answer_layout.addWidget(self.btn)

        self.consulting_layout = QVBoxLayout()
        self.consulting_layout.addWidget(self.question_textEdit)
        self.consulting_layout.addLayout(self.answer_layout)

        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.consulting_layout)
        self.main_layout.addLayout(self.details_layout)
        self.setLayout(self.main_layout)

        self.init_question()

        self.btn.clicked.connect(self.next_question)
        self.restart_button.clicked.connect(self.init_question)

    def init_question(self):
        self.question_textEdit.clear()
        self.combo.clear()
        self.details_textEdit.clear()
        self.current_id = 1
        self.query = "SELECT * FROM films"
        self.option_ids = []
        for question in self.questions_cur.execute('SELECT * FROM questions WHERE id == ' + str(self.current_id) + ';'):
            self.question_textEdit.append(question[1])
        for option in self.questions_cur.execute('SELECT * FROM options WHERE question_id == ' + str(self.current_id) + ';'):
            self.combo.addItem(option[1])
            self.option_ids.append(option[0])

    def next_question(self):
        if len(self.option_ids) != 0:
            self.option_id = str(self.option_ids[self.combo.currentIndex()])
        query = "SELECT next_question_id, filter FROM options WHERE id == " + self.option_id + ";"
        for option in self.questions_cur.execute(query):
            if option[0] is None:
                self.query_formation(option[1])
                print("end")
            else:
                self.query_formation(option[1])
                self.current_id = option[0]
        self.replace_question()

    def query_formation(self, filter_value):
        if filter_value != '':
            if filter_value.find('LIKE') != -1:
                filter_value += '\'%' + self.combo.currentText() + '%\''
            if self.query.find('WHERE') != -1:
                self.query += ' AND ' + filter_value
            else:
                self.query += ' WHERE ' + filter_value

    def replace_question(self):
        self.question_textEdit.clear()
        for question in self.questions_cur.execute('SELECT * FROM questions WHERE id == ' + str(self.current_id) + ';'):
            self.question_textEdit.append(question[1])
        self.option_ids = []
        self.combo.clear()
        for option in self.questions_cur.execute('SELECT * FROM options WHERE question_id == ' + str(self.current_id) + ';'):
            values_arr = []
            if option[2].find('LIKE') != -1:
                new_query = self.query.replace('*', option[2].split(' ')[0])
                for film in self.films_cur.execute(new_query):
                    values_arr += film[0].split(',')
                values_arr = list(set(values_arr))
                self.combo.addItems(values_arr)
                self.option_id = str(option[0])
            else:
                self.combo.addItem(option[1])
                self.option_ids.append(option[0])
        if self.filtration():
            self.open_result_window()

    def filtration(self):
        self.details_textEdit.append(self.query)
        count = 0
        for film in self.films_cur.execute(self.query):
            count += 1
        self.details_textEdit.append("Фреймов удовлетворяющих ответу: " + str(count))
        if count == 1:
            self.details_textEdit.append("Найден результат!")
            return True
        elif count == 0:
            self.details_textEdit.append("Подходящего к запросу фрейма не найдено")
        else:
            return False

    def open_result_window(self):
        database = sqlite3.connect('films_database.db')
        films_cur = database.cursor()
        title = ''
        overview = ''
        genres = ''
        rating = 0
        year = 0
        director = ''
        actors = ''
        poster_url = ''

        for film in films_cur.execute(self.query):
            title = film[1]
            overview = film[2]
            genres = film[3]
            rating = film[4]
            year = film[5]
            director = film[8]
            actors = film[9]
            poster_url = film[10]
        w = ResultWindow(self, title, overview, genres, rating, year, director, actors, poster_url)
        w.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ConsultingWindow()
    win.show()
    sys.exit(app.exec_())