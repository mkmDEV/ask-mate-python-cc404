import csv
import datetime
import calendar
import time
import os
from operator import itemgetter


import database_common


@database_common.connection_handler
def show_questions(cursor):
    cursor.execute("""SELECT * FROM question;""")
    question_all = cursor.fetchall()
    return question_all


@database_common.connection_handler
def show_question_by_id(cursor, question_id):
    cursor.execute("""SELECT * FROM question
                    WHERE id=%(question_id)s;""",
                   {'question_id': question_id})
    question_by_id = cursor.fetchall()
    return question_by_id


@database_common.connection_handler
def get_question_title(cursor, question_id):
    cursor.execute("""SELECT title FROM question
                    WHERE id=%(question_id)s""",
                   {'question_id': question_id})
    question_title = cursor.fetchall()
    for item in question_title:
        title = item['title']
    return title


@database_common.connection_handler
def show_answers(cursor, question_id):
    cursor.execute("""SELECT * FROM answer
                    WHERE question_id=%(question_id)s;""",
                   {'question_id': question_id})
    answer_all = cursor.fetchall()
    return answer_all


###################
@database_common.connection_handler
def add_question(cursor, new_question):
    cursor.execute("""INSERT INTO question (submission_time, view_number, title, message, image) 
                      VALUES ('<new_question>');""")


###################
@database_common.connection_handler
def add_message(cursor, new_answer):
    cursor.execute("""INSERT INTO quiestion
                      VALUES '<new_answer>';""")


@database_common.connection_handler
def remove_question_from_database(cursor, question_id):
    cursor.execute("""DELETE FROM question WHERE id=%(question_id)s;
                    DELETE FROM answer WHERE question_id=%(question_id)s;""",
                   {'question_id': question_id})


@database_common.connection_handler
def remove_answer_from_database(cursor, answer_id):
    cursor.execute("""DELETE FROM answer WHERE id=%(answer_id)s;""",
                   {'answer_id': answer_id})


def get_time_form_from_stamp(table, is_table=True):
    if is_table:
        for row in table:
            row['submission_time'] = \
                datetime.datetime.fromtimestamp(int(row['submission_time'])).strftime('%Y-%m-%d %H:%M:%S')
    else:
        table['submission_time'] = \
            datetime.datetime.fromtimestamp(int(table['submission_time'])).strftime('%Y-%m-%d %H:%M:%S')
    return table


def get_unix_time():
    return str(calendar.timegm(time.gmtime()))


"""def sorter(table, keyvalue, is_reverse=True):
    return sorted(table, key=itemgetter(keyvalue), reverse=is_reverse)"""


"""def get_next_id(file):
    existing_data = get_csv_data(file)
    if len(existing_data) == 0:
        return '1'
    return str(int(existing_data[-1]['id']) + 1)"""


"""def add_message_to_file(request, file='data/question.csv', q_id='0'):
    if file == 'data/question.csv':
        fields = [get_next_id('data/question.csv'), get_unix_time(), '0', '0', request['title'], request['message']]
    else:
        fields = [get_next_id('data/answer.csv'), get_unix_time(), '0', q_id, request['message']]
    with open(file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)"""


"""def create_updated_file(id, file, col):
    with open(file, 'r') as f:
        with open('data/cache.csv', 'w') as f1:
            for line in f:
                if line[col] != id:
                    f1.write(line)"""


"""def update_original_file(file):
    with open('data/cache.csv', 'r') as f:
        with open(file, 'w') as f1:
            for line in f:
                f1.write(line)
    os.remove('data/cache.csv')"""
