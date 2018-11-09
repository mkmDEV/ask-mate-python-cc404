from flask import Flask, render_template, redirect, request
import data_handler

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def home():
    questions = data_handler.get_csv_data()
    questions = data_handler.sorter(questions, 'submission_time')
    questions = data_handler.get_time_form_from_stamp(questions)
    return render_template('list.html',
                           questions=questions,
                           page_title='Welcome to AskMate!')


@app.route('/question/<question_id>')
def display_question(question_id: int):
    question_data = data_handler.get_csv_data(id=question_id, key='id')
    question_data = data_handler.get_time_form_from_stamp(question_data, False)
    answers = data_handler.get_csv_data('data/answer.csv', question_id, 'question_id', False)
    answers = data_handler.sorter(answers, 'submission_time')
    answers = data_handler.get_time_form_from_stamp(answers)
    return render_template('single_question.html',
                           question=question_data,
                           page_title=question_data['title'],
                           answers=answers,
                           )


@app.route('/new-question')
def write_new_question():
    return render_template('new_question.html')


@app.route('/new-question', methods=['POST'])
def post_new_question():
    data_handler.add_message_to_file(request.form)
    return redirect('/')


@app.route('/question/<question_id>/delete')
def delete_question(question_id: int):
    data_handler.create_updated_file(question_id, 'data/question.csv', 0)
    data_handler.update_original_file('data/question.csv')
    #data_handler.create_updated_file(question_id, 'data/answer.csv', 3)
    #data_handler.update_original_file('data/answer.csv')
    return redirect('/')


@app.route('/question/<question_id>/new-answer')
def write_new_answer(question_id: int):
    question_data = data_handler.get_csv_data(id=question_id, key='id')
    question_data = data_handler.get_time_form_from_stamp(question_data, False)
    return render_template('new_answer.html',
                           question=question_data,
                           question_id=question_id,
                           page_title=question_data['title']
                           )


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def post_new_answer(question_id):
    data_handler.add_message_to_file(request.form, 'data/answer.csv', question_id)
    return redirect('/question/'+question_id)


@app.route('/question/<question_id>/answer/<answer_id>')
def delete_answer(question_id, answer_id: int):
    data_handler.create_updated_file(answer_id, 'data/answer.csv', 0)
    data_handler.update_original_file('data/answer.csv')
    return redirect('/question/' + question_id)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
