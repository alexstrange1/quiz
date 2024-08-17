import sqlite3

db_name = "quiz.sqlite"
conn = None
cursor = None

def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()

def get_questions(quiz_id):
    open()
    sql = '''
    SELECT question.question,
    question.answer,
    question.wrong1,
    question.wrong2,
    question.wrong3,
    quiz.name
    FROM question, quiz_content, quiz
    WHERE question.id == quiz_content.question_id
    AND quiz.id == quiz_content.quiz_id
    AND quiz_content.quiz_id == ?;'''
    cursor.execute(sql, [quiz_id])
    data = cursor.fetchall()
    close()
    return data

def get_quizzes():
    open()
    sql = 'SELECT * FROM quiz ORDER BY id;'
    cursor.execute(sql)
    data = cursor.fetchall()
    close()
    return data
