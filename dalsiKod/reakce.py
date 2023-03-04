
class reakceData:

    def __init__(self, reactionsOutput, uzlyAJejichSouradnice):

        self.reactionsOutput = reactionsOutput
        self.uzlyAJejichSouradnice = uzlyAJejichSouradnice

        self.reakceAJejichSouradnice = self.priradSouradniceKeVsemOFT(self.reactionsOutput, self.uzlyAJejichSouradnice)


    def getReakceAJejichSouradnice(self):
        return(self.reakceAJejichSouradnice)



    def priradSouradniceKeVsemOFT(self, reactionsOutput, uzlyAJejichSouradnice):

        reakceSouradnice = []

        for OFT in range(0, len(reactionsOutput)):
            reactionsOutputOFT = reactionsOutput[OFT]
            reakceSouradniceOFT = self.priradSouradniceKJednomuOFT(reactionsOutputOFT, uzlyAJejichSouradnice)
            reakceSouradnice.append(reakceSouradniceOFT)

        return(reakceSouradnice)


    def priradSouradniceKJednomuOFT(self, reactionsOutputOFT, uzlyAJejichSouradnice):

        reakceSouradniceOFT = []

        for iRadek in range(0, len(reactionsOutputOFT)):
            radek = reactionsOutputOFT[iRadek]
            cisloUzlu = radek[0]
            velikostiSil = radek[2]
            souradniceUzlu = self.vyhledejSouradnicePodleCislaUzlu(uzlyAJejichSouradnice, cisloUzlu)

            radekNew = []
            radekNew.append(cisloUzlu)
            radekNew.append(souradniceUzlu)
            radekNew.append(velikostiSil)

            reakceSouradniceOFT.append(radekNew)

        return(reakceSouradniceOFT)


    def vyhledejSouradnicePodleCislaUzlu(self, uzlyAJejichSouradnice, cisloUzluExp):

        souradniceUzlu = []

        for iUzel in range(0, len(uzlyAJejichSouradnice)):
            uzelRadek = uzlyAJejichSouradnice[iUzel]
            cisloUzlu = uzelRadek[0]

            if(cisloUzlu == cisloUzluExp):
                souradniceUzlu = uzelRadek
                break

        return(souradniceUzlu)
