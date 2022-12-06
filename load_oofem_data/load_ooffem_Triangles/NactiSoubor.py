
class txt:

    def __init__(self, adresaXML):

        self.pole = []
        self.adresaXML = adresaXML
        self.nacitejXML()


    def getPole(self):
        return(self.pole);


    def nacitejXML(self):

        self.pole = self.nactiXML()
        print("")


    def nactiXML(self):

        pole = []

        r = -1
        with open(self.adresaXML, 'r') as f:
            for line in f:
                r = r + 1

                pole.append(line)

        return (pole)