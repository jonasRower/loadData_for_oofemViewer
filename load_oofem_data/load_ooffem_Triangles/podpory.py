# zpracuje data pro vykresleni podpor
class podporyData:

    def __init__(self, boundaryConditionPole, setyDataPole, uzlyAJejichSouradnice):

        self.boundaryConditionPole = boundaryConditionPole
        self.setyDataPole = setyDataPole
        self.uzlyAJejichSouradnice = uzlyAJejichSouradnice

        # souradnice jsou rozdeleny do poli, kazde pole je prirazeno jine podpore
        self.podporyKloubovePosuvneVodorovne = []
        self.podporyKloubovePosuvneSvisle = []
        self.podporyVetknute = []

        self.dofsPole = self.vratSloupecZPole(self.boundaryConditionPole, 2)
        self.cislaSetuPole = self.vratSloupecZPole(self.boundaryConditionPole, 4)

        self.cislaUzluProJednotliveBC = self.vratCislaUzluProJednotliveBC(self.cislaSetuPole)
        self.souradniceProJednotliveBC = self.vratSouradniceUzluProJednotliveBC(self.cislaUzluProJednotliveBC,
                                                                                self.uzlyAJejichSouradnice)

        # roztridi souradnice do poli podle jednotlivych podpor
        self.roztridDataPodlePodpor(self.dofsPole, self.souradniceProJednotliveBC)

    def getPodporyKloubovePosuvneVodorovne(self):
        return (self.podporyKloubovePosuvneVodorovne)

    def getPodporyKloubovePosuvneSvisle(self):
        return (self.podporyKloubovePosuvneSvisle)

    def getPodporyVetknute(self):
        return (self.podporyVetknute)

    def roztridDataPodlePodpor(self, dofsPole, souradniceProJednotliveBC):

        for i in range(0, len(dofsPole)):
            dofs = dofsPole[i]
            souradnice = souradniceProJednotliveBC[i]
            if (dofs == ['3']):
                self.podporyKloubovePosuvneVodorovne.append(souradnice)
            if (dofs == ['1']):
                self.podporyKloubovePosuvneSvisle.append(souradnice)
            if (dofs == ['1', '3', '5']):
                self.podporyVetknute.append(souradnice)

    def vratSouradniceUzluProJednotliveBC(self, cislaUzluProJednotliveBC, uzlyAJejichSouradnice):

        souradniceUzluProVsechnyBC = []

        for i in range(0, len(cislaUzluProJednotliveBC)):
            cislaUzlu = cislaUzluProJednotliveBC[i]

            souradniceUzluProDanouBC = []

            for iUzel in range(0, len(cislaUzlu)):
                cisloUzlu = cislaUzlu[iUzel]
                souradniceUzlu = self.vratSouradniceUzluPodleJehoCisla(uzlyAJejichSouradnice, cisloUzlu)

                souradniceUzluProDanouBC.append(souradniceUzlu)

            souradniceUzluProVsechnyBC.append(souradniceUzluProDanouBC)

        return (souradniceUzluProVsechnyBC)

    def vratSouradniceUzluPodleJehoCisla(self, uzlyAJejichSouradnice, cisloUzluExp):

        for i in range(0, len(uzlyAJejichSouradnice)):
            uzel = uzlyAJejichSouradnice[i]
            cisloUzlu = uzel[0]
            if (int(cisloUzlu) == int(cisloUzluExp)):
                souradniceUzlu = []
                X = uzel[1]
                Y = uzel[2]

                souradniceUzlu.append(X)
                souradniceUzlu.append(Y)

                break

        return (souradniceUzlu)

    def vratCislaUzluProJednotliveBC(self, cislaSetuPole):

        cislaUzluProJednotliveBC = []

        for set in range(0, len(cislaSetuPole)):
            cisloSetu = cislaSetuPole[set]
            setCislo = cisloSetu[0]

            cislaUzlu = self.vratCislaUzluZSetu(self.setyDataPole, setCislo)
            cislaUzluProJednotliveBC.append(cislaUzlu)

        return (cislaUzluProJednotliveBC)

    def vratCislaUzluZSetu(self, setyDataPole, cisloSetuExp):

        for i in range(0, len(setyDataPole)):
            setData = setyDataPole[i]
            cisloSetu = setData[0]

            if (int(cisloSetu) == int(cisloSetuExp)):
                cislaUzlu = setData[2]
                break

        return (cislaUzlu)

    def vratSloupecZPole(self, pole, sloupec):

        hodnotyPole = []

        for i in range(0, len(pole)):
            poleRadek = pole[i]
            hodnoty = poleRadek[sloupec]
            hodnotyPole.append(hodnoty)

        return (hodnotyPole)


"""       
    # dofs [1,3,5]
    def dataPodporyVetknute(self):

    # dofs [1,3]
    def dataPodporyKloubovePevne(self):

    # dofs [1]
    def dataPodporyKloubovePosuvneSvisle(self):

    # dofs [3]
    def dataPodporyKloubovePosuvneVodorovne(self):
"""