from flask import Flask, render_template, request, redirect, url_for

import data_handler

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    questions = data_handler.get_all_question(convert_linebreaks=True)

    return render_template('list.html', questions=questions)


@app.route('/newquestion')
def route_question():
    return render_template('question.html')

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
