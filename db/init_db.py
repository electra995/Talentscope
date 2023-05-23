import csv
import json
from lib.Database import DB


def lettore_csv(file):
    lista = []
    with open(file, encoding='utf-8') as file_csv:
        lettore = csv.reader(file_csv, delimiter=";")
        lettore.__next__()
        for riga in lettore:
            lista.append(tuple(riga))
    return lista


per1 = './Assessment.csv'
lista_dom = lettore_csv(per1)

with open('config.json', 'r') as f:
    config = json.load(f)

connection: DB = DB(config)

# data analyst = 1
# data scientist = 0
# both = 2
lista_skill = [('AWS', '1'), ('Python', '2'), ('MySQL', '2'), ('Excel', '1'), ('PowerBI', '1'),
               ('ML', '0'), ('R', '0'), ('Git', '0')]

# Creare un database
connection.query('CREATE DATABASE TALENTSC;', args=None)
connection.query('USE TALENTSC;', args=None)

# Creo una tabella
query = "CREATE TABLE SKILLS(ID INT NOT NULL AUTO_INCREMENT, SKILL VARCHAR(100), ROLE VARCHAR(100), PRIMARY KEY (ID));"
connection.query(query, args=None)
query = "INSERT INTO SKILLS(SKILL, ROLE) VALUES ( %s, %s);"
connection.insertmany(query, lista_skill)

query = "CREATE TABLE ASSESSMENT(ID INT NOT NULL AUTO_INCREMENT, SKILL VARCHAR(20), DOMANDA VARCHAR(1000), " \
        "RISPOSTA1 VARCHAR(1000), RISPOSTA2 VARCHAR(1000),RISPOSTA3 VARCHAR(1000), RISPOSTAESATTA VARCHAR(1000), " \
        "PRIMARY KEY (ID));"
connection.query(query, args=None)
query = "INSERT INTO ASSESSMENT(SKILL, DOMANDA, RISPOSTA1, RISPOSTA2, RISPOSTA3, RISPOSTAESATTA) VALUES (%s, %s, %s, " \
        "%s, %s, %s);"
connection.insertmany(query, lista_dom)

query = "CREATE TABLE ANSWERS(ID INT NOT NULL AUTO_INCREMENT, IDDOMANDA INT, IDSKILL INT, RISPOSTA VARCHAR(1000), " \
        "EMAIL VARCHAR(100)," \
        "PRIMARY KEY (ID), FOREIGN KEY (IDDOMANDA) REFERENCES ASSESSMENT(ID), FOREIGN KEY (IDSKILL) REFERENCES " \
        "SKILLS(ID));"
connection.query(query, args=None)
