class Contatore:

    def __init__(self,
                 skill: str,
                 risposte_esatte: int,
                 risposte_tot: int,
                 ):

        self.skill = skill
        self.risposte_esatte = risposte_esatte
        self.risposte_tot = risposte_tot

    def percentuale(self):
        return (self.risposte_esatte / self.risposte_tot) * 100
