from flask import Flask, render_template, redirect, request
import data_handler

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def home():
    questions = data_handler.show_questions()
    #questions = data_handler.sorter(questions, 'submission_time')
    #questions = data_handler.get_time_form_from_stamp(questions)
    return render_template('list.html',
                           questions=questions,
                           page_title='Welcome to AskMate!')


@app.route('/question/<question_id>')
def display_question(question_id):
    question_data = data_handler.show_question_by_id(question_id)
    comments = data_handler.show_comments_for_question(question_id)
    answers = data_handler.show_answers(question_id)
    title = data_handler.get_question_title(question_id)
    return render_template('single_question.html',
                           question=question_data,
                           page_title=title,
                           comments=comments,
                           answers=answers,
                           )


@app.route('/new-question')
def write_new_question():
    return render_template('new_question.html')


@app.route('/new-question', methods=['POST'])
def post_new_question():
    new_question = dict(request.form)
    data_handler.add_question(new_question)
    return redirect('/')


@app.route('/question/<question_id>/delete')
def delete_question(question_id: int):
    data_handler.remove_question(question_id)
    return redirect('/')


@app.route('/question/<question_id>/new-answer')
def write_new_answer(question_id):
    question_data = data_handler.add_message(question_id)
    question_data = data_handler.get_time_form_from_stamp(question_data, False)
    return render_template('new_answer.html',
                           question=question_data,
                           question_id=question_id,
                           page_title=title
                           )


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def post_new_answer(question_id):
    new_answer = dict(request.form)
    data_handler.add_question(question_id, new_answer)
    return redirect('/question/' + question_id)


@app.route('/question/<question_id>/answer/<answer_id>')
def delete_answer(question_id, answer_id: int):
    data_handler.remove_answer_from_database(answer_id)
    return redirect('/question/' + question_id)


@app.route('/question/<question_id>/new-comment')
def write_new_comment(question_id):
    comment_data = data_handler.add_comment(question_id)
    comment_data = data_handler.get_time_form_from_stamp(question_data, False)
    return render_template('new_comment.html',
                           page_title='Add new comment',
                           question_id=question_id,
                           comment=comment_data,
                           )


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def post_new_comment(question_id):
    new_comment = dict(request.form)
    data_handler.add_comment(question_id, new_comment)
    return redirect('/question/' + question_id)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
