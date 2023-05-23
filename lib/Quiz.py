import random


class Quiz:

    def __init__(self,
                 id: int,
                 skill: str,
                 domanda: str,
                 risposta1: str,
                 risposta2: str,
                 risposta3: str,
                 risposta_esatta: str,
                 risposta_data: str = ''
                 ):
        self.id = id
        self.skill = skill
        self.domanda = domanda
        risposte = {'RISPOSTA1': risposta1, 'RISPOSTA2': risposta2, 'RISPOSTA3': risposta3,
                    'RISPOSTAESATTA': risposta_esatta, 'RISPOSTA': risposta_data}
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

    def check_risposta(self) -> bool:
        """
        Fa un check per controllare se la risposta dell'utente è corretta o sbagliata.
        :return: True se la risposta data dall'utente è corretta, False se la risposta è sbagliata.
        """
        if self.risposte['RISPOSTA'] == self.risposte['RISPOSTAESATTA']:
            return True
        else:
            return False
