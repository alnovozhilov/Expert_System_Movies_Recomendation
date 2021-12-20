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

        self.textEdit = QTextEdit()
        self.current_id = 1
        for question in self.questions_cur.execute('SELECT * FROM questions WHERE id == ' + str(self.current_id) + ';'):
            self.textEdit.append(question[1])

        self.combo = QComboBox()
        self.option_ids = []
        for option in self.questions_cur.execute('SELECT * FROM options WHERE question_id == ' + str(self.current_id) + ';'):
            self.combo.addItem(option[1])
            self.option_ids.append(option[0])
        self.btn = QPushButton("Далее")

        main_layout = QVBoxLayout()
        self.answer_layout = QHBoxLayout()
        self.answer_layout.addWidget(self.combo)
        self.answer_layout.addWidget(self.btn)
        main_layout.addWidget(self.textEdit)
        main_layout.addLayout(self.answer_layout)
        self.setLayout(main_layout)

        self.btn.clicked.connect(self.next_question)

    def next_question(self):
        if len(self.option_ids) != 0:
            self.option_id = str(self.option_ids[self.combo.currentIndex()])
        query = "SELECT next_question_id, filter FROM options WHERE id == " + self.option_id + ";"
        for option in self.questions_cur.execute(query):
            if option[0] is None:
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
        self.textEdit.clear()
        for question in self.questions_cur.execute('SELECT * FROM questions WHERE id == ' + str(self.current_id) + ';'):
            self.textEdit.append(question[1])
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
        self.filtration()


    def filtration(self):
        print(self.query)
        count = 0
        for film in self.films_cur.execute(self.query):
            count += 1
        print(count)
        #if count == 1:
        #    return True
        #else:
        #    return False

    def open_result_window(self):
        w = ResultWindow()
        w.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ConsultingWindow()
    win.show()
    sys.exit(app.exec_())