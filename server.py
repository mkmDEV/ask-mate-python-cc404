from flask import Flask, render_template, redirect, request, session
import data_handler
import os
import password_verfication
import psycopg2

app = Flask(__name__)
app.secret_key = os.urandom(24)
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
    if 'image' in request.files:
        file = request.files['image']
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        filename = file.filename
    else:
        filename = None
    data_handler.add_question(request.form['title'], request.form['message'], filename, session['user'])
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
    if 'image' in request.files:
        file = request.files['image']
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        filename = file.filename
    else:
        filename = None
    data_handler.add_answer(question_id, request.form['message'], filename, session['user'])
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
    data_handler.add_comment_for_question(question_id, request.form['message'], session['user'])
    return redirect('/question/' + question_id)


@app.route('/question/<question_id>/delete-comment/<comment_id>')
def delete_comment(question_id, comment_id: int):
    data_handler.remove_comment(comment_id)
    return redirect('/question/' + question_id)


@app.route('/question/<question_id>/answer/<answer_id>/new-comment')
def write_new_comment_for_answers(answer_id, question_id):
    return render_template('new_answer_comment.html',
                           page_title='Add new comment',
                           answer_id=answer_id,
                           question_id=question_id
                           )


@app.route('/question/<question_id>/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def post_new_comment_for_answers(answer_id, question_id):
    data_handler.add_comment_for_answer(answer_id, request.form['message'], session['user'])
    return redirect('/question/' + question_id)


@app.route('/userlist')
def list_all_users():
    user_data = data_handler.list_all_users()
    return render_template('userlist.html', user_data=user_data)


@app.route('/christmas-egg')
def christmas_egg():
    return render_template('christmas_egg.html')


@app.route('/registration')
def load_registration_page():
    return render_template('registration.html')


@app.route('/registration', methods=['POST'])
def registration():
    user_data = {'user_name': request.form['username'],
                 'user_email': request.form['email'],
                 'user_password': request.form['password'],
                 'confirm_password': request.form['confirm']}
    hashed_password = password_verfication.hash_password(user_data['user_password'])
    if password_verfication.verify_password(user_data['confirm_password'], hashed_password) is True:
        message = 'Your registration was successful. Please, log in to continue!'
        try:
            data_handler.save_user(user_data, hashed_password)
            return render_template('login.html', message=message)
        except psycopg2.IntegrityError as e:
            error_message = 'Something went wrong. Please, try again!'
            if 'user_pk' in str(e):
                error_message = 'This username is taken.'
            elif 'user_user_email_uindex' in str(e):
                error_message = 'This email is taken.'
            return render_template('registration.html', message=error_message)
    else:
        message = 'The passwords don\'t match. Please, try again!'
    return render_template('registration.html',
                           message=message,
                           username=request.form['username'],
                           email=request.form['email'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = data_handler.get_user_by_email(email)
        if user and password_verfication.verify_password(password, user['hashed_password']):
            session['user'] = user['user_name']
            return redirect('/')
        else:
            message = "Login failed. Please check your details."
            return render_template('login.html',
                                   message=message,)
    return render_template('login.html')


@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user', None)
        return redirect('/')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
