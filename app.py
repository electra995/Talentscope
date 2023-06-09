import json
from itertools import groupby
from flask import Flask, redirect, url_for
from flask import render_template
from flask import request
from lib.Database import DB
from lib.Quiz import Quiz
from lib.Contatore import Contatore
from lib.grafico import plot

app = Flask(__name__)
quiz_tot = []
quiz_per_skill = []

with open('db/config.json', 'r') as f:
    config = json.load(f)


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


def popola_counter():
    """
    Raggruppa le risposte totali per ogni skill e popola una lista di oggetti Contatore in cui tenere traccia delle
    risposte corrette date dall'utente.
    :return: Lista di oggetti contatore.
    """
    global quiz_tot
    risposte_per_skill = {}
    counter_tot = []

    for key, group in groupby(quiz_tot, lambda x: x.skill):
        risposte_per_skill[key] = list(group)

    for key in risposte_per_skill.keys():
        counter = 0
        for quiz in risposte_per_skill[key]:
            if quiz.check_risposta():
                counter += 1
        counter_tot.append(Contatore(key, counter, len(risposte_per_skill[key])))

    return counter_tot


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/valutazione')
def seconda():
    return render_template('seconda.html')


@app.route('/quiz/<skill>&<role>', methods=['GET'])
def questionario(skill: str, role: str):
    global quiz_per_skill
    global quiz_tot

    if role == 'data analyst':

        if skill == 'inizio':
            quiz_tot = []
            skill = 'AWS'
        elif skill == 'AWS':
            skill = 'Python'
        elif skill == 'Python':
            skill = 'MySQL'
        elif skill == 'MySQL':
            skill = 'Excel'
        elif skill == 'Excel':
            skill = 'PowerBI'
        elif skill == 'PowerBI':
            counter_tot = popola_counter()
            plot(role, counter_tot, len(quiz_per_skill))
            return render_template('evaluation_analyst.html', quiz_tot=quiz_tot, counter_tot=counter_tot)

    else:
        if skill == 'inizio':
            quiz_tot = []
            skill = 'ML'
        elif skill == 'ML':
            skill = 'Python'
        elif skill == 'Python':
            skill = 'MySQL'
        elif skill == 'MySQL':
            skill = 'R'
        elif skill == 'R':
            skill = 'Git'
        elif skill == 'Git':
            counter_tot = popola_counter()
            plot(role, counter_tot, len(quiz_per_skill))
            return render_template('evaluation_scientist.html', quiz_tot=quiz_tot, counter_tot=counter_tot)

    query_db(skill)

    return render_template('quiz.html', quiz_per_skill=quiz_per_skill, skill=skill, role=role)


@app.route('/post/quiz/', methods=['POST'])
def post_quiz():
    skill = request.args.get('skill')
    role = request.args.get('role')
    popola_quiz()

    return redirect(url_for('questionario', skill=skill, role=role))


@app.route('/about')
def about_us():
    return render_template('about_us.html')


@app.route('/graph')
def graph():
    return render_template('grafici.html')


@app.route('/chart-analyst')
def chart_analyst():
    return render_template('chart-analyst.html')


@app.route('/chart-scientist')
def chart_scientist():
    return render_template('chart-scientist.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404


if __name__ == '__main__':
    app.run()
