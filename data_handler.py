import csv
import os
import time

QUESTIONS_FILE_PATH = os.getenv('QUESTIONS_FILE_PATH') if 'QUESTIONS_FILE_PATH' in os.environ else 'question.csv'
ANSWERS_FILE_PATH = os.getenv('ANSWERS_FILE_PATH') if 'ANSWERS_FILE_PATH' in os.environ else 'answer.csv'
QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_all_question(convert_linebreaks=False):
    all_question = get_csv_data()

    if convert_linebreaks:
        for question in all_question:
            question['message'] = convert_linebreaks_to_br(question['message'])

    return all_question


def convert_time(timestamp):
    return time.strftime("%D %H:%M", time.localtime(int(timestamp)))


def get_question(question_id):
    return get_csv_data(question_id)


def get_next_id():
    existing_data = get_all_question()

    if len(existing_data) == 0:
        return '1'

    return str(int(existing_data[-1]['id']) + 1)


def get_csv_data(one_question_id=None):
    questions = []

    with open(QUESTIONS_FILE_PATH, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            user_story = dict(row)

            if one_question_id is not None and one_question_id == user_story['id']:
                return user_story

            questions.append(user_story)

    return questions


def add_user_story(story):
    story['id'] = get_next_id()
    story['status'] = DEFAULT_STATUS

    add_user_story_to_file(story, True)


def update_user_story(story):
    add_user_story_to_file(story, False)


def add_user_story_to_file(story, append=True):
    existing_data = get_all_question()

    with open(QUESTIONS_FILE_PATH, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=QUESTION_HEADER)
        writer.writeheader()

        for row in existing_data:
            if not append:
                if row['id'] == story['id']:
                    row = story

            writer.writerow(row)

        if append:
            writer.writerow(story)


def convert_linebreaks_to_br(original_str):
    return '<br>'.join(original_str.split('\n'))
