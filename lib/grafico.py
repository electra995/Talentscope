import pandas as pd
from math import pi
import matplotlib.pyplot as plt


def plot():
    # DATA SET
    df = pd.DataFrame({
        'group': ['A', 'B', 'C', 'D'],
        'var1': [40, 1.5, 30, 4],
        'var2': [40, 40, 40, 40],
        'var3': [40, 39, 23, 24],
        'var4': [40, 31, 33, 14],
        'var5': [40, 15, 32, 14]
    })

    # CREAZIONE BACKGROUND PT.1

    # NUMERO DI VARIABILI
    categorie = list(df)[1:]
    N = len(categorie)

    # CALCOLIAMO L'ANGOLO DI CIASCUN ASSE NEL GRAFICO (dividiamo n/ numero di variabili)
    angoli = [n / float(N) * 2 * pi for n in range(N)]
    angoli += angoli[:1]

    # CREIAMO LO SPIDER PLOT
    ax = plt.subplot(111, polar=True)

    # SE VOGLIAMO CHE LA PRIMA ASSE SIA ON THE TOP:
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    # DISEGNAMO UN ASCIA PER VARIABILE + AGGIUNGIAMO DELLE ETICHETTE
    plt.xticks(angoli[:-1], categorie)

    # DISEGNAMO LE ETICHETTE
    ax.set_rlabel_position(0)
    plt.yticks([10, 20, 30], ["10", "20", "30"], color="grey", size=7)
    plt.ylim(0, 40)

    # aggiungi argomenti pt.2

    # IND1
    values = df.loc[0].drop("group").values.flatten().tolist()
    values += values[:1]
    ax.plot(angoli, values, linewidth=1, linestyle='solid', label="group A")
    ax.fill(angoli, values, 'b', alpha=0.1)

    # IND2
    values = df.loc[1].drop("group").values.flatten().tolist()
    values += values[:1]
    ax.plot(angoli, values, linewidth=1, linestyle='solid', label="group B")
    ax.fill(angoli, values, 'r', alpha=0.1)

    # AGGIUNGIAMO LEGGENDA
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

    # PER VEDERE IL GRAFICO
#    plt.show()
    # plot title
    plt.title('My chart!')

    plt.savefig('static/images/chart.png')
