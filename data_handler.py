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
                                LOWER(message) LIKE LOWER(%(search)s) OR
                                LOWER(username) LIKE LOWER(%(search)s)
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
def add_question(cursor, title, message, file_path, username):
    cursor.execute("""INSERT INTO question (title, message, image, username) 
                      VALUES (%(title)s, %(message)s, %(file_path)s, %(username)s);""",
                   {'title': title,
                    'message': message,
                    'file_path': file_path,
                    'username': username})


@database_common.connection_handler
def add_answer(cursor, question_id, message, file_path, username):
    cursor.execute("""INSERT INTO answer (question_id, message, image, username)
                      VALUES (%(question_id)s, %(message)s, %(file_path)s, %(username)s);""",
                   {'question_id': question_id,
                    'message': message,
                    'file_path': file_path,
                    'username': username})


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
def add_comment_for_question(cursor, question_id, message, username):
    cursor.execute("""INSERT INTO comment (question_id, message, username)
                      VALUES (%(question_id)s, %(message)s, %(username)s);""",
                   {'question_id': question_id, 'message': message, 'username': username})


@database_common.connection_handler
def add_comment_for_answer(cursor, answer_id, message, username):
    cursor.execute("""INSERT INTO comment (answer_id, message, username)
                      VALUES (%(answer_id)s, %(message)s, %(username)s);""",
                   {'answer_id': answer_id, 'message': message, 'username': username})


@database_common.connection_handler
def remove_comment(cursor, comment_id):
    cursor.execute("""DELETE FROM comment WHERE id=%(comment_id)s;""",
                   {'comment_id': comment_id})


@database_common.connection_handler
def save_user(cursor, user_data, hashed_password):
    cursor.execute("""INSERT INTO "user" (user_name, user_email, hashed_password)
                    VALUES (%(user_name)s, %(user_email)s, %(hashed_password)s);""",
                   {'user_name': user_data['user_name'],
                    'user_email': user_data['user_email'],
                    'hashed_password': hashed_password})


@database_common.connection_handler
def get_user_by_email(cursor, email):
    cursor.execute("""SELECT * FROM "user"
                      WHERE user_email=%(email)s""",
                   {'email': email})
    user_data = cursor.fetchone()
    return user_data


@database_common.connection_handler
def list_all_users(cursor):
    cursor.execute("""SELECT DISTINCT "user".user_name, "user".user_email, "user".reg_time,
                    (SELECT COUNT(question.id) FROM question WHERE question.username="user".user_name) as question,
                    (SELECT COUNT(answer.id) FROM answer WHERE answer.username="user".user_name) as answer,
                    (SELECT COUNT("comment".id) FROM "comment" WHERE "comment".username="user".user_name) as "comment",
                    FROM "user", question, answer, "comment"
                    WHERE "user".user_name=question.username AND "user".user_name=answer.username AND "user".user_name="comment".username
                    GROUP BY "user".user_name, question.id, answer.id, "comment".id""")
    return cursor.fetchall()
