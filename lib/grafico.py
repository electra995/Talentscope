import pandas as pd
from math import pi
import matplotlib.pyplot as plt
import os


def plot(role):
    # DATA SET
    df = pd.DataFrame({
        'group': ['A', 'B'],
        'AWS': [3, 1.5],
        'Python': [3, 1],
        'Azure': [3, 2],
        'Google Cloud': [3, 1],
        'placeholder': [3, 1]
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
    plt.yticks([1, 2, 3], ["1", "2", "3"], color="grey", size=7)
    plt.ylim(0, 3)

    # aggiungi argomenti pt.2

    # IND1
    values = df.loc[0].drop("group").values.flatten().tolist()
    values += values[:1]
    ax.plot(angoli, values, linewidth=1, linestyle='solid', label=f"{role}")
    ax.fill(angoli, values, 'b', alpha=0.1)

    # IND2
    values = df.loc[1].drop("group").values.flatten().tolist()
    values += values[:1]
    ax.plot(angoli, values, linewidth=1, linestyle='solid', label="mocc a sort")
    ax.fill(angoli, values, 'r', alpha=0.1)

    # AGGIUNGIAMO LEGGENDA
    plt.legend(loc='lower left', bbox_to_anchor=(-0.3, -0.1))

    # PER VEDERE IL GRAFICO
    # plt.show()

    # plt.title('My chart!')
# plot(role)
    os.makedirs('./static/images', exist_ok=True)
    plt.savefig('./static/images/chart.png')
