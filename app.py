from flask import Flask, redirect, url_for
from flask import render_template
from flask import request
from lib.Database import DB
from lib.Quiz import Quiz

app = Flask(__name__)
quiz_tot = []
quiz_per_skill = []

config = {
    'user': 'root',
    'password': '****',
    'host': 'localhost',
    'database': '****'
}


def query_db(skill: str):
    """
    Interroga il database e aggiunge alla lista quiz_per_skill gli oggetti Quiz.
    :param skill: Il nome della skill.
    :return:
    """
    global quiz_per_skill
    quiz_per_skill = []
    connection: DB = DB(config)
    query: str = f'SELECT * FROM ASSESMENT WHERE SKILL = "{skill}" LIMIT 3'
    righe: list = connection.fetch(query, args=None)
    del connection

    for riga in righe:
        quiz = Quiz(riga[0], riga[1], riga[2], riga[3], riga[4], riga[5], riga[6])
        quiz_per_skill.append(quiz)


def popola_quiz():
    """
    Riempie la lista quiz_tot con gli oggetti Quiz impostando anche la risposta dell'utente.
    :return:
    """
    global quiz_per_skill
    global quiz_tot
    risposte = dict(request.form)
    for key in risposte.keys():
        for quiz in quiz_per_skill:
            if quiz.id == int(key):
                quiz.set_risposta_data(risposte[key])
                quiz_tot.append(quiz)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/quiz/<skill>&<role>', methods=['GET'])
def questionario(skill: str, role: str):
    global quiz_per_skill
    global quiz_tot

    if role == 'data_analyst':

        if skill == 'inizio':
            skill = 'aws'
        elif skill == 'aws':
            skill = 'python'
        elif skill == 'python':
            skill = 'AZURE'
        elif skill == 'AZURE':
            skill = 'GOOGLE CLOUD'
        elif skill == 'GOOGLE CLOUD':
            return render_template('valutazioni.html', quiz_tot=quiz_tot)

    else:
        pass

    query_db(skill)

    return render_template('quiz.html', quiz_per_skill=quiz_per_skill, skill=skill, role=role)


@app.route('/post/quiz/', methods=['POST'])
def post_quiz():
    skill = request.args.get('skill')
    role = request.args.get('role')
    popola_quiz()

    return redirect(url_for('questionario', skill=skill, role=role))


if __name__ == '__main__':
    app.run()
