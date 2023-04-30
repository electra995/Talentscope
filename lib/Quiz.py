class Quiz:
    def __init__(self, id, skill, domanda, risposta1, risposta2, risposta3, risposta_esatta):
        self.id = id
        self.skill = skill
        self.domanda = domanda
        self.risposte = {
            'R1': risposta1,
            'R2': risposta2,
            'R3': risposta3,
            'Esatta': risposta_esatta,
            'Data': ''
        }

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
