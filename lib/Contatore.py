class Contatore:

    def __init__(self,
                 skill: str,
                 risposte_esatte: int,
                 risposte_tot: int,
                 ):

        self.skill = skill
        self.risposte_esatte = risposte_esatte
        self.risposte_tot = risposte_tot

    def __str__(self):
        return f'skill: {self.skill}, risposte_esatte: {self.risposte_esatte}, risposte_tot: {self.risposte_tot}'

    def percentuale(self):
        return round((self.risposte_esatte / self.risposte_tot) * 100, 2)
