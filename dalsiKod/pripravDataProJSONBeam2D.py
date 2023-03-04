
import dopocitejMeritkoGraf

class dataProJSON:

    def __init__(self,  souradnicePrutu, LocalDisplacements, LocalForces, globalDisplacements, Strains, Stresses, MeritkoKCE, NodalDisplacements, siloveZatizeniNaPrutech, zatizeniTeplotouHorniVlakna, zatizeniTeplotouDolniVlakna, cislaUzluZacatekAKonecKonecElementu):

        self.MeritkoKCE = MeritkoKCE
        self.MeritkaGrafy = []

        self.souradnicePrutu = souradnicePrutu
        self.LocalDisplacements = LocalDisplacements
        self.LocalForces = LocalForces
        self.NodalDisplacements = NodalDisplacements
        self.globalDisplacements = globalDisplacements

        self.siloveZatizeniNaPrutech = siloveZatizeniNaPrutech
        self.zatizeniTeplotouHorniVlakna = zatizeniTeplotouHorniVlakna
        self.zatizeniTeplotouDolniVlakna = zatizeniTeplotouDolniVlakna

        self.cislaUzluZacatekAKonecKonecElementu = cislaUzluZacatekAKonecKonecElementu
        self.MeritkaGrafyOutputs = self.ziskejMeritkaGrafyOutputs(self.LocalDisplacements, self.LocalForces, self.globalDisplacements)
        self.MeritkaGrafyInputs = self.ziskejMeritkaGrafyInputs(self.siloveZatizeniNaPrutech, self.zatizeniTeplotouHorniVlakna, self.zatizeniTeplotouDolniVlakna)
        self.DOFs = self.ziskejPoleVsechDOF(self.NodalDisplacements)
        #self.DOFs = []

        #pro Strains a Stresses zatim vystupy nejsou

        # radkyKCE maji jen jedny data, tvar KCE je vzdy stejny
        self.radkyKCE = self.ziskejPoleRadkuKCE()

        # radkyGraf maji vnorena data v nasledujici strukture
        #    - LocalDisplacement
        #         - w
        #             - output for time 001
        #             - output for time 002
        #             - output for time 003
        #         - u
        #             - output for time 001
        #             - output for time 002
        #             - output for time 003
        #         - fi
        #             - output for time 001
        #             - output for time 002
        #             - output for time 003
        #    - LocalForces
        #         - V
        #             - output for time 001
        #             - output for time 002
        #             - output for time 003
        #         - N
        #             - output for time 001
        #             - output for time 002
        #             - output for time 003
        #         - M
        #             - output for time 001
        #             - output for time 002
        #             - output for time 003

        self.radkyGrafOutput = self.ziskejDataProLocalDisplacementAForces()
        self.radkyGrafInput = self.ziskejDataProMemberLoadTemperatureLoad()

        print("")


    # getry
    def getRadkyKCE(self):
        return(self.radkyKCE)

    def getRadkyGrafOutput(self):
        return (self.radkyGrafOutput)

    def getRadkyGrafInput(self):
        return (self.radkyGrafInput)

    def getMeritkaGrafyOutputs(self):
        return(self.MeritkaGrafyOutputs)

    def getMeritkaGrafyInputs(self):
        return(self.MeritkaGrafyInputs)

    def getDofs(self):
        return(self.DOFs)



    # ziska pole vsech DOF, tak, aby je mohl zapsat jako nazvy slozek

    def ziskejPoleVsechDOF(self, nodalDisplacements):

        # zatim uvazuje dof pouze z 1. radku
        nodalDisplacementPrvniRadek = nodalDisplacements[0]
        nodalDisplacementPrvniRadek = nodalDisplacementPrvniRadek[0]
        DOFS = nodalDisplacementPrvniRadek[1]

        return (DOFS)


    def ziskejMeritkaGrafyOutputs(self, LocalDisplacements, LocalForces, GlobalDisplacements):

        # dopocita meritko grafu v jine tride
        MeritkaGrafyLocalDisplacements = dopocitejMeritkoGraf.meritkoGraf(LocalDisplacements, True)
        MeritkaGrafyLocalForces = dopocitejMeritkoGraf.meritkoGraf(LocalForces, True)
        MeritkaGrafyGlobalDisplacements = dopocitejMeritkoGraf.meritkoGraf(GlobalDisplacements, True)

        MeritkaLocalDisplacements = MeritkaGrafyLocalDisplacements.getMeritkaGrafy()
        MeritkaLocalForces = MeritkaGrafyLocalForces.getMeritkaGrafy()
        MeritkaGlobalDisplacements = MeritkaGrafyGlobalDisplacements.getMeritkaGrafy()

        meritkaGrafy = []
        meritkaGrafy.append(MeritkaLocalDisplacements)
        meritkaGrafy.append(MeritkaLocalForces)
        meritkaGrafy.append(MeritkaGlobalDisplacements)

        return(meritkaGrafy)



    def ziskejMeritkaGrafyInputs(self, ElementLoads, TemperatureHorni, TemperatureDolni):

        # dopocita meritko grafu v jine tride
        MeritkaGrafyElementLoads = dopocitejMeritkoGraf.meritkoGraf(ElementLoads, False)
        MeritkaGrafyTemperatureHorni = dopocitejMeritkoGraf.meritkoGraf(TemperatureHorni, False)
        MeritkaGrafyTemperatureDolni = dopocitejMeritkoGraf.meritkoGraf(TemperatureDolni, False)

        MeritkaElementLoads = MeritkaGrafyElementLoads.getMeritkaGrafy()
        MeritkaTemperatureHorni = MeritkaGrafyTemperatureHorni.getMeritkaGrafy()
        MeritkaTemperatureDolni = MeritkaGrafyTemperatureDolni.getMeritkaGrafy()

        meritkaGrafy = []
        meritkaGrafy.append(MeritkaElementLoads)
        meritkaGrafy.append(MeritkaTemperatureHorni)
        meritkaGrafy.append(MeritkaTemperatureDolni)

        return (meritkaGrafy)


    #ziska pole radku , kde klic je "kce"
    def ziskejPoleRadkuKCE(self):

        radkyKCE = []

        for BE in range(0, len(self.souradnicePrutu)):
            souradnice = self.ziskejDataProVykresleniPrutuSouradnice(BE, self.souradnicePrutu)

            souradniceZacatkuPrutu = souradnice[0]
            souradniceKonecPrutu = souradnice[1]
            Ax = souradniceZacatkuPrutu[0]
            Ay = souradniceZacatkuPrutu[1]
            By = souradniceKonecPrutu[1]
            Bx = souradniceKonecPrutu[0]

            # cisla uzlu zacatku a koncu elementu
            cislaUzlu = self.cislaUzluZacatekAKonecKonecElementu[BE]
            cisloUzluStart = int(cislaUzlu[0])
            cisloUzluEnd = int(cislaUzlu[1])

            radekKce = self.vratRadekKCE(Ax, Ay, Bx, By, self.MeritkoKCE, cisloUzluStart, cisloUzluEnd)

            radkyKCE.append(radekKce)

        return(radkyKCE)


    # zatim ziskava pouze local displacement a local forces (strains a stresses zatim neni)
    def ziskejDataProLocalDisplacementAForces(self):

        grafOutput = []
        LocalDisplacementOutput = self.ziskejOutputProVsechnySmeryAOFT(self.LocalDisplacements)
        LocalForcesOutput = self.ziskejOutputProVsechnySmeryAOFT(self.LocalForces)
        GlobalDisplacementOutput = self.ziskejOutputProVsechnySmeryAOFT(self.globalDisplacements)

        grafOutput.append(LocalDisplacementOutput)
        grafOutput.append(LocalForcesOutput)
        grafOutput.append(GlobalDisplacementOutput)

        return(grafOutput)


    def ziskejDataProMemberLoadTemperatureLoad(self):

        # aby dokazal pouzit stavajicich funkci ziskejOutputProVsechnySmeryAOFT
        # je potreba, aby data pro vstupy byla jeste 1x vnorena
        # jelikoz vystupy jsou jeste cleneny do casovych kroku OFT, zatimco zatizeni casove kroky nemaji

        siloveZatizeniPruty = []
        teplotaNahorePruty = []
        teplotaDolePruty = []

        siloveZatizeniPruty.append(self.siloveZatizeniNaPrutech)
        teplotaNahorePruty.append(self.zatizeniTeplotouHorniVlakna)
        teplotaDolePruty.append(self.zatizeniTeplotouDolniVlakna)

        grafInput = []
        siloveZatizeniPrutyInput = self.ziskejOutputProVsechnySmeryAOFT(siloveZatizeniPruty)
        teplotaNahorePrutyInput = self.ziskejOutputProVsechnySmeryAOFT(teplotaNahorePruty)
        teplotaDolePrutyInput = self.ziskejOutputProVsechnySmeryAOFT(teplotaDolePruty)

        grafInput.append(siloveZatizeniPrutyInput)
        grafInput.append(teplotaNahorePrutyInput)
        grafInput.append(teplotaDolePrutyInput)

        return(grafInput)


    # ziska system poli, kde klic je "graf"
    def ziskejOutputProVsechnySmeryAOFT(self, velicinaDataPoleIput):

        velicinaVsechnySmeryOutput = []

        # index rozlisuje smery, ktere veliciny se budou vykreslovat
        for index in range(1, 4):
            # index = 1 : u (N)
            # index = 2 : w (V)
            # index = 3 : fi (M)

            velicinaOFToutput = []

            #ziska data pro jednotlivy output for time
            for OFT in range(0, len(velicinaDataPoleIput)):
                velicinaData = velicinaDataPoleIput[OFT]

                # ziska data pro vsechny output for time
                velicinaOFT = self.vratPoleRadkuGraf(velicinaData, index)
                velicinaOFToutput.append(velicinaOFT)

            velicinaVsechnySmeryOutput.append(velicinaOFToutput)

        return(velicinaVsechnySmeryOutput)


    # vrati pole radku , kde klic je "graf"
    def vratPoleRadkuGraf(self, velicina, index):

        radkyGraf = []

        for BE in range(0, len(velicina)):

            deformace = self.ziskejDataProVykresleniPrutuDeformace(BE, velicina, index)
            deformaceZacatekPrutu = deformace[0]
            deformaceKonecPrutu = deformace[1]
            nasobkyMocnin = self.vratMasobkyMocnin(deformaceZacatekPrutu, deformaceKonecPrutu)
            radekGraf = self.vratRadekGraf(nasobkyMocnin)

            radkyGraf.append(radekGraf)

        return(radkyGraf)


    # ziska dvojici hodnot na zacatku a konci prutu
    # dvojici koncovych souradnic
    # dvojici koncovych deformaci nebo vnitrnich sil
    # je treba zadat cislo "output for time" (=OFT) a cislo prutu (=BE),
    #            dale pak pole deformaci nebo vnitrnich sil
    # index poukazuje na poradi jake deformace se maji vyhledavat (1=u, 2=w, 3=fi)

    def ziskejDataProVykresleniPrutuDeformace(self, BE, deformace, index):
        deformacePrut = deformace[BE]
        indexZacatekPrutu = index-1
        indexKonecPrutu = indexZacatekPrutu + 3

        deformaceZacatekPrutu = deformacePrut[indexZacatekPrutu]
        deformaceKonecPrutu = deformacePrut[indexKonecPrutu]

        deformace = []
        deformace.append(deformaceZacatekPrutu)
        deformace.append(deformaceKonecPrutu)

        return(deformace)


    def ziskejDataProVykresleniPrutuSouradnice(self, BE, souradnice):

        souradnicePrutu = souradnice[BE]
        return(souradnicePrutu)


    def vratRadekKCE(self, Ax, Ay, Bx, By, meritko, cisloUzluStart, cisloUzluEnd):

        #Ax = 100
        #Ay = 0
        #Bx = 300
        #By = 10

        Ax = Ax*meritko
        Ay = Ay*meritko
        Bx = Bx*meritko
        By = By*meritko

        graf = True
        vykreslitPrut = True
        barvaCary = "darkBlue"
        tloustkaCary = 3

        grafStr = self.prevedTrueFalseNaJavascript(graf)
        vykreslitPrutStr = self.prevedTrueFalseNaJavascript(vykreslitPrut)
        radekKCE = '\'           "kce": {"Ax":' + str(Ax) + ',"Ay":' + str(Ay) + ',"Bx":' + str(Bx) + ',"By":' + str(By) + ',"graf":' + grafStr + ',"vykreslitPrut":' + vykreslitPrutStr + ',"barvaCary":"' + barvaCary + '", "tloustkaCary":"' + str(tloustkaCary) + '", "uzelStart":"' + str(cisloUzluStart) + '", "uzelEnd":"' + str(cisloUzluEnd) + '"},\''

        return(radekKCE)


    def vratRadekGraf(self, nasobkyMocnin):

        delkaKrokuPriblizne = 10
        #nasobkyMocnin = [[0, 1], [0, -100]]
        vykreslitGraf = True
        vykreslitSrafu = True
        barvaCarySrafy = "#000000"
        tloustkaCarySrafa = 0.5
        barvaCaryGraf = "#000000"
        tloustkaCaryGraf = 1

        vykreslitGrafStr = self.prevedTrueFalseNaJavascript(vykreslitGraf)
        vykreslitSrafuStr = self.prevedTrueFalseNaJavascript(vykreslitSrafu)

        radekGraf = '\'           "graf": {"delkaKrokuPriblizne":' + str(delkaKrokuPriblizne) + ',"nasobkyMocnin":' + str(nasobkyMocnin) + ',"vykreslitGraf":' + vykreslitGrafStr + ',"vykreslitSrafu":' + vykreslitSrafuStr + ',"barvaCarySrafy":"' + barvaCarySrafy + '","tloustkaCarySrafa":"' + str(tloustkaCarySrafa) + '","barvaCaryGraf":"' + barvaCaryGraf + '","tloustkaCaryGraf":"' + str(tloustkaCaryGraf) + '"}\''

        return(radekGraf)


    # vrati nasobky mocnin pro linearni rozlozeni grafu
    def vratMasobkyMocnin(self, hodnotaVlevo, hodnotaVpravo):

        osaX = []
        osaY = []
        nasobkyMocnin = []

        hodnotaVlevo = float(hodnotaVlevo)
        hodnotaVpravo = float(hodnotaVpravo)

        osaX.append(0)
        osaX.append(1)
        osaY.append(hodnotaVlevo)
        osaY.append(hodnotaVpravo)

        nasobkyMocnin.append(osaX)
        nasobkyMocnin.append(osaY)


        return(nasobkyMocnin)



    # upravi True/False do podoby aby bylo citelne javascriptem, tj, zmeni pocatecni pismeno na t/f
    def prevedTrueFalseNaJavascript(self, boolean):

        if(boolean) == True:
            booleanStr = "true"
        else :
            booleanStr = "false"

        return(booleanStr)




