import csv
import datetime
from operator import itemgetter

QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_csv_data(file='question.csv', id=None, key=None, isquestions=True):
    all_data = []
    with open(file, encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            single_data = dict(row)
            if isquestions:
                if id is not None and id == single_data[key]:
                    return single_data
                all_data.append(single_data)
            else:
                if id is not None and id == single_data[key]:
                    all_data.append(single_data)
        return all_data


def get_timeform_from_stamp(table, istable=True):
    if istable:
        for row in table:
            row['submission_time'] = datetime.datetime.fromtimestamp(int(row['submission_time'])).strftime('%Y-%m-%d %H:%M:%S')
    else:
        table['submission_time'] = datetime.datetime.fromtimestamp(int(table['submission_time'])).strftime('%Y-%m-%d %H:%M:%S')
    return table

def sorter(table, keyvalue, isreverse=True):
    return sorted(table, key=itemgetter(keyvalue), reverse=isreverse)


def get_next_id():
    existing_data = get_all_question()

    if len(existing_data) == 0:
        return '1'

    return str(int(existing_data[-1]['id']) + 1)


def add_user_story(story):
    story['id'] = get_next_id()
    story['status'] = DEFAULT_STATUS

    add_user_story_to_file(story, True)


def update_user_story(story):
    add_user_story_to_file(story, False)


def add_user_story_to_file(story, append=True):
    existing_data = get_all_question()

    with open(QUESTIONS_FILE_PATH, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=QUESTION_HEADER)
        writer.writeheader()

        for row in existing_data:
            if not append:
                if row['id'] == story['id']:
                    row = story

            writer.writerow(row)

        if append:
            writer.writerow(story)
