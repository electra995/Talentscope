import plotly.graph_objects as go
import plotly.offline as py


def plot(role, counter_tot, domande_tot):
    print(role)
    if role == 'data analyst':
        categories = ['AWS', 'Python', 'Azure', 'Google Cloud', 'PowerBI']

    else:
        categories = ['ML', 'Python', 'MySql', 'R', 'Git']

    categories = [*categories, categories[0]]

    perfect_skills = [domande_tot, domande_tot, domande_tot, domande_tot, domande_tot]
    user = [x.risposte_esatte for x in counter_tot]
    perfect_skills = [*perfect_skills, perfect_skills[0]]
    user = [*user, user[0]]

    fig = go.Figure(
        data=[
            go.Scatterpolar(r=perfect_skills, theta=categories, fill='toself', name=role),
            go.Scatterpolar(r=user, theta=categories, fill='toself', name='your result'),
        ],
        layout=go.Layout(
            title=go.layout.Title(text='Results'),
            polar={'radialaxis': {'visible': True}},
            showlegend=True
        )
    )

    py.plot(fig, auto_open=False, filename='./templates/chart.html')
