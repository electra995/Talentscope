import csv
import mysql.connector


def lettore_csv(file):
    lista = []
    with open(file, encoding='utf-8') as file_csv:
        lettore = csv.reader(file_csv, delimiter=";")
        lettore.__next__()
        for riga in lettore:
            lista.append(tuple(riga))
    return lista


lista_u = [('Matteo', 'Barone', 'mail', 'pass', '1', '10', '11', '12', '13', '14')]
# data analyst = 1
# data scientist = 0
lista_voti = [('10', '10', '10', '10', '10'), ('10', '10', '10', '10', '10')]

per1 = './Assessment.csv'

# print(lettorecsv(per1))
lista_dom = lettore_csv(per1)
print(lista_dom)
# print(lettorejson(per2))
# lista2= lettore(per2)

# Creare un database
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
)
my_cursor = mydb.cursor()
# print(mycursor)

my_cursor.execute('CREATE DATABASE TALENTSC;')
my_cursor.execute('USE TALENTSC;')
# mycursor.execute("DROP TABLE ASSESMENT;")

# Creo una tabella
sql1 = "CREATE TABLE ASSESMENT(ID INT NOT NULL AUTO_INCREMENT, SKILL VARCHAR(20), DOMANDA VARCHAR(1000), RISPOSTA1 VARCHAR(1000), RISPOSTA2 VARCHAR(1000),RISPOSTA3 VARCHAR(1000), RISPOSTAESATTA VARCHAR(1000), PRIMARY KEY (ID));"
my_cursor.execute(sql1)
sql1c = "INSERT INTO ASSESMENT(SKILL, DOMANDA, RISPOSTA1, RISPOSTA2, RISPOSTA3, RISPOSTAESATTA) VALUES (%s, %s, %s, %s, %s, %s);"
my_cursor.executemany(sql1c, lista_dom)
mydb.commit()
# mycursor.execute("SELECT * FROM ASSESMENT;")


sqlu = "CREATE TABLE UTENTE(NOME VARCHAR(1000), COGNOME VARCHAR(1000), EMAIL VARCHAR(1000), PASSWORD VARCHAR(1000), RUOLO VARCHAR(1000), VOTO1 VARCHAR(1000), VOTO2 VARCHAR(1000), VOTO3 VARCHAR(1000), VOTO4 VARCHAR(1000), VOTO5 VARCHAR(1000));"
my_cursor.execute(sqlu)
sql1u = "INSERT INTO UTENTE(NOME, COGNOME, EMAIL, PASSWORD, RUOLO, VOTO1, VOTO2, VOTO3, VOTO4, VOTO5) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
my_cursor.executemany(sql1u, lista_u)
mydb.commit()
my_cursor.execute("SELECT * FROM UTENTE;")
for i in my_cursor:
    print(i)

# mycursor.execute("DROP TABLE DATA;")
sqld = "CREATE TABLE DATA(SQUL VARCHAR(100), EXCEL VARCHAR(100), PYTHON VARCHAR(100), POWBI VARCHAR(100), TABLO VARCHAR(100));"
my_cursor.execute(sqld)
sql1d = "INSERT INTO DATA(SQUL, EXCEL, PYTHON, POWBI, TABLO) VALUES ( %s, %s, %s, %s, %s);"
my_cursor.executemany(sql1d, lista_voti)
mydb.commit()
my_cursor.execute("SELECT * FROM DATA;")
for i in my_cursor:
    print(i)

# mycursor.execute("DROP TABLE SCIENT;")
sqls = "CREATE TABLE SCIENT(ML VARCHAR(100), PHYTON VARCHAR(100), SQUL VARCHAR(100), AWS VARCHAR(100), R VARCHAR(100));"
my_cursor.execute(sqls)
sql1s = "INSERT INTO SCIENT(ML, PHYTON, SQUL, AWS, R) VALUES (%s, %s, %s, %s, %s);"
my_cursor.executemany(sql1s, lista_voti)
mydb.commit()
my_cursor.execute("SELECT * FROM SCIENT;")
for i in my_cursor:
    print(i)
