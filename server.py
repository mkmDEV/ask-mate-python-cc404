from flask import Flask, render_template, request, redirect, url_for
import data_handler

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def home():
    questions = data_handler.get_all_question(convert_linebreaks=True)
    questions = data_handler.sorter(questions, 'submission_time')
    questions = data_handler.get_timeform_from_stamp(questions)
    return render_template('list.html',
                           questions=questions,
                           page_title='Welcome to AskMate!')


@app.route('/new-question')
def write_new_question():
    return render_template('question.html')


@app.route('/new-question', methods=['POST'])
def post_new_question():
    return redirect('/')


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def display_question(question_id: int):
    answers = [
        {
        'id': 0,
        'submission_time': '2018-11-01',
        'vote_number': 12,
        'question_id': 0,
        'message': 'Here is a sample Lorem Ipsum Sit Dolor Amet',
        'image': '',
        },
        {
        'id': 1,
        'submission_time': '2018-11-02',
        'vote_number': -5,
        'question_id': 1,
        'message': 'Here is another sample Lorem Ipsum Sit Dolor Amet',
        'image': '',
        },
    ]
    question_data = data_handler.get_question(question_id)
    print(question_data)
    question_data = data_handler.get_timeform_from_stamp(question_data, False)
    return render_template('single_question.html',
                           question=question_data,
                           page_title=question_data['title'],
                           answers=answers,
                           )


@app.route('/question/<question_id>/new-answer')
def write_new_answer(question_id: int):
    question_data = data_handler.get_question(question_id)
    return render_template('post_answer.html',
                           question=question_data,
                           question_id=question_id,
                           page_title=question_data['title']
                           )


@app.route('/question/<question_id>/new-answer', methods=['POST'])
def post_new_answer(question_id):
    return redirect('/')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
