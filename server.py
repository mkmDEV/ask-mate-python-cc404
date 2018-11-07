from flask import Flask, render_template, request, redirect, url_for
import data_handler

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def home():
    questions = data_handler.get_all_question(convert_linebreaks=True)
    return render_template('list.html', questions=questions, page_title='Welcome')


@app.route('/newquestion')
def route_question():
    return render_template('question.html')


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def display_question(question_id :int):
    question_data = data_handler.get_question(question_id)
    return render_template('single_question.html',
                           question=question_data,
                           page_title=question_data['title'],
                           )


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
