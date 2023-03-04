
# dopocita meritko grafu, tak aby se JSON zobrazil v meritku a byl citelny
class meritkoGraf:

    def __init__(self, dataGraf, output):

        self.maximalniDovolenaHodnota = 40
        self.meritkaGrafy = []
        self.output = output

        self.dataGraf = dataGraf

        if(output == True):
            self.meritkaGrafy = self.ziskejDataOFTOutputs(self.dataGraf)

        if(output == False):
            self.meritkaGrafy = self.ziskejDataOFTInputs(self.dataGraf)


    # getry
    def getMeritkaGrafy(self):
        return(self.meritkaGrafy)


    def ziskejDataOFTInputs(self, dataGraf):

        meritkaPole = []
        meritkoUPole = []
        meritkoVPole = []
        meritkoFiPole = []

        """
        maximalniHodnotaU = 0
        maximalniHodnotaV = 0
        maximalniHodnotaFi = 0
        """

        maximalniHodnotaUPredchozi = 0
        maximalniHodnotaVPredchozi = 0
        maximalniHodnotaFiPredchozi = 0

        for OFT in range(0, len(dataGraf)):
            meritkaPole = []
            dataGrafOFT = dataGraf[OFT]

            # hodnoty u - zacatek a konec prutu
            hodnotyUZacatekPrutu = dataGrafOFT[0]
            hodnotyUKonecPrutu = dataGrafOFT[3]

            # hodnoty v - zacatek a konec prutu
            hodnotyVZacatekPrutu = dataGrafOFT[1]
            hodnotyVKonecPrutu = dataGrafOFT[4]

            # hodnoty fi - zacatek a konec prutu
            hodnotyFiZacatekPrutu = dataGrafOFT[2]
            hodnotyFiKonecPrutu = dataGrafOFT[5]

            # maximalni hodnoty
            maximalniHodnotaU = max(abs(float(hodnotyUZacatekPrutu)), abs(float(hodnotyUKonecPrutu)))
            maximalniHodnotaV = max(abs(float(hodnotyVZacatekPrutu)), abs(float(hodnotyVKonecPrutu)))
            maximalniHodnotaFi = max(abs(float(hodnotyFiZacatekPrutu)), abs(float(hodnotyFiKonecPrutu)))

            maximalniHodnotaU = max(maximalniHodnotaU, maximalniHodnotaUPredchozi)
            maximalniHodnotaV = max(maximalniHodnotaV, maximalniHodnotaVPredchozi)
            maximalniHodnotaFi = max(maximalniHodnotaFi, maximalniHodnotaFiPredchozi)

            maximalniHodnotaUPredchozi = maximalniHodnotaU
            maximalniHodnotaVPredchozi = maximalniHodnotaV
            maximalniHodnotaFiPredchozi = maximalniHodnotaFi

            print("")

        meritkoU = self.dopocitejMeritko(maximalniHodnotaU)
        meritkoV = self.dopocitejMeritko(maximalniHodnotaV)
        meritkoFi = self.dopocitejMeritko(maximalniHodnotaFi)

        """
        meritkoUPole.append(meritkoU)
        meritkoVPole.append(meritkoV)
        meritkoFiPole.append(meritkoFi)
        """

        meritkaPole.append(meritkoU)
        meritkaPole.append(meritkoV)
        meritkaPole.append(meritkoFi)

        return (meritkaPole)


    def ziskejDataOFTOutputs(self, dataGraf):

        meritkaPole = []
        meritkoUPole = []
        meritkoVPole = []
        meritkoFiPole = []

        for OFT in range(0, len(dataGraf)):
            meritkaPole = []
            dataGrafOFT = dataGraf[OFT]

            # hodnoty u - zacatek a konec prutu
            hodnotyUZacatekPrutu = self.vyberPoleHodnotProDanyIndex(dataGrafOFT, 0)
            hodnotyUKonecPrutu = self.vyberPoleHodnotProDanyIndex(dataGrafOFT, 3)

            # hodnoty v - zacatek a konec prutu
            hodnotyVZacatekPrutu = self.vyberPoleHodnotProDanyIndex(dataGrafOFT, 1)
            hodnotyVKonecPrutu = self.vyberPoleHodnotProDanyIndex(dataGrafOFT, 4)

            # hodnoty fi - zacatek a konec prutu
            hodnotyFiZacatekPrutu = self.vyberPoleHodnotProDanyIndex(dataGrafOFT, 2)
            hodnotyFiKonecPrutu = self.vyberPoleHodnotProDanyIndex(dataGrafOFT, 5)

            # maximalni Hodnota u
            maximalniHodnotaU = self.vratMaximalniHodnotu(hodnotyUZacatekPrutu, 0)
            maximalniHodnotaU = self.vratMaximalniHodnotu(hodnotyUKonecPrutu, maximalniHodnotaU)

            # maximalni hodnota v
            maximalniHodnotaV = self.vratMaximalniHodnotu(hodnotyVZacatekPrutu, 0)
            maximalniHodnotaV = self.vratMaximalniHodnotu(hodnotyVKonecPrutu, maximalniHodnotaV)

            # maximalni hodnota fi
            maximalniHodnotaFi = self.vratMaximalniHodnotu(hodnotyFiZacatekPrutu, 0)
            maximalniHodnotaFi = self.vratMaximalniHodnotu(hodnotyFiKonecPrutu, maximalniHodnotaFi)

            meritkoU = self.dopocitejMeritko(maximalniHodnotaU)
            meritkoV = self.dopocitejMeritko(maximalniHodnotaV)
            meritkoFi = self.dopocitejMeritko(maximalniHodnotaFi)

            meritkoUPole.append(meritkoU)
            meritkoVPole.append(meritkoV)
            meritkoFiPole.append(meritkoFi)

        meritkaPole.append(meritkoUPole)
        meritkaPole.append(meritkoVPole)
        meritkaPole.append(meritkoFiPole)

        return (meritkaPole)


    def vyberPoleHodnotProDanyIndex(self, dataGrafOFT, index):

        hodnotyIndexPole = []

        if(dataGrafOFT[0] == '0.0'):
            print("")

        for i in range(0, len(dataGrafOFT)):
            dataGrafOFTRadek = dataGrafOFT[i]
            hodnotaIndex = dataGrafOFTRadek[index]

            hodnotyIndexPole.append(hodnotaIndex)

        return(hodnotyIndexPole)


    def vratMaximalniHodnotu(self, dataPole, hodnotaMax):

        for i in range(0, len(dataPole)):
            hodnota = dataPole[i]
            if(abs(float(hodnota)) > hodnotaMax):
                hodnotaMax = abs(float(hodnota))

        return(hodnotaMax)


    def dopocitejMeritko(self, maximalniHodnota):

        if(maximalniHodnota > 0):
            meritkoGrafu = self.maximalniDovolenaHodnota/maximalniHodnota
        else:
            meritkoGrafu = 0

        meritkoGrafu = round(meritkoGrafu*100)/100

        return(meritkoGrafu)

