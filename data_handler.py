import csv
import datetime
import calendar
import time
import os
from operator import itemgetter


def get_csv_data(file='data/question.csv', id=None, key=None, isquestions=True):
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


def get_unix_time():
    return str(calendar.timegm(time.gmtime()))


def sorter(table, keyvalue, isreverse=True):
    return sorted(table, key=itemgetter(keyvalue), reverse=isreverse)


def get_next_id(file):
    existing_data = get_csv_data(file)
    if len(existing_data) == 0:
        return '1'
    return str(int(existing_data[-1]['id']) + 1)


def add_message_to_file(request, file='data/question.csv', q_id='0'):
    if file == 'data/question.csv':
        fields = [get_next_id('data/question.csv'), get_unix_time(), '0', '0', request['title'], request['message']]
    else:
        fields = [get_next_id('data/answer.csv'), get_unix_time(), '0', q_id, request['message']]
    with open(file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)


def create_updated_file(id, file, col):
    with open(file, 'r') as f:
        with open('data/cache.csv', 'w') as f1:
            for line in f:
                if line[col] != id:
                    f1.write(line)


def update_original_file(file):
    with open('data/cache.csv', 'r') as f:
        with open(file, 'w') as f1:
            for line in f:
                f1.write(line)
    os.remove('data/cache.csv')

