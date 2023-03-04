

class vytvorSekceReactions:

    def __init__(self, reactionsRadky, poleDof):

        self.reactionsRadky = reactionsRadky
        self.poleDOF = poleDof

        self.potrebnaData = self.rozdelPotrebnaData(self.reactionsRadky)
        self.seskupenaDatareakce = self.seskupDataCiselUzlu(self.potrebnaData)

        self.dataReakce = self.formatujDataDoUzelDofHodnotyVsechnyDof(self.seskupenaDatareakce, self.poleDOF)



    def getDataReakce(self):
        return(self.dataReakce)



    def formatujDataDoUzelDofHodnotyVsechnyDof(self, seskupenaDatareakce, poleDof):

        seskupenaDataReakceNew = []

        for OFT in range(0, len(seskupenaDatareakce)):
            seskupenaDatareakceOFT = seskupenaDatareakce[OFT]
            seskupenaDatareakceOFTNew = self.formatujDataDoUzelDofHodnoty(seskupenaDatareakceOFT, poleDof)

            seskupenaDataReakceNew.append(seskupenaDatareakceOFTNew)

        return(seskupenaDataReakceNew)


    # formatuje data do formatu "cislo uzlu"-"dof"-"hodnoty"
    def formatujDataDoUzelDofHodnoty(self, seskupenaDatareakce, poleDof):

        seskupenaDatareakceNew = []

        for iRadek in range(0, len(seskupenaDatareakce)):
            radek = seskupenaDatareakce[iRadek]
            cisloUzlu = radek[0]
            dofStavajici = radek[1]
            hodnotyPole = radek[2]

            hodnotyPoleNew = self.doplnNuloveHodnotyProChybejiciDof(dofStavajici, poleDof, hodnotyPole)

            radekNew = []
            radekNew.append(cisloUzlu)
            radekNew.append(poleDof)
            radekNew.append(hodnotyPoleNew)

            seskupenaDatareakceNew.append(radekNew)

        return(seskupenaDatareakceNew)


    def doplnNuloveHodnotyProChybejiciDof(self, dofStavajici, poleDof, hodnotyPole):

        hodnotyPoleNew = []

        for iDof in range(0, len(poleDof)):
            dof = poleDof[iDof]
            indexPole = self.vratIndexPole(dofStavajici, dof)

            if(indexPole == -1):
                hodnota = 0
            else:
                hodnota = hodnotyPole[indexPole]

            hodnotyPoleNew.append(hodnota)

        return(hodnotyPoleNew)




    def vratIndexPole(self, pole, hodnota):

        try:
            pole.index(hodnota)
        except ValueError:
            indexVPoli = -1
        else:
            indexVPoli = pole.index(hodnota)

        return(indexVPoli)


    def detekujZdaDofJeChybejici(self, poleDof, dofExp):

        dofNalezeno = False

        if dofExp not in poleDof:
            dofNalezeno = True

        return(dofNalezeno)





    def seskupDataCiselUzlu(self, potrebnaData):

        seskupenaDataVsechnyOFT = []

        for OFT in range(0, len(potrebnaData)):
            dataOFT = potrebnaData[OFT]
            dataSeskupenaOFT = self.seskupDataCiselUzluProJedenOFT(dataOFT)

            seskupenaDataVsechnyOFT.append(dataSeskupenaOFT)

        return(seskupenaDataVsechnyOFT)


    def seskupDataCiselUzluProJedenOFT(self, dataJedenOFT):

        dataSeskupenaOFT = []

        for iRadek in range(0, len(dataJedenOFT)):
            radek = dataJedenOFT[iRadek]
            cisloUzlu = radek[0]
            indexyPribuznychRadkuPodleCislaUzlu = self.vratCislaIndexuPolePodleCislaUzlu(dataJedenOFT, cisloUzlu)

            iDofData = self.vratPoleJakoSloupecPodleIndexuRadku(dataJedenOFT, indexyPribuznychRadkuPodleCislaUzlu, 1)
            reactionsData = self.vratPoleJakoSloupecPodleIndexuRadku(dataJedenOFT, indexyPribuznychRadkuPodleCislaUzlu, 2)
            bcIdData = self.vratPoleJakoSloupecPodleIndexuRadku(dataJedenOFT, indexyPribuznychRadkuPodleCislaUzlu, 3)

            radekKompaktni = []
            radekKompaktni.append(cisloUzlu)
            radekKompaktni.append(iDofData)
            radekKompaktni.append(reactionsData)
            radekKompaktni.append(bcIdData)

            if radekKompaktni not in dataSeskupenaOFT:
                dataSeskupenaOFT.append(radekKompaktni)

        return(dataSeskupenaOFT)


    # vrati pole hodnot z jednotlivych radku, kde radky jsou v "indexyRadku", a "cisloSloupce"
    def vratPoleJakoSloupecPodleIndexuRadku(self, pole, indexyRadku, cisloSloupce):

        poleHodnotVDanemSloupci = []

        for iRadek in range(0, len(pole)):
            if iRadek in indexyRadku:
                radek = pole[iRadek]
                hodnota = radek[cisloSloupce]

                poleHodnotVDanemSloupci.append(hodnota)

        return(poleHodnotVDanemSloupci)




    # rozdeli data do pole
    def rozdelPotrebnaData(self, reactionsRadky):

        potrebnaData = []

        for OFT in range(0, len(reactionsRadky)):
            potrebnaDataOFT = []
            radkyOFT = reactionsRadky[OFT]

            cislaUzluNaRadcich = []
            iDofNaRadcich = []
            reactionNaRadcich = []
            bcIdNaRadcich = []

            # asi jsou data vlozena jedenkrat navic
            radkyOFT0 = radkyOFT[0]

            for iRadek in range(0, len(radkyOFT0)):
                radek = radkyOFT0[iRadek]

                jednaSeOPotrebnyRadek = self.detekujZdaSeJednaOPotrebnyRadek(radek, 'Node')

                if(jednaSeOPotrebnyRadek == True):
                    cisloUzlu = self.vratHodnotuZRadku(radek, "Node")
                    iDof = self.vratHodnotuZRadku(radek, "iDof")
                    reaction = self.vratHodnotuZRadku(radek, "reaction")
                    bcId = self.vratHodnotuZRadku(radek, "bc-id")

                    potrebnaDataRadek = []
                    potrebnaDataRadek.append(cisloUzlu)
                    potrebnaDataRadek.append(iDof)
                    potrebnaDataRadek.append(reaction)
                    potrebnaDataRadek.append(bcId)

                    potrebnaDataOFT.append(potrebnaDataRadek)

            potrebnaData.append(potrebnaDataOFT)

        return(potrebnaData)


    def usporadejReakceDoPole(self, reactionsRadky):

        for OFT in range(0, len(reactionsRadky)):
            reactionsOFT = reactionsRadky[OFT]



        print("")


    def ziskejRadekProUzel(self, reactionsOFT):

        print("")


    def vratHodnotuZRadku(self, radekReakce, pozadovanaVelicina):

        if(pozadovanaVelicina == "Node"):
            indIDOFPred = radekReakce.index("Node") + 4
            indIDOFZa = radekReakce.index("iDof")

        if(pozadovanaVelicina == "iDof"):
            indIDOFPred = radekReakce.index("iDof") + 4
            indIDOFZa = radekReakce.index("reaction")

        if (pozadovanaVelicina == "reaction"):
            indIDOFPred = radekReakce.index("reaction") + 8
            indIDOFZa = radekReakce.index("[")

        if (pozadovanaVelicina == "bc-id"):
            indIDOFPred = radekReakce.index("bc-id:") + 6
            indIDOFZa = radekReakce.index("]")


        velicinaStr = radekReakce[indIDOFPred: indIDOFZa: 1]
        velicinaStr = velicinaStr.strip()
        velicinaFloat = float(velicinaStr)

        return(velicinaFloat)


    # vrati indexy tech radku, kde se nachazi cislo uzlu, tj. polozka v 1. sloupci
    def vratCislaIndexuPolePodleCislaUzlu(self, potrebnaDataOFT, cisloUzluExp):

        indexyRadkuPole = []

        for iRadek in range(0, len(potrebnaDataOFT)):
            radek = potrebnaDataOFT[iRadek]
            cisloUzlu = radek[0]

            if(cisloUzlu == cisloUzluExp):
                indexyRadkuPole.append(iRadek)

        return(indexyRadkuPole)


    # vrati true, pokud se jedna o potrebny radek
    def detekujZdaSeJednaOPotrebnyRadek(self, radek, polozka):

        try:
            radek.index(polozka)
        except ValueError:
            jednaSeOPotrebnyRadek = False
        else:
            jednaSeOPotrebnyRadek = True


        return(jednaSeOPotrebnyRadek)