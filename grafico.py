
'''
import matplotlib.pyplot as plt
import pandas as pd
from math import pi
def grafico():
    #DATA SET
    df = pd.DataFrame({
        'group' : ['A','B','C','D'],
        'var1' : [38, 1.5, 30, 4],
        'var2': [29, 10, 9, 34],
        'var3': [8, 39, 23, 24],
        'var4': [7, 31, 33, 14],
        'var5': [28, 15, 32, 14]
    })

    #CREAZIONE BACKGROUND PT.1

    #NUMERO DI VARIABILI
    categorie = list(df)[1:]
    N = len(categorie)

    #CALCOLIAMO L'ANGOLO DI CIASCUN ASSE NEL GRAFICO (dividiamo n/ numero di variabili)
    angoli= [n / float(N) * 2 * pi for n in range(N)]
    angoli += angoli[:1]

    #CREIAMO LO SPIDER PLOT
    ax = plt.subplot(111, polar=True)

    #SE VOGLIAMO CHE LA PRIMA ASSE SIA ON THE TOP:
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    #DISEGNAMO UN ASCIA PER VARIABILE + AGGIUNGIAMO DELLE ETICHETTE
    plt.xticks(angoli[:-1], categorie)

    #DISEGNAMO LE ETICHETTE
    ax.set_rlabel_position(0)
    plt.yticks([10,20,30], ["10","20","30"], color="grey", size=7)
    plt.ylim(0,40)

    #aggiungi argomenti pt.2

    #IND1
    values=df.loc[0].drop("group").values.flatten().tolist()
    values += values[:1]
    ax.plot(angoli , values, linewidth=1, linestyle='solid', label="group A")
    ax.fill(angoli, values, 'b', alpha=0.1)

    #IND2
    values=df.loc[1].drop("group").values.flatten().tolist()
    values += values[:1]
    ax.plot(angoli, values, linewidth=1, linestyle='solid', label="group B")
    ax.fill(angoli, values, 'r', alpha=0.1)

    #AGGIUNGIAMO LEGGENDA
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

    #PER VEDERE IL GRAFICO
    plt.show()
'''

from flask import Flask, render_template
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def plot():
    left = [1, 2, 3, 4, 5]
    # heights of bars
    height = [10, 24, 36, 40, 5]
    # labels for bars
    tick_label = ['one', 'two', 'three', 'four', 'five']
    # plotting a bar chart
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['red', 'green'])

    # naming the y-axis
    plt.ylabel('y - axis')
    # naming the x-axis
    plt.xlabel('x - axis')
    # plot title
    plt.title('My bar chart!')

    plt.savefig('static/images/plot.png')

    return render_template('plot.html', url='/static/images/plot.png')

if __name__ == '__main__':
   app.run()