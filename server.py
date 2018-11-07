from flask import Flask, render_template, request, redirect, url_for
import data_handler

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    questions = data_handler.get_all_question(convert_linebreaks=True)

    return render_template('list.html', questions=questions, page_title='Welcome')


@app.route('/newquestion')
def route_question():
    return render_template('question.html')


@app.route('/question/<question_id>')
def display_question(question_id: int):

    question = {
        'id': 1,
        'submission_time': '2018-11-05',
        'title': "This is a test post",
        'content': "First question content comes here",
        'image': 'default.jpg'
        }

    return render_template('single_question.html',
                           question_id=question['id'],
                           page_title=question['title'])


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
