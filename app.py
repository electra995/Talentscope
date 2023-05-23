import json
from flask import Flask, redirect, url_for
from flask import render_template
from flask import request
from lib.Database import DB
from lib.Quiz import Quiz
from lib.Contatore import Contatore
from lib.grafico import plot

app = Flask(__name__)

with open('db/config.json', 'r') as f:
    config = json.load(f)


def domande_per_skill(skill: str, limit: int) -> list:
    """
    Interroga il database e aggiunge alla lista quiz_per_skill gli oggetti Quiz.
    :param limit: Il limite di domande da proporre.
    :param skill: Il nome della skill.
    :return: Lista di domande per skill.
    """
    quiz_per_skill = []
    connection: DB = DB(config)
    query: str = f'SELECT * FROM ASSESSMENT ' \
                 f'WHERE SKILL = "{skill}" ' \
                 f'ORDER BY RAND() LIMIT {limit}'

    righe: list = connection.fetch(query, args=None)
    del connection

    for riga in righe:
        quiz = Quiz(riga[0], riga[1], riga[2], riga[3], riga[4], riga[5], riga[6])
        quiz_per_skill.append(quiz)

    return quiz_per_skill


def inserisci_modifica_risposte(email: str):
    """
    Inserisce o modifica le risposte per ogni utente nella tabella ANSWERS del DB.
    :param email: L'email dell'utente.
    :return:
    """
    connection: DB = DB(config)
    risposte = dict(request.form)
    for key in risposte.keys():
        query = f'SELECT RISPOSTA FROM ANSWERS ' \
                f'WHERE IDDOMANDA = "{key}" AND EMAIL = "{email}";'

        check: str = connection.fetchone(query, args=None)
        query = f'SELECT {risposte[key]}, SKILL FROM ASSESSMENT ' \
                f'WHERE ID = "{key}";'

        risposta_skill: tuple = connection.fetchone(query, args=None)
        risposta: str = risposta_skill[0]
        skill: str = risposta_skill[1]
        if check is None:
            query = f'SELECT ID FROM SKILLS ' \
                    f'WHERE SKILL = "{skill}"'

            skill_id: str = connection.fetchone(query, args=None)[0]
            query = f'INSERT INTO ANSWERS(IDDOMANDA, IDSKILL, RISPOSTA, EMAIL) VALUES (%s, %s, %s, %s);'
            args = (key, skill_id, risposta, email)
            connection.insert(query, args=args)
        else:
            query = f'UPDATE ANSWERS SET RISPOSTA = "{risposta}" ' \
                    f'WHERE IDDOMANDA = "{key}" AND EMAIL = "{email}";'

            connection.update(query, args=None)
    del connection


def risposte_totali(email: str, role: str) -> list:
    """
    Crea degli oggetti Quiz partendo dalle domande inserite nella tabella ANSWERS del DB.
    :param email: L'email dell'utente.
    :param role: La figura lavorativa scelta dall'utente.
    :return: Lista di oggetti Quiz.
    """
    quiz_tot = []
    connection: DB = DB(config)

    if role == 'data_analyst':
        role = 1
    else:
        role = 0

    query = f'SELECT ASSESSMENT.*, ANSWERS.RISPOSTA ' \
            f'FROM ASSESSMENT ' \
            f'JOIN ANSWERS ON ASSESSMENT.ID = ANSWERS.IDDOMANDA ' \
            f'JOIN SKILLS ON ASSESSMENT.SKILL = SKILLS.SKILL ' \
            f'WHERE ANSWERS.EMAIL = "{email}" ' \
            f'AND (SKILLS.ROLE = "{role}" OR SKILLS.ROLE = "2");'

    righe: tuple = connection.fetch(query, args=None)
    for riga in righe:
        quiz = Quiz(riga[0], riga[1], riga[2], riga[3], riga[4], riga[5], riga[6], riga[7])
        quiz_tot.append(quiz)

    return quiz_tot


def contatore_totale(quiz_tot: list) -> list:
    """
    Crea degli oggetti Contatore che divide le domande esatte per ogni skill.
    :param quiz_tot: La lista di oggetti Quiz.
    :return: Lista di oggetti Contatore.
    """
    counter_tot = []
    counter_dict = {}

    for quiz in quiz_tot:
        skill = quiz.skill
        if skill in counter_dict:
            counter_dict[skill][0] += quiz.check_risposta()
            counter_dict[skill][1] += 1
        else:
            counter_dict[skill] = [quiz.check_risposta(), 1]

    for skill, (risposte_corrette, totale_domande) in counter_dict.items():
        counter_tot.append(Contatore(skill, risposte_corrette, totale_domande))

    return counter_tot


def cancella_dati(email: str):
    """
    Elimina i dati relativi a un utente.
    :param email: L'email dell'utente.
    :return:
    """
    connection: DB = DB(config)
    query = f'DELETE FROM ANSWERS ' \
            f'WHERE EMAIL = "{email}" AND ID <> 0;'

    connection.update(query, args=None)
    del connection


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/valutazione')
def seconda():
    return render_template('seconda.html')


@app.route('/quiz', methods=['GET'])
def questionario():
    limit: int = 3
    skill = request.args.get('skill')
    role = request.args.get('role')
    email = request.args.get('email')

    if role == 'data_analyst':
        if skill == 'inizio':
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
            quiz_tot: list = risposte_totali(email, role)
            counter_tot: list = contatore_totale(quiz_tot)
            plot(role, counter_tot)
            return render_template('evaluation_analyst.html', quiz_tot=quiz_tot, counter_tot=counter_tot, email=email)

    else:
        if skill == 'inizio':
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
            quiz_tot: list = risposte_totali(email, role)
            counter_tot: list = contatore_totale(quiz_tot)
            plot(role, counter_tot)
            return render_template('evaluation_scientist.html', quiz_tot=quiz_tot, counter_tot=counter_tot, email=email)

    quiz_per_skill = domande_per_skill(skill, limit)

    return render_template('quiz.html',
                           quiz_per_skill=quiz_per_skill,
                           skill=skill,
                           role=role,
                           email=email)


@app.route('/quiz/post/', methods=['POST'])
def post_quiz():
    skill = request.args.get('skill')
    role = request.args.get('role')
    email = request.args.get('email')
    inserisci_modifica_risposte(email)

    return redirect(url_for('questionario', skill=skill, role=role, email=email))


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


@app.route('/reset')
def reset():
    email = request.args.get('email')
    cancella_dati(email)
    return redirect(url_for('seconda'))


@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template('error404.html'), 404


if __name__ == '__main__':
    app.run()
