import random


class Quiz:

    def __init__(self,
                 id: int,
                 skill: str,
                 domanda: str,
                 risposta1: str,
                 risposta2: str,
                 risposta3: str,
                 risposta_esatta: str
                 ):
        self.id = id
        self.skill = skill
        self.domanda = domanda
        risposte = {'R1': risposta1, 'R2': risposta2, 'R3': risposta3, 'Esatta': risposta_esatta, 'Data': ''}
        risposte = Quiz.mescola_dizionario(risposte)
        self.risposte = risposte

    @classmethod
    def mescola_dizionario(cls, dizionario: dict) -> dict:
        """
        Metodo di classe per randomizzare il dizionario delle domande.
        :param dizionario: Il dizionario delle domande con la relativa risposta esatta.
        :return: Dizionario delle domande randomizzato.
        """
        items = list(dizionario.items())
        random.shuffle(items)
        return dict(items)

    def __str__(self):
        return f'{self.risposte}'

    def set_risposta_data(self, risposta: str):
        """
        Imposta la risposta data dall'utente alla domanda.
        :param risposta: La risposta data dall'utente come chiave delle risposte (es. R1, R2, R3, Esatta).
        :return:
        """
        self.risposte['Data'] = risposta

    def check_risposta(self) -> bool:
        """
        Fa un check per controllare se la risposta dell'utente è corretta o sbagliata.
        :return: True se la risposta data dall'utente è corretta, False se la risposta è sbagliata.
        """
        if self.risposte['Data'] == 'Esatta':
            return True
        else:
            return False
