import database_common
from flask import request


@database_common.connection_handler
def show_questions(cursor, search, limit=5):
    if search is None:
        cursor.execute("""SELECT * FROM question 
                          ORDER BY submission_time
                          DESC LIMIT 5""")
    else:
        cursor.execute("""SELECT * FROM question 
                          WHERE LOWER(title) LIKE LOWER(%(search)s) OR
                                LOWER(message) LIKE LOWER(%(search)s)
                          ORDER BY submission_time
                          DESC LIMIT %(limit)s""",
                       {'limit': limit, 'search': search})
    question_all = cursor.fetchall()
    return question_all


@database_common.connection_handler
def sort(cursor):
    for key in request.args:
        criteria = key
        order = request.args.get(key)
    cursor.execute(f"SELECT * FROM question ORDER BY {criteria} {order}")
    question_sorted = cursor.fetchall()
    return question_sorted


@database_common.connection_handler
def show_question_by_id(cursor, question_id):
    cursor.execute("""UPDATE question
                      SET view_number = view_number + 1
                      WHERE id=%(question_id)s;
                      SELECT * FROM question
                      WHERE id=%(question_id)s;""",
                   {'question_id': question_id})
    question_by_id = cursor.fetchall()
    return question_by_id


@database_common.connection_handler
def show_answers(cursor, question_id):
    cursor.execute("""SELECT * FROM answer
                    WHERE question_id=%(question_id)s;""",
                   {'question_id': question_id})
    answer_all = cursor.fetchall()
    return answer_all


@database_common.connection_handler
def add_question(cursor, new_question, file_path):
    cursor.execute("""INSERT INTO question (title, message, image) 
                      VALUES (%(title)s, %(message)s, %(file_path)s);""",
                   {'title': new_question['title'], 'message': new_question['message'], 'file_path': file_path})


@database_common.connection_handler
def add_message(cursor, question_id, new_answer, file_path):
    cursor.execute("""INSERT INTO answer (message, question_id, image)
                      VALUES (%(message)s, %(question_id)s, %(file_path)s);""",
                   {'message': new_answer['message'], 'question_id': question_id, 'file_path': file_path})


@database_common.connection_handler
def remove_question_from_database(cursor, question_id):
    cursor.execute("""DELETE FROM comment WHERE question_id=%(question_id)s;
                      DELETE FROM answer WHERE question_id=%(question_id)s;
                      DELETE FROM question WHERE id=%(question_id)s;""",
                   {'question_id': question_id})


@database_common.connection_handler
def remove_answer_from_database(cursor, answer_id):
    cursor.execute("""DELETE FROM comment WHERE answer_id=%(answer_id)s;
                      DELETE FROM answer WHERE id=%(answer_id)s;""",
                   {'answer_id': answer_id})


@database_common.connection_handler
def show_comments(cursor):
    cursor.execute("""SELECT *
                      FROM comment""",)
    comment_all = cursor.fetchall()
    return comment_all


@database_common.connection_handler
def add_comment_for_question(cursor, question_id, new_comment):
    cursor.execute("""INSERT INTO comment (message, question_id)
                      VALUES (%(message)s, %(question_id)s);""",
                   {'message': new_comment['message'], 'question_id': question_id})


@database_common.connection_handler
def add_comment_for_answer(cursor, answer_id, new_comment):
    cursor.execute("""INSERT INTO comment (message, answer_id)
                      VALUES (%(message)s, %(answer_id)s);""",
                   {'message': new_comment['message'], 'answer_id': answer_id})


@database_common.connection_handler
def remove_comment(cursor, comment_id):
    cursor.execute("""DELETE FROM comment WHERE id=%(comment_id)s;""",
                   {'comment_id': comment_id})


@database_common.connection_handler
def save_user(cursor, user_data):
    cursor.execute("""INSERT INTO user""")
    pass
