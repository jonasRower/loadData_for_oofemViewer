#import podpory
#import sily

import tiskniDataDoExceluProTestovani


class data:

    def __init__(self, poleRadku):

        self.poleRadku = poleRadku
        self.polePrvnichSlov = []
        self.poleNode = []

        self.souradniceX = []
        self.souradniceY = []

        self.uzelElementu1 = []
        self.uzelElementu2 = []
        self.cislaUzluZacatekAKonecKonecElementu = []

        self.souradniceVsechPrutu = []
        self.souradniceVsechTrojuhelniku = []
        self.uzlyTrojuhelnika = []
        self.uzlyPrutu = []
        self.cislaUzluSouradnice = []

        ####################################################################
        # Sestavi pole souradnic elementu

        self.vratPolePrvnichSlov()
        self.poleNode = self.vytvorPolePodlePrvnihoSlovaNaRadku("node")
        self.poleBeam2d = self.vytvorPolePodlePrvnihoSlovaNaRadku("Beam2d")
        self.poleTr1supgaxi = self.vytvorPolePodlePrvnihoSlovaNaRadku("tr1supgaxi")
        self.poleSetu = self.vytvorPolePodlePrvnihoSlovaNaRadku("Set")
        self.poleBoundaryCondition = self.vytvorPolePodlePrvnihoSlovaNaRadku("BoundaryCondition")
        self.poleConstantEdgeLoad = self.vytvorPolePodlePrvnihoSlovaNaRadku("ConstantEdgeLoad")
        self.poleNodalLoad = self.vytvorPolePodlePrvnihoSlovaNaRadku("NodalLoad")
        self.poleStructTemperatureLoad = self.vytvorPolePodlePrvnihoSlovaNaRadku("StructTemperatureLoad")
        self.polePeakFunction = self.vytvorPolePodlePrvnihoSlovaNaRadku("PeakFunction")

        self.cislaLoadTimeFunction = self.vratPoleJednohoSLoupce(self.poleBoundaryCondition, 3)
        self.cislaUzlu = self.vratPoleJednohoSLoupce(self.poleNode, 1)


        # rozlisuje zda nacitaBeam2D nebo tr1supgaxi
        if(len(self.poleTr1supgaxi) == 0):  #nacita beam2D
            self.souradniceX = self.vratPoleJednohoSLoupce(self.poleNode, 4)
            self.souradniceY = self.vratPoleJednohoSLoupce(self.poleNode, 6)
            self.souradniceZ = self.vratPoleJednohoSLoupce(self.poleNode, 5)

            self.uzelElementu1 = self.vratPoleJednohoSLoupce(self.poleBeam2d, 4)
            self.uzelElementu2 = self.vratPoleJednohoSLoupce(self.poleBeam2d, 5)
            self.cislaUzluZacatekAKonecKonecElementu = self.kElementumZapisCislaUzluZacatkuAKonce(self.uzelElementu1, self.uzelElementu2)
            self.sestavSouradnicePrutu()

        else:                               # nacita tr1supgaxi
            self.souradniceX = self.vratPoleJednohoSLoupce(self.poleNode, 4)
            self.souradniceY = self.vratPoleJednohoSLoupce(self.poleNode, 5)
            self.souradniceZ = self.vratPoleJednohoSLoupce(self.poleNode, 6)

            self.uzelElementu1 = self.vratPoleJednohoSLoupce(self.poleTr1supgaxi, 4)
            self.uzelElementu2 = self.vratPoleJednohoSLoupce(self.poleTr1supgaxi, 5)
            self.uzelElementu3 = self.vratPoleJednohoSLoupce(self.poleTr1supgaxi, 6)

            self.sestavSouradniceTrojuhelnika()


        ##### roztridi data do poli podle 1. slova na radku
        self.setyDataPole = self.roztridSety(self.poleSetu)
        self.boundaryConditionsDataPole = self.roztridBoundaryCondition(self.poleBoundaryCondition)
        self.ConstantEdgeLoadDataPole = self.roztridConstantEdgeLoad(self.poleConstantEdgeLoad)
        self.NodalLoadDataPole = self.roztridNodalLoad(self.poleNodalLoad)
        self.StructTemperatureLoadPole = self.roztridStructTemperatureLoad(self.poleStructTemperatureLoad)
        self.peakFunctionDataPole = self.roztridPeakFunction(self.polePeakFunction)

        ##### pripravi data pro vykresleni konstrukce
        self.sestavSouradniceUzlu()

        # tiskne data do Excelu, tak aby se data dali testovat
        self.dataDoExcelu = []
        self.dataDoExcelu.append(self.poleBeam2d)
        self.dataDoExcelu.append(self.poleTr1supgaxi)
        self.dataDoExcelu.append(self.poleSetu)
        self.dataDoExcelu.append(self.poleBoundaryCondition)
        self.dataDoExcelu.append(self.poleConstantEdgeLoad)
        self.dataDoExcelu.append(self.poleNodalLoad)
        self.dataDoExcelu.append(self.poleStructTemperatureLoad)
        self.dataDoExcelu.append(self.polePeakFunction)

        tiskDoExceluProTestovani = tiskniDataDoExceluProTestovani.dataDoExceluProTestovani(self.dataDoExcelu)


    # vrati data
    def getSouradniceVsechPrutu(self):
        return(self.souradniceVsechPrutu)

    def getUzlyPrutu(self):
        return(self.uzlyPrutu)

    def getUzlyASouradnice(self):
        return(self.cislaUzluSouradnice)

    def getBoundaryCondition(self):
        return(self.boundaryConditionsDataPole)

    def getSetyDataPole(self):
        return(self.setyDataPole)

    def getSouradniceVsechTrojuhelniku(self):
        return(self.souradniceVsechTrojuhelniku)

    def getUzlyTrojuhelnika(self):
        return (self.uzlyTrojuhelnika)

    def getCislaUzluZacatekAKonecKonecElementu(self):
        return(self.cislaUzluZacatekAKonecKonecElementu)


    # vrati zatizeni
    def getConstantEdgeLoadDataPole(self):
        return(self.ConstantEdgeLoadDataPole)

    def getStructTemperatureLoadPole(self):
        return (self.StructTemperatureLoadPole)

    def getBoundaryConditionsDataPole(self):
        return (self.boundaryConditionsDataPole)

    def getNodalLoadDataPole(self):
        return(self.NodalLoadDataPole)



    #self.setyDataPole
    """
    def getZatizeniNaPrutechPodleDof(self):
        return(self.zatizeniNaPrutechPodleDof)

    def getZatizeniTeplotouHorniDolniVlakna(self):
        return(self.zatizeniTeplotouHorniDolniVlakna)

    def getPodporyBoundaryConditionsPodleDof(self):
        return(self.podporyBoundaryConditionsPodleDof)

    def getZatizeniNaUzlechPodleDof(self):
        return(self.zatizeniNaUzlechPodleDof)
    """

    # na kazdy index poleSetu vlozi pole:
    # 1) cislo indexu setu
    # 2) klicoveSlovo
    # 3) pole s uzly
    # 4) pole s elementy
    def roztridSety(self, poleSetu):

        cislaSetu = self.vratPoleJednohoSLoupce(poleSetu, 1)
        setyDataPole = []

        for r in range(0, len(poleSetu)):
            setRadek = poleSetu[r]

            cisloSetu = cislaSetu[r]
            klicoveSlovo = self.vratKlicoveSlovoSet(setRadek)

            hodnotyZaKlicovymSlovem = self.vratPoleHodnotZaKlicovymSlovem(setRadek, klicoveSlovo)
            radekSetPole = self.vratRadekProZapisSetu(cisloSetu, klicoveSlovo, hodnotyZaKlicovymSlovem)

            setyDataPole.append(radekSetPole)

        return(setyDataPole)

    # na kazdy index poleBoundaryCondition vlozi pole:
    # 1) cislo indexu boundary condition
    # 2) cislo indexu loadTimeFunction
    # 3) pole s dofs
    # 4) pole s values
    # 5) pole s set (asi pouze jedna hodnota -vzdy)
    def roztridBoundaryCondition(self, poleBoundaryCondition):

        cislaBoundaryCondition = self.vratPoleJednohoSLoupce(poleBoundaryCondition, 1)
        boundaryConditionsDataPole = []

        for r in range(0, len(poleBoundaryCondition)):
            boundaryConditionsData = []

            BCradek = poleBoundaryCondition[r]
            BCcislo = cislaBoundaryCondition[r]
            LoadTimeFunctionCislo = self.cislaLoadTimeFunction[r]
            dofsPoleHodnot = self.vratPoleHodnotZaKlicovymSlovem(BCradek, "dofs")
            valuesPoleHodnot = self.vratPoleHodnotZaKlicovymSlovem(BCradek, "values")
            setPoleHodnot = self.vratPoleHodnotZaKlicovymSlovem(BCradek, "set")

            boundaryConditionsData.append(BCcislo)
            boundaryConditionsData.append(LoadTimeFunctionCislo)
            boundaryConditionsData.append(dofsPoleHodnot)
            boundaryConditionsData.append(valuesPoleHodnot)
            boundaryConditionsData.append(setPoleHodnot)

            boundaryConditionsDataPole.append(boundaryConditionsData)

        return(boundaryConditionsDataPole)


    # na kazdy index ConstantEdgeLoadDataPole vlozi pole:
    # 1) cislo indexu ConstantEdgeLoad condition
    # 2) cislo indexu loadTimeFunction
    # 3) pole s Components
    # 4) pole s loadType
    # 5) pole s set (asi pouze jedna hodnota -vzdy)
    def roztridConstantEdgeLoad(self, poleConstantEdgeLoad):

        cislaConstantEdgeLoad = self.vratPoleJednohoSLoupce(poleConstantEdgeLoad, 1)
        ConstantEdgeLoadDataPole = []

        for r in range(0, len(poleConstantEdgeLoad)):
            ConstantEdgeLoadData = []

            ConstantEdgeLoadradek = poleConstantEdgeLoad[r]
            ConstantEdgeLoadCislo = cislaConstantEdgeLoad[r]
            LoadTimeFunctionCislo = self.cislaLoadTimeFunction[r]
            ComponentsPoleHodnot = self.vratPoleHodnotZaKlicovymSlovem(ConstantEdgeLoadradek, "Components")
            LoadTypePoleHodnot = self.vratPoleHodnotZaKlicovymSlovem(ConstantEdgeLoadradek, "loadType")
            setPoleHodnot = self.vratPoleHodnotZaKlicovymSlovem(ConstantEdgeLoadradek, "set")

            ConstantEdgeLoadData.append(ConstantEdgeLoadCislo)
            ConstantEdgeLoadData.append(LoadTimeFunctionCislo)
            ConstantEdgeLoadData.append(ComponentsPoleHodnot)
            ConstantEdgeLoadData.append(LoadTypePoleHodnot)
            ConstantEdgeLoadData.append(setPoleHodnot)

            ConstantEdgeLoadDataPole.append(ConstantEdgeLoadData)

        return(ConstantEdgeLoadDataPole)


    # na kazdy index poleNodalLoadDataPole vlozi pole:
    # 1) cislo indexu NodalLoad condition
    # 2) cislo indexu loadTimeFunction
    # 3) pole s dofs
    # 4) pole s Components
    # 5) pole s set (asi pouze jedna hodnota -vzdy)
    def roztridNodalLoad(self, poleNodalLoad):

        cislaPoleNodalLoad = self.vratPoleJednohoSLoupce(poleNodalLoad, 1)
        poleNodalLoadDataPole = []

        for r in range(0, len(poleNodalLoad)):
            poleNodalLoadData = []

            NodalLoadRadek = poleNodalLoad[r]
            NodalLoadCislo = cislaPoleNodalLoad[r]
            LoadTimeFunctionCislo = self.cislaLoadTimeFunction[r]
            dofsPoleHodnot = self.vratPoleHodnotZaKlicovymSlovem(NodalLoadRadek, "dofs")
            ComponentsPoleHodnot = self.vratPoleHodnotZaKlicovymSlovem(NodalLoadRadek, "Components")
            setPoleHodnot = self.vratPoleHodnotZaKlicovymSlovem(NodalLoadRadek, "set")

            poleNodalLoadData.append(NodalLoadCislo)
            poleNodalLoadData.append(LoadTimeFunctionCislo)
            poleNodalLoadData.append(dofsPoleHodnot)
            poleNodalLoadData.append(ComponentsPoleHodnot)
            poleNodalLoadData.append(setPoleHodnot)

            poleNodalLoadDataPole.append(poleNodalLoadData)

        return(poleNodalLoadDataPole)

    # na kazdy index poleStructTemperatureLoad vlozi pole:
    # 1) cislo indexu StructTemperatureLoad condition
    # 2) cislo indexu loadTimeFunction
    # 3) pole s Components
    # 4) pole s set (asi pouze jedna hodnota -vzdy)
    def roztridStructTemperatureLoad(self, poleStructTemperatureLoad):

        cislaPoleStructTemperatureLoad = self.vratPoleJednohoSLoupce(poleStructTemperatureLoad, 1)
        structTemperatureLoadDataPole = []

        for r in range(0, len(poleStructTemperatureLoad)):
            poleStructTemperatureLoadData = []

            structTemperatureLoadRadek = poleStructTemperatureLoad[r]
            structTemperatureLoadCislo = cislaPoleStructTemperatureLoad[r]
            LoadTimeFunctionCislo = self.cislaLoadTimeFunction[r]
            ComponentsPoleHodnot = self.vratPoleHodnotZaKlicovymSlovem(structTemperatureLoadRadek, "Components")
            setPoleHodnot = self.vratPoleHodnotZaKlicovymSlovem(structTemperatureLoadRadek, "set")

            poleStructTemperatureLoadData.append(structTemperatureLoadCislo)
            poleStructTemperatureLoadData.append(LoadTimeFunctionCislo)
            poleStructTemperatureLoadData.append(ComponentsPoleHodnot)
            poleStructTemperatureLoadData.append(setPoleHodnot)

            structTemperatureLoadDataPole.append(poleStructTemperatureLoadData)

        return(structTemperatureLoadDataPole)

    # na kazdy index polePeakFunction vlozi pole:
    # 1) cislo indexu polePeakFunction
    # 2) pole s t
    # 3) pole s ft
    def roztridPeakFunction(self, polePeakFunction):

        cislaPolePeakFunction = self.vratPoleJednohoSLoupce(polePeakFunction, 1)
        peakFunctionDataPole = []

        for r in range(0, len(polePeakFunction)):
            polePeakFunctionData = []

            peakFunctionRadek = polePeakFunction[r]
            peakFunctionCislo = cislaPolePeakFunction[r]
            tPoleHodnot = self.vratPoleHodnotZaKlicovymSlovem(peakFunctionRadek, "t")
            ftPoleHodnot = self.vratPoleHodnotZaKlicovymSlovem(peakFunctionRadek, "f(t)")

            polePeakFunctionData.append(peakFunctionCislo)
            polePeakFunctionData.append(tPoleHodnot)
            polePeakFunctionData.append(ftPoleHodnot)

            peakFunctionDataPole.append(polePeakFunctionData)

        return(peakFunctionDataPole)


    #vraci subPole ktere je na radku poleSetu
    def vratRadekProZapisSetu(self, cisloSetu, klicoveSlovo, hodnotyZaKlicovymSlovem):

        radekSetPole = []
        hodnotyNodes = []
        hodnotyElements = []

        if(klicoveSlovo == "nodes"):
            hodnotyNodes = hodnotyZaKlicovymSlovem
        else:
            hodnotyElements = hodnotyZaKlicovymSlovem

        radekSetPole.append(cisloSetu)
        radekSetPole.append(klicoveSlovo)
        radekSetPole.append(hodnotyNodes)
        radekSetPole.append(hodnotyElements)

        return(radekSetPole)


    def vratPoleHodnotZaKlicovymSlovem(self, radek, klicoveSlovo):

        wordArr = radek.split()

        for i in range(0, len(wordArr)):
            bunka = wordArr[i]
            if(bunka == klicoveSlovo):
                indexKlicovehoSlova = i
                break

        # zjisti pocet hodnot (= delka pole) za klicovym slovem
        pocetHodnotZaKlicovymSlovem = wordArr[indexKlicovehoSlova+1]
        pocetHodnotZaKlicovymSlovem = self.odstranNepotrebneZnaky(pocetHodnotZaKlicovymSlovem)
        jePotrebaVratitIntervalHodnot = self.detekujZdaJePotrebaVratitInterval(wordArr, indexKlicovehoSlova)

        if(jePotrebaVratitIntervalHodnot == True):
            prvniAPosledniHodnotaIntervalu = self.vratPrvniAPosledniHodnotuIntervalu(wordArr, indexKlicovehoSlova+1)
            prvniHodnotaIntervalu = prvniAPosledniHodnotaIntervalu[0]
            posledniHodnotaIntervalu = prvniAPosledniHodnotaIntervalu[1]
            hodnotyZaKlicovymSlovem = self.vratIntervalHodnot(prvniHodnotaIntervalu, posledniHodnotaIntervalu)

        else:
            prvniIndex = indexKlicovehoSlova + 2
            posledniIndex = prvniIndex + int(round(float(pocetHodnotZaKlicovymSlovem)))

            hodnotyZaKlicovymSlovem = self.vratHodnotyZaKlicovymSlovem(radek, prvniIndex, posledniIndex)


        return(hodnotyZaKlicovymSlovem)



    # rozlisuje zda radek obsahuje interval zadany takto: "{(1 5)}"
    def detekujZdaJePotrebaVratitInterval(self, wordArr, indexKlicovehoSlova):

        clenZaKlicovymSlovem = wordArr[indexKlicovehoSlova+1]
        clenObsahujeZavorky = self.detekujPritomnostSlova(clenZaKlicovymSlovem, "{(")

        return(clenObsahujeZavorky)


    def vratPrvniAPosledniHodnotuIntervalu(self, wordArr, indexKdeJeDetekovanInterval):

        prvniAPosledniHodnota = []

        prvniHodnota = wordArr[indexKdeJeDetekovanInterval]
        posledniHodnota = wordArr[indexKdeJeDetekovanInterval + 1]

        prvniHodnota = self.odstranNepotrebneZnaky(prvniHodnota)
        posledniHodnota = self.odstranNepotrebneZnaky(posledniHodnota)
        prvniAPosledniHodnota.append(prvniHodnota)
        prvniAPosledniHodnota.append(posledniHodnota)

        return(prvniAPosledniHodnota)

    def odstranNepotrebneZnaky(self, radek):

        radekNew = radek
        radekNew = radekNew.replace("(","")
        radekNew = radekNew.replace("{", "")
        radekNew = radekNew.replace("}", "")
        radekNew = radekNew.replace(")", "")

        return(radekNew)


    # vraci interval v pripade, ze hodnoty jsou definovany napr. takto: {(1 5)}
    def vratIntervalHodnot(self, prvniHodnota, posledniHodnota):

        intervalHodnotPole = []
        for i in range(int(prvniHodnota), int(posledniHodnota)+1):  #uvazuje se posledniHodnota-vcetne
            intervalHodnotPole.append(i)

        return (intervalHodnotPole)


    def vratHodnotyZaKlicovymSlovem(self, radek, prvniIndex, posledniIndex):

        wordArr = radek.split()
        poleHodnot = []

        delkaWordArr = len(wordArr)

        # pokud je prvniIndex za koncem WordArray, pak vrati pouze posledni hodnotu
        if(posledniIndex > len(wordArr)):
            poleHodnot.append(wordArr[len(wordArr)-1])
        else:
            for i in range(prvniIndex, posledniIndex):
                hodnota = wordArr[i]
                poleHodnot.append(hodnota)

        return(poleHodnot)


    # vrati klicove slovo pro radek "set"
    def vratKlicoveSlovoSet(self, setRadek):

        radekObsahujeNodes = self.detekujPritomnostSlova(setRadek, "nodes")
        radekObsahujeElementranges = self.detekujPritomnostSlova(setRadek, "elementranges")
        radekObsahujeElementedges = self.detekujPritomnostSlova(setRadek, "elementedges")
        radekObsahujeElements = self.detekujPritomnostSlova(setRadek, "elements")
        radekObsahujeNoderanges = self.detekujPritomnostSlova(setRadek, "noderanges")

        if (radekObsahujeNodes == True):
            klicovSlovo = "nodes"
        if (radekObsahujeElementranges == True):
            klicovSlovo = "elementranges"
        if (radekObsahujeElementedges == True):
            klicovSlovo = "elementedges"
        if (radekObsahujeElements == True):
            klicovSlovo = "elements"
        if (radekObsahujeNoderanges == True):
            klicovSlovo = "noderanges"


        return(klicovSlovo)


    def detekujPritomnostSlova(self, radek, klicoveSlovo):

        if(radek.find(klicoveSlovo) == -1):
            obsahujeKlicoveSlovo = False
        else:
            obsahujeKlicoveSlovo = True

        return(obsahujeKlicoveSlovo)


    # vrati cislaUzlu a jejich souradnice
    def vratCislaUzluSJejichSouradnicemi(self, cislaUzlu, X, Y):

        cislaUzluSouradnice = []

        for i in range(0, len(cislaUzlu)):
            cisloUzlu = cislaUzlu[i]
            sourX = X[i]
            sourY = Y[i]

            uzelXY = []
            uzelXY.append(cisloUzlu)
            uzelXY.append(sourX)
            uzelXY.append(sourY)

            cislaUzluSouradnice.append(uzelXY)

        return(cislaUzluSouradnice)


    # vrat pole jejich polozky jsou prvnimi slovy z self.poleRadku
    def vratPolePrvnichSlov(self):

        for r in range(0, len(self.poleRadku)):

            radek = self.poleRadku[r]
            wordArr = radek.split()
            if(wordArr == []):
                prvniSlovoNaRadku = ""
            else:
                prvniSlovoNaRadku = wordArr[0]

            self.polePrvnichSlov.append(prvniSlovoNaRadku)



    # podle prvniho slova na radku vybere
    def vytvorPolePodlePrvnihoSlovaNaRadku(self, prvniSlovo):

        poleRadkuPodlePrvnihoSlova = []

        for r in range(0, len(self.polePrvnichSlov)):
            prvniSlovoPole = self.polePrvnichSlov[r]
            if(prvniSlovo == prvniSlovoPole):
                radek = self.poleRadku[r]
                poleRadkuPodlePrvnihoSlova.append(radek)

        return(poleRadkuPodlePrvnihoSlova)



    # vybere sloupec z pole radku - jedna se napr. o souradnici x nebo cokoliv jineho
    # vybira substring z pole radku, ktery je na dany pozici oddeleny mezerami
    def vratPoleJednohoSLoupce(self, poleRadku, pozice):

        sloupecPole = []


        for r in range(0, len(poleRadku)):
            radek = poleRadku[r]
            wordArr = radek.split()
            substring = wordArr[pozice]
            cislo = float(substring)

            sloupecPole.append(cislo)

        return(sloupecPole)


    # vytvori pole XYZ jako pole souradnic
    def vytvorPoleXYZ(self, index):
        x = self.souradniceX[int(index)-1]
        y = self.souradniceY[int(index)-1]
        z = self.souradniceZ[int(index)-1]

        poleXYZ = []
        poleXYZ.append(x)
        poleXYZ.append(y)
        poleXYZ.append(z)

        return(poleXYZ)


    # sestavi souradnice elementu
    def sestavSouradnicePrutu(self):

        for r in range(0, len(self.poleBeam2d)):
            index1 = self.uzelElementu1[r]
            index2 = self.uzelElementu2[r]

            poleXYZ1 = self.vytvorPoleXYZ(index1)
            poleXYZ2 = self.vytvorPoleXYZ(index2)

            souradnicePrutu = []
            uzlyPrutu = []

            souradnicePrutu.append(poleXYZ1)
            souradnicePrutu.append(poleXYZ2)

            uzlyPrutu.append(index1)
            uzlyPrutu.append(index2)

            self.souradniceVsechPrutu.append(souradnicePrutu)
            self.uzlyPrutu.append(uzlyPrutu)


    # sestavi souradnice trojuhelnikoveho elementu
    def sestavSouradniceTrojuhelnika(self):

        for r in range(0, len(self.poleTr1supgaxi)):
            index1 = self.uzelElementu1[r]
            index2 = self.uzelElementu2[r]
            index3 = self.uzelElementu3[r]

            poleXYZ1 = self.vytvorPoleXYZ(index1)
            poleXYZ2 = self.vytvorPoleXYZ(index2)
            poleXYZ3 = self.vytvorPoleXYZ(index3)

            souradniceTrojUhelnika = []
            uzlyTrojuhelnika = []

            souradniceTrojUhelnika.append(poleXYZ1)
            souradniceTrojUhelnika.append(poleXYZ2)
            souradniceTrojUhelnika.append(poleXYZ3)

            uzlyTrojuhelnika.append(index1)
            uzlyTrojuhelnika.append(index2)
            uzlyTrojuhelnika.append(index3)

            self.souradniceVsechTrojuhelniku.append(souradniceTrojUhelnika)
            self.uzlyTrojuhelnika.append(uzlyTrojuhelnika)


    def sestavSouradniceUzlu(self):

        for i in range(0, len(self.cislaUzlu)):
            uzel = self.cislaUzlu[i]
            poleXYZ1 = self.vytvorPoleXYZ(uzel)
            sourX = poleXYZ1[0]
            sourY = poleXYZ1[1]

            uzelXY = []
            uzelXY.append(uzel)
            uzelXY.append(sourX)
            uzelXY.append(sourY)

            self.cislaUzluSouradnice.append(uzelXY)


    # slouci uzelElementu1 a uzelElementu2 do jednoho pole, tak aby data dokazal predat dal
    # data je treba predavat z duvodu aby sla porovnat mezi DofManager output a Beam element output
    def kElementumZapisCislaUzluZacatkuAKonce(self, uzelElementu1, uzelElementu2):

        # vytvori pole, kam uklada zacatky a konce uzlu elementu - cisla uzlu
        cislaUzluZacatekAKonecKonecElementu = []

        for i in range(0, len(uzelElementu1)):
            uzel1 = uzelElementu1[i]
            uzel2 = uzelElementu2[i]

            # vytvori promennaou kam uklada cisla zacatku a konce elementu
            zacatekAKonecElementuUzly = []
            zacatekAKonecElementuUzly.append(uzel1)
            zacatekAKonecElementuUzly.append(uzel2)

            cislaUzluZacatekAKonecKonecElementu.append(zacatekAKonecElementuUzly)


        return(cislaUzluZacatekAKonecKonecElementu)




