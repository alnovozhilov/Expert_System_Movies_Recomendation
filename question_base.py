import sys
from PyQt5.QtWidgets import*
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import*
from PyQt5.QtGui import QKeyEvent
import sqlite3


class QuestionBase(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Question base")
        self.resize(1200, 600)

        database = sqlite3.connect('questions_database.db')
        self.films_cur = database.cursor()

        self.question_table = QuestionsTableView(self)
        self.question_model = QStandardItemModel()
        self.question_table.setModel(self.question_model)

        self.option_table = OptionsTableView(self)
        self.option_model = QStandardItemModel()
        self.option_table.setModel(self.option_model)

        self.add_question_button = QPushButton("Добавить")
        self.add_question_button.setMaximumWidth(100)
        self.add_option_button = QPushButton("Добавить")
        self.add_option_button.setMaximumWidth(100)

        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.question_table, 0, 0, 1, 1)
        self.main_layout.addWidget(self.option_table, 0, 1, 1, 1)
        self.main_layout.addWidget(self.add_question_button, 1, 0, -1, 1)
        self.main_layout.addWidget(self.add_option_button, 1, 1, -1, 1)
        self.setLayout(self.main_layout)

        self.add_question_button.clicked.connect(self.open_add_question_dialog)
        self.add_option_button.clicked.connect(self.open_add_option_dialog)

        self.setup_question_table()
        self.setup_option_table()

    def setup_question_table(self):
        query = "PRAGMA table_info(questions)"
        columns = []
        for column in self.films_cur.execute(query):
            columns.append(column[1])

        self.question_model.setRowCount(len(columns))
        self.question_model.setHorizontalHeaderLabels(columns)

        query = "SELECT * FROM questions"
        count = 0
        for question in self.films_cur.execute(query):
            count += 1
        self.question_model.setRowCount(count)
        count = 0
        for question in self.films_cur.execute(query):
            for j in range(len(question)):
                self.question_model.setItem(count, j, QStandardItem(str(question[j])))
            count += 1

        for i in range(len(columns)):
            if i != 2 and i != 10:
                self.question_table.resizeColumnToContents(i)

        self.question_table.verticalHeader().setVisible(False)
        self.question_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

    def setup_option_table(self):
        query = "PRAGMA table_info(options)"
        columns = []
        for column in self.films_cur.execute(query):
            columns.append(column[1])

        self.option_model.setRowCount(len(columns))
        self.option_model.setHorizontalHeaderLabels(columns)

        query = "SELECT * FROM options"
        count = 0
        for question in self.films_cur.execute(query):
            count += 1
        self.option_model.setRowCount(count)
        count = 0
        for question in self.films_cur.execute(query):
            for j in range(len(question)):
                self.option_model.setItem(count, j, QStandardItem(str(question[j])))
            count += 1

        for i in range(len(columns)):
            if i != 2 and i != 10:
                self.option_table.resizeColumnToContents(i)

        self.option_table.verticalHeader().setVisible(False)
        self.option_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

    def open_add_question_dialog(self):
        ad = QuestionDialog(self)
        ad.show()

    def open_add_option_dialog(self):
        od = OptionDialog(self)
        od.show()


class QuestionsTableView(QTableView):
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
        database = sqlite3.connect('questions_database.db')
        questions_cur = database.cursor()
        query = "DELETE FROM questions WHERE id = " + id + ";"
        questions_cur.execute(query)
        database.commit()
        self.main.setup_question_table()
        print("success!")

    def update_data(self, id, column, data):
        database = sqlite3.connect('questions_database.db')
        questions_cur = database.cursor()
        query = "UPDATE questions SET " + column + " = \'" + data + "\' WHERE id = " + id + ";"
        print(query)
        questions_cur.execute(query)
        database.commit()


class OptionsTableView(QTableView):
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
        database = sqlite3.connect('questions_database.db')
        options_cur = database.cursor()
        query = "DELETE FROM options WHERE id = " + id + ";"
        options_cur.execute(query)
        database.commit()
        self.main.setup_option_table()
        print("success!")

    def update_data(self, id, column, data):
        database = sqlite3.connect('questions_database.db')
        options_cur = database.cursor()
        query = "UPDATE options SET " + column + " = \'" + data + "\' WHERE id = " + id + ";"
        print(query)
        options_cur.execute(query)
        database.commit()


class QuestionDialog(QDialog):
    def __init__(self, root):
        QWidget.__init__(self, root)
        self.main = root

        self.question_label = QLabel("Введите вопрос:")
        self.question_edit = QLineEdit()

        self.apply_button = QPushButton("Применить")
        self.apply_button.setMaximumWidth(100)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.question_label)
        self.main_layout.addWidget(self.question_edit)
        self.main_layout.addWidget(self.apply_button)

        self.setLayout(self.main_layout)

        self.apply_button.clicked.connect(self.insert_question_and_close)

    def insert_question_and_close(self):
        database = sqlite3.connect('questions_database.db')
        films_cur = database.cursor()
        query = "INSERT INTO questions (question) VALUES (\'" + self.question_edit.text() + "\');"
        films_cur.execute(query)
        database.commit()
        self.main.setup_question_table()
        self.close()


class OptionDialog(QDialog):
    def __init__(self, root):
        QWidget.__init__(self, root)
        self.main = root

        self.option_label = QLabel("Вариант ответа:")
        self.option_edit = QLineEdit()

        self.filter_label = QLabel("Выражение")
        self.filter_edit = QLineEdit()

        self.question_id_label = QLabel("id вопроса")
        self.question_id_edit = QLineEdit()

        self.next_question_id_label = QLabel("id следующего вопроса")
        self.next_question_id_edit = QLineEdit()

        self.labels_layout = QVBoxLayout()
        self.labels_layout.addWidget(self.option_label)
        self.labels_layout.addWidget(self.filter_label)
        self.labels_layout.addWidget(self.question_id_label)
        self.labels_layout.addWidget(self.next_question_id_label)

        self.edit_layout = QVBoxLayout()
        self.edit_layout.addWidget(self.option_edit)
        self.edit_layout.addWidget(self.filter_edit)
        self.edit_layout.addWidget(self.question_id_edit)
        self.edit_layout.addWidget(self.next_question_id_edit)

        self.row_layout = QHBoxLayout()
        self.row_layout.addLayout(self.labels_layout)
        self.row_layout.addLayout(self.edit_layout)

        self.apply_button = QPushButton("Применить")
        self.apply_button.setMaximumWidth(100)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.row_layout)
        self.main_layout.addWidget(self.apply_button)

        self.setLayout(self.main_layout)

        self.apply_button.clicked.connect(self.insert_option_and_close)

    def insert_option_and_close(self):
        database = sqlite3.connect('questions_database.db')
        films_cur = database.cursor()
        option = self.option_edit.text()
        filter = self.filter_edit.text()
        question_id = self.question_id_edit.text()
        next_question_id = "NULL" if self.next_question_id_edit.text() == '' else self.next_question_id_edit.text()
        print(next_question_id)
        query = '''INSERT INTO options (option, filter, question_id, next_question_id) 
                            VALUES (\'''' + option + '\', \'' + filter +\
                                    '\', ' + question_id + ',' + next_question_id + ');'
        print(query)
        films_cur.execute(query)
        database.commit()
        self.main.setup_option_table()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QuestionBase()
    win.show()
    sys.exit(app.exec_())