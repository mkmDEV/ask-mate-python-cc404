from flask import Flask, render_template, redirect, request
import data_handler
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/images'


@app.route('/')
def home():
    questions = data_handler.show_questions(None)
    return render_template('list.html',
                           questions=questions,
                           page_title='Welcome to AskMate!')


@app.route('/list', methods=['GET', 'POST'])
def sort_questions():
    questions = data_handler.sort()
    return render_template('list.html',
                           questions=questions,
                           page_title='Welcome to AskMate!')


@app.route('/search', methods=['POST'])
def search():
    search = "%"+request.form['search']+"%"
    questions = data_handler.show_questions(search)
    return render_template('list.html',
                           questions=questions,
                           page_title='Search results:')


@app.route('/question/<question_id>')
def display_question(question_id):
    question_data = data_handler.show_question_by_id(question_id)
    comments = data_handler.show_comments()
    answers = data_handler.show_answers(question_id)
    title = question_data[0]['title']
    return render_template('single_question.html',
                           question=question_data,
                           page_title=title,
                           comments=comments,
                           answers=answers,
                           title=title,
                           )


@app.route('/new-question')
def write_new_question():
    return render_template('new_question.html')


@app.route('/new-question', methods=['POST'])
def post_new_question():
    file = request.files['image']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    new_question = dict(request.form)
    data_handler.add_question(new_question, file.filename)
    return redirect('/')


@app.route('/question/<question_id>/delete')
def delete_question(question_id: int):
    data_handler.remove_question_from_database(question_id)
    return redirect('/')


@app.route('/question/<question_id>/new-answer')
def write_new_answer(question_id: int):
    question_data = data_handler.show_question_by_id(question_id)
    title = question_data[0]['title']
    return render_template('new_answer.html',
                           question_id=question_id,
                           page_title=title)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def post_new_answer(question_id: int):
    file = request.files['image']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    new_answer = dict(request.form)
    data_handler.add_message(question_id, new_answer, file.filename)
    return redirect('/question/' + str(question_id))


@app.route('/question/<question_id>/answer/<answer_id>')
def delete_answer(question_id, answer_id: int):
    data_handler.remove_answer_from_database(answer_id)
    return redirect('/question/' + question_id)


@app.route('/question/<question_id>/new-comment')
def write_new_comment(question_id):
    return render_template('new_comment.html',
                           page_title='Add new comment',
                           question_id=question_id,
                           )


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def post_new_comment(question_id):
    new_comment = dict(request.form)
    data_handler.add_comment_for_question(question_id, new_comment)
    return redirect('/question/' + question_id)


@app.route('/question/<question_id>/delete-comment/<comment_id>')
def delete_comment(question_id, comment_id: int):
    data_handler.remove_comment(comment_id)
    return redirect('/question/' + question_id)


@app.route('/answer/<answer_id>/new-comment')
def write_new_comment_for_answers(answer_id):
    return render_template('new_answer_comment.html',
                           page_title='Add new comment',
                           answer_id=answer_id,
                           )


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def post_new_comment_for_answers(answer_id):
    new_comment = dict(request.form)
    data_handler.add_comment_for_answer(answer_id, new_comment)
    return redirect('/')


@app.route('/christmas-egg')
def christmas_egg():
    return render_template('christmas_egg.html')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
