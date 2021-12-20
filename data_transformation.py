import pandas as pd
import sqlite3


def transform_data():
    excel_data_df = pd.read_csv('imdb_top_1000.csv', lineterminator='\n')

    excel_data_df = excel_data_df.drop(['Meta_score',
                                        'No_of_Votes',
                                        'Gross\r'], 1)

    count = 0
    genres = []
    genres_df = []
    stars = []
    runtime = []
    for i in range(0, len(excel_data_df)):
        filmGenres = excel_data_df['Genre'][i].replace(" ", "")
        genres += filmGenres.split(',')
        genres_df.append(filmGenres)
        runtime.append(excel_data_df['Runtime'][i].split(" ")[0])
        stars.append(excel_data_df['Star1'][i] + ',' +
                     excel_data_df['Star2'][i] + ',' +
                     excel_data_df['Star3'][i] + ',' +
                     excel_data_df['Star4'][i])
    genres = list(set(genres))

    clear_df = pd.DataFrame()
    clear_df['Title'] = excel_data_df['Series_Title']
    clear_df['Overview'] = excel_data_df['Overview']
    clear_df['Genres'] = genres_df
    clear_df['Rating'] = excel_data_df['IMDB_Rating']
    clear_df['Year'] = excel_data_df['Released_Year']
    clear_df.loc[(clear_df.Year == 'PG'), 'Year'] = '1995'
    clear_df['Year'] = clear_df['Year'].astype('int')
    clear_df['Certificate'] = excel_data_df['Certificate']
    clear_df['Runtime'] = runtime
    clear_df['Runtime'] = clear_df['Runtime'].astype('int')
    clear_df['Director'] = excel_data_df['Director']
    clear_df['Stars'] = stars
    clear_df['Poster_Link'] = excel_data_df['Poster_Link']

    #print(clear_df['Certificate'].unique())

    #database = sqlite3.connect('films_database.db')
    #cur = database.cursor()
    #cur.execute("CREATE TABLE genres (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL , name TEXT NOT NULL);")
    #for genre in genres:
    #    cur.execute("INSERT INTO genres (name) VALUES (\'" + genre + "\');")

    #database.commit()
    #database.close()


    database = sqlite3.connect('films_database.db')
    clear_df.to_sql('films', con=database)



   # return clear_df


def create_questions_table():
    database = sqlite3.connect('questions_database.db')
    cur = database.cursor()
    cur.execute('''DROP TABLE IF EXISTS questions;''')
    cur.execute('''CREATE TABLE IF NOT EXISTS questions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL , 
                        question TEXT NOT NULL
                   );''')

    cur.execute('''INSERT INTO questions (question) 
                   VALUES (\'Выбирать из списка фильмов с высоким рейтингом?\'),
                          (\'Подходит ли фильм для детей?\'),
                          (\'Фильм имеет рейтинг только для взрослых?\'),
                          (\'Выберите предпочитаемую продолжительность\'),
                          (\'Фильмы какого десятилетия вы предпочитаете?\'),
                          (\'Выберите предпочитаемый жанр\'),
                          (\'Фильмы какого режиссера вы предпочитаете?\'),
                          (\'Выберите предпочитаемого актера\');''')

    database.commit()
    database.close()


def create_options_table():
    database = sqlite3.connect('questions_database.db')
    cur = database.cursor()
    cur.execute('''DROP TABLE IF EXISTS options;''')
    cur.execute('''CREATE TABLE IF NOT EXISTS options (
                                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                option TEXT NOT NULL,
                                filter TEXT NOT NULL,
                                question_id INTEGER NOT NULL,
                                next_question_id INTEGER,
                                FOREIGN KEY(question_id, next_question_id) REFERENCES questions(id, id)
                           );''')

    cur.execute('''INSERT INTO options (option, filter, question_id, next_question_id) 
                               VALUES (\'Не имеет значения\', \'\', 1, 2),
                                      (\'Да\', \'Rating >= 8\', 1, 2),
                                      
                                      (\'Не имеет значения\', \'\', 2, 4),
                                      (\'Да\', \"(Certificate == \'G\' OR Certificate == \'PG\')\", 2, 4),
                                      (\'Нет\', \'\', 2, 3),
                                      
                                      (\'Не имеет значения\', \'\', 3, 4),
                                      (\'Да\', \"(Certificate == \'R\' OR Certificate == \'A\')\", 3, 4),
                                      
                                      (\'Не имеет значения\', \'\', 4, 5),
                                      (\'Менее двух часов\', \'Runtime < 120\', 4, 5),
                                      (\'Два - три часа\', \'Runtime >= 120 AND Runtime <= 180\', 4, 5),
                                      (\'Более трех часов\', \'Runtime > 180\', 4, 5),
                                      
                                      (\'Не имеет значения\', \'\', 5, 6),
                                      (\'< 1980\', \'Year < 1980\', 5, 6),
                                      (\'1980 - 1989\', \'Year >= 1980 AND Year <= 1989\', 5, 6),
                                      (\'1990 - 1999\', \'Year >= 1990 AND Year <= 1999\', 5, 6),
                                      (\'2000 - 2009\', \'Year >= 2000 AND Year <= 2009\', 5, 6),
                                      (\'2009 >\', \'Year > 2009\', 5, 6),                                   
                                      
                                      (\'\', \'Genres LIKE \', 6, 7),
                                      
                                      (\'\', \'Director LIKE \', 7, 8),
                                      
                                      (\'\', \'Stars LIKE \', 8, NULL);''')

    database.commit()
    database.close()


def test():
    database = sqlite3.connect('films_database.db')
    cur = database.cursor()

    query = "ALTER TABLE films RENAME TO films_old"
    cur.execute(query)
    query = '''CREATE TABLE IF NOT EXISTS films (
                            id INTEGER PRIMARY KEY NOT NULL,
                            Title TEXT NOT NULL,
                            Overview TEXT NOT NULL,
                            Genres TEXT NOT NULL,
                            Rating REAL NOT NULL,
                            Year INTEGER NOT NULL,
                            Certificate TEXT,
                            Runtime INTEGER NOT NULL,
                            Director TEXT NOT NULL,
                            Stars TEXT NOT NULL,
                            Poster_Link TEXT NOT NULL
                            );'''
    cur.execute(query)

    films = []
    for film in cur.execute("SELECT * FROM films_old;"):
        overview = film[2].replace("\"", "\'")
        films.append([film[0], film[1], overview, film[3], film[4], film[5], film[6], film[7], film[8], film[9], film[10]])

    for film in films:
        print(film)
        query = '''INSERT INTO films (Title, Overview, Genres, Rating, Year, Certificate, Runtime, Director, Stars, Poster_Link)
                            VALUES (\"''' + str(film[1]) + '\",\"' + str(film[2]) + \
                                    '\",\"' + str(film[3]) + '\",' + str(film[4]) + \
                                    ',' + str(film[5]) + ',\"' + str(film[6]) + \
                                    '\",' + str(film[7]) + ',\"' + str(film[8]) + \
                                    '\",\"' + str(film[9]) + '\",\"' + str(film[10]) + '\");'
        print(query)
        cur.execute(query)
    query = "DROP TABLE IF EXISTS films_old;"
    cur.execute(query)
    database.commit()


def test1():
    database = sqlite3.connect('questions_database.db')
    cur = database.cursor()
    id = []
    questions = []
    for row in cur.execute('SELECT * FROM options WHERE id == 1;'):
        id.append(row[0])
        questions.append(row[1])
    print(id)
    print(questions)

def test2():
    database = sqlite3.connect('films_database.db')
    cur = database.cursor()
    for row in cur.execute('SELECT * FROM films;'):
        print(row)

#create_options_table()
transform_data()
test()
#test2()
