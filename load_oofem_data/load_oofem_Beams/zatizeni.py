
class zatizeniData:

    def __init__(self, ConstantEdgeLoadDataPole, StructTemperatureLoadPole, boundaryConditionsDataPole, NodalLoadDataPole, setyDataPole, pocetPrutu, uzlyAJejichSouradnice):

        self.ConstantEdgeLoadDataPole = ConstantEdgeLoadDataPole
        self.StructTemperatureLoadPole = StructTemperatureLoadPole
        self.boundaryConditionsDataPole = boundaryConditionsDataPole
        self.NodalLoadDataPole = NodalLoadDataPole
        self.setyDataPole = setyDataPole
        self.pocetPrutu = pocetPrutu
        self.uzlyAJejichSouradnice = uzlyAJejichSouradnice

        # musim vymyslet jak sem dostanu pole Dof
        # zatim nastavuji na tvrdo
        self.poleDof = []
        self.poleDof.append('1')
        self.poleDof.append('3')
        self.poleDof.append('5')

        # vykonava program
        self.slucData(self.ConstantEdgeLoadDataPole, self.StructTemperatureLoadPole, self.boundaryConditionsDataPole, self.NodalLoadDataPole, self.setyDataPole)
        self.vratDataMain()


    # getry
    def getSiloveZatizeniNaPrutech(self):
        return(self.siloveZatizeniNaPrutech)

    def getZatizeniTeplotouHorniVlakna(self):
        return(self.zatizeniTeplotouHorniVlakna)

    def getZatizeniTeplotouDolniVlakna(self):
        return(self.zatizeniTeplotouDolniVlakna)

    def getVynuceneZatizeniPodpor(self):
        return(self.vynuceneZatizeniPodpor)

    def getSilyAJejichSouradnice(self):
        return(self.silyAJejichSouradnice)




    # volano primo konstruktorem
    def slucData(self, ConstantEdgeLoadDataPole, StructTemperatureLoadPole, boundaryConditionsDataPole, NodalLoadDataPole, setyDataPole):

        # sloucene pole se sety
        self.poleConstantEdgeLoadSety = self.sestavDataSetyPole(ConstantEdgeLoadDataPole, setyDataPole)
        self.poleStructTemperatureLoadSety = self.sestavDataSetyPole(StructTemperatureLoadPole, setyDataPole)
        self.poleBoundaryConditionsSety = self.sestavDataSetyPole(boundaryConditionsDataPole, setyDataPole)
        self.poleNodalLoadSety = self.sestavDataSetyPole(NodalLoadDataPole, setyDataPole)


    # volano primo konstruktorem
    # pripravi data tak, aby byly roztrideny podle DOF
    def vratDataMain(self):

        # pripravi data, aby mohl vykreslit spojite zatizeni
        self.siloveZatizeniNaPrutech = self.sestavZatizeniPruty(self.poleConstantEdgeLoadSety)
        self.zatizeniTeplotouHorniVlakna = self.vratPoleLoadSetyProTemperatureLoad(self.poleStructTemperatureLoadSety, 0)
        self.zatizeniTeplotouDolniVlakna = self.vratPoleLoadSetyProTemperatureLoad(self.poleStructTemperatureLoadSety, 1)

        # pripravi data, aby mohl vykreslit zatizeni na uzly
        self.vynuceneZatizeniPodpor = self.sestavZatizeniUzlove(self.poleBoundaryConditionsSety, self.uzlyAJejichSouradnice)
        self.silyAJejichSouradnice = self.sestavZatizeniUzlove(self.poleNodalLoadSety, self.uzlyAJejichSouradnice)




    # vrati data oddelene pro horni a dolni vlakna
    # pokud vlaknaIndex = 0, pak vraci horni vlakna
    # pokud vlaknaIndex = 1, pak vraci dolni vlakna
    def vratPoleLoadSetyProTemperatureLoad(self, poleStructTemperatureLoadSety, vlaknaIndex):

        pocetPrutu = self.pocetPrutu
        temperatureZatizeni = self.sestavDataLoadProVsechnyPruty(poleStructTemperatureLoadSety)
        temperatureVlaknaPole = []


        # vytvori zatim prazdne pole, ktere bude prepisovat
        prutyZatizeniPole = self.vytvorDataProJSONPrutyPrazdne(pocetPrutu)

        for iPrut in range(0, len(temperatureZatizeni)):
            temperatureZatizeniPrut = temperatureZatizeni[iPrut]
            cisloPrutu = temperatureZatizeniPrut[0]
            indexPrutu = cisloPrutu-1
            tempPole = temperatureZatizeniPrut[1]
            tempVal = tempPole[vlaknaIndex]

            # vytvori tempRadek
            zatizeniCelyPrut = self.vytvorTempRadek(tempVal)

            # zapise data - prepise jiz aktualni prutyZatizeniPole
            prutyZatizeniPole[indexPrutu] = zatizeniCelyPrut

        return(prutyZatizeniPole)


    def vytvorTempRadek(self, tempVal):

        tempRadek = []
        tempRadek.append('0')
        tempRadek.append(tempVal)
        tempRadek.append('0')
        tempRadek.append('0')
        tempRadek.append(tempVal)
        tempRadek.append('0')

        return(tempRadek)


    # slouci data a sety do dvojice radku pole
    # a to nejen ConstantEdgeLoadDataPole, ale i jakekoliv jine
    def sestavDataSetyPole(self, ConstantEdgeLoadDataPole, setyDataPole):

        datasetyPole = []

        for r in range(0, len(ConstantEdgeLoadDataPole)):
            ConstantEdgeLoadDataRadek = ConstantEdgeLoadDataPole[r]
            cisloSetuPole = ConstantEdgeLoadDataRadek[len(ConstantEdgeLoadDataRadek) - 1]
            cisloSetu = int(cisloSetuPole[0])
            setyDataRadek = self.vratSetPodleCislaSetu(setyDataPole, cisloSetu)

            ConstantEdgeLoadSetData = []
            ConstantEdgeLoadSetData.append(ConstantEdgeLoadDataRadek)
            ConstantEdgeLoadSetData.append(setyDataRadek)

            datasetyPole.append(ConstantEdgeLoadSetData)

        return (datasetyPole)



    def sestavZatizeniPruty(self, polePrutyLoadSety):

        prutyZatizeni = self.sestavDataLoadProVsechnyPruty(polePrutyLoadSety)
        pocetPrutu = self.pocetPrutu

        # vytvori zatim prazdne pole, ktere bude prepisovat
        prutyZatizeniPole = self.vytvorDataProJSONPrutyPrazdne(pocetPrutu)

        for iPrut in range(0, len(prutyZatizeni)):
            prutZatizeni = prutyZatizeni[iPrut]
            cisloPrutu = prutZatizeni[0]
            indexPrutu = int(cisloPrutu) -1

            zatizeni = prutZatizeni[1]
            zatizeniZacatek = zatizeni
            zatizeniKonec = zatizeni
            zatizeniCelyPrut = zatizeniZacatek + zatizeniKonec

            # zapise data - prepise jiz aktualni prutyZatizeniPole
            prutyZatizeniPole[indexPrutu] = zatizeniCelyPrut

        return(prutyZatizeniPole)


    def sestavDataLoadProVsechnyPruty(self, elementSetDataPole):

        dataVsechnyPruty = []

        for iPrut in range(0, len(elementSetDataPole)):
            polozkaJedenPrut = elementSetDataPole[iPrut]
            dataLoad = polozkaJedenPrut[0]
            velikostZatizeniVsechnyDof = dataLoad[2]
            cisloPrutuData = polozkaJedenPrut[1]
            cisloPrutuPole = cisloPrutuData[3]
            cisloPrutu = int(cisloPrutuPole[1])

            zatizeniDataJedenPrut = []
            zatizeniDataJedenPrut.append(cisloPrutu)
            zatizeniDataJedenPrut.append(velikostZatizeniVsechnyDof)
            dataVsechnyPruty.append(zatizeniDataJedenPrut)

        return(dataVsechnyPruty)


    def sestavZatizeniUzlove(self, poleUzlyLoadSety, uzlyAJejichSouradnice):

        zatizeniDataVsechnyUzly = self.sestavDataLoadProVsechnyUzly(poleUzlyLoadSety)
        zatizeniDataVsechnyUzlyPoUzlech = self.vratZatizeniDataVsechnyUzlyPoUzlech(zatizeniDataVsechnyUzly)
        vsechnySlozkyZatizeniUzlove = self.vytvorDataSeVsemiSlozkamiZatizeniUzloveho(zatizeniDataVsechnyUzlyPoUzlech, "freeDOF")
        silyAJejichSouradnice = self.vratSilyAJejichSouradnice(vsechnySlozkyZatizeniUzlove, uzlyAJejichSouradnice)


        return (silyAJejichSouradnice)


    def vratSilyAJejichSouradnice(self, vsechnySlozkyZatizeniUzlove, uzlyAJejichSouradnice):

        silyAJejichSouradnice = []

        for iUzel in range(0, len(vsechnySlozkyZatizeniUzlove)):
            slozkyZatizeniUzel = vsechnySlozkyZatizeniUzlove[iUzel]

            cisloUzlu = slozkyZatizeniUzel[0]
            slozkySily = slozkyZatizeniUzel[1]
            indexUzlu = int(cisloUzlu) - 1
            souradniceUzlu = uzlyAJejichSouradnice[indexUzlu]

            slozkyZatizeniASouradnice = []
            slozkyZatizeniASouradnice.append(cisloUzlu)
            slozkyZatizeniASouradnice.append(souradniceUzlu)
            slozkyZatizeniASouradnice.append(slozkySily)

            silyAJejichSouradnice.append(slozkyZatizeniASouradnice)

        return(silyAJejichSouradnice)


    # vrati pole, kde kazdy radek bude obsahovat
    # [cisloUzlu, [FX, FY, M]]
    # do jednotlivych smeru vklada string freeDOF, ktery nasledne prepisuje
    def vytvorDataSeVsemiSlozkamiZatizeniUzloveho(self, zatizeniDataVsechnyUzlyPoUzlech, freeDOF):

        vsechnySlozkyZatizeniUzlove = []

        for iUzel in range(0, len(zatizeniDataVsechnyUzlyPoUzlech)):
            zatizeniDataUzel = zatizeniDataVsechnyUzlyPoUzlech[iUzel]
            dofPole = zatizeniDataUzel[0]
            cisloUzlu = zatizeniDataUzel[1]
            zatizeniPole = zatizeniDataUzel[2]

            radek = self.vratRadekFxFyMZatizeniUzlove(dofPole, zatizeniPole, freeDOF)

            vsechnySlozkyZatizeniUzloveRadek = []
            vsechnySlozkyZatizeniUzloveRadek.append(cisloUzlu)
            vsechnySlozkyZatizeniUzloveRadek.append(radek)

            vsechnySlozkyZatizeniUzlove.append(vsechnySlozkyZatizeniUzloveRadek)

        return(vsechnySlozkyZatizeniUzlove)


    def vratRadekFxFyMZatizeniUzlove(self, dofPole, zatizeniPole, freeDOF):

        radek = []
        radek.append(freeDOF)
        radek.append(freeDOF)
        radek.append(freeDOF)


        for iDof in range(0, len(dofPole)):
            dof = dofPole[iDof]
            DofPoradi = self.vratPoradiPolozky(self.poleDof, dof)
            dofZatizeni = zatizeniPole[iDof]
            radek[DofPoradi] = dofZatizeni

        return(radek)



    # upravi pole tak, aby na kazdem radku byl jen jeden uzel
    def vratZatizeniDataVsechnyUzlyPoUzlech(self, zatizeniDataVsechnyUzly):

        zatizeniDataVsechnyUzlyNew = zatizeniDataVsechnyUzly

        for i in range(0, len(zatizeniDataVsechnyUzly)):
            zatizeniDataVsechnyUzlyRadek = zatizeniDataVsechnyUzly[i]

            DofNaRadku = zatizeniDataVsechnyUzlyRadek[0]
            seznamUzluNaRadku = zatizeniDataVsechnyUzlyRadek[1]
            hodnotyNaRadku = zatizeniDataVsechnyUzlyRadek[2]

            pocetUzlu = len(seznamUzluNaRadku)

            for iUzel in range(0, pocetUzlu):
                cisloUzlu = seznamUzluNaRadku[iUzel]

                radekNew = []
                radekNew.append(DofNaRadku)
                radekNew.append(cisloUzlu)
                radekNew.append(hodnotyNaRadku)

                if(iUzel == 0):
                    zatizeniDataVsechnyUzlyNew[i] = radekNew
                else:
                    zatizeniDataVsechnyUzlyNew.append(radekNew)

        return(zatizeniDataVsechnyUzlyNew)


    def sestavDataLoadProVsechnyUzly(self, nodalSetDataPole):

        dataVsechnyUzly = []

        for iUzel in range(0, len(nodalSetDataPole)):
            polozkaJedenUzel = nodalSetDataPole[iUzel]
            dataLoad = polozkaJedenUzel[0]
            sadaDof = dataLoad[2]
            sadaVelikosti = dataLoad[3]

            cisloUzluData = polozkaJedenUzel[1]
            cisloUzluPole = cisloUzluData[2]

            dataJedenUzel = []
            dataJedenUzel.append(sadaDof)
            dataJedenUzel.append(cisloUzluPole)
            dataJedenUzel.append(sadaVelikosti)


            dataVsechnyUzly.append(dataJedenUzel)

        return(dataVsechnyUzly)


    def vratSetPodleCislaSetu(self, setyDataPole, cisloSetuExp):

        for i in range(0, len(setyDataPole)):
            setyDataRadek = setyDataPole[i]
            cisloSetu = setyDataRadek[0]
            if(cisloSetu == cisloSetuExp):
                setyDataRadekPodleCislaSetu = setyDataRadek
                break

        return(setyDataRadekPodleCislaSetu)


    def sestavZatizeniUzlyProDanyDof(self, dataVsechnyUzly, iDofExp):

        zatizeniDataVsechnyUzlyDofExp = []

        #zatim je natvrdo
        vsechnyDOF = []
        vsechnyDOF.append('1')
        vsechnyDOF.append('3')
        vsechnyDOF.append('5')

        for iUzel in range(0, len(dataVsechnyUzly)):
            zatizeniDatJedenUzel = dataVsechnyUzly[iUzel]
            seznamDof = zatizeniDatJedenUzel[0]
            danyDof = vsechnyDOF[iDofExp]
            iDofVyhledavany = self.vratPoradiPolozky(seznamDof, danyDof)

            if(iDofVyhledavany > -1):

                cisloUzlu = zatizeniDatJedenUzel[1]
                zatizeniVsechnyDOF = zatizeniDatJedenUzel[2]
                zatizeniDofExp = zatizeniVsechnyDOF[iDofVyhledavany]

                zatizeniDataJedenUzelDofExp = []
                zatizeniDataJedenUzelDofExp.append(cisloUzlu)
                zatizeniDataJedenUzelDofExp.append(zatizeniDofExp)
                zatizeniDataVsechnyUzlyDofExp.append(zatizeniDataJedenUzelDofExp)

            else:
                zatizeniDataVsechnyUzlyDofExp.append([])

        return(zatizeniDataVsechnyUzlyDofExp)


    def vratPoradiPolozky(self, polozkyPole, polozkaExp):

        indexPolozky = -1

        for i in range(0, len(polozkyPole)):
            polozka = polozkyPole[i]
            if (polozka == polozkaExp):
                indexPolozky = i
                break

        return (indexPolozky)


    # radek je plny [] a [1,2,3], rozlozi data, aby byly lepe citelne
    def prevedPoleNaJedenRadek(self, radekKRozlozeni):

        radekNew = []

        for i in range(0, len(radekKRozlozeni)):
            subRadek = radekKRozlozeni[i]
            delkaSubRadku = len(subRadek)
            if (delkaSubRadku > 0):
                poleRadekUzly = self.zprehledniDataRadek(subRadek)
                radekNew = radekNew + poleRadekUzly

        return (radekNew)



    def zprehledniDataRadek(self, radekUzly):
        uzlyPole = radekUzly[0]
        velikost = radekUzly[1]

        poleRadekUzly = []

        for i in range(0, len(uzlyPole)):
            uzel = uzlyPole[i]

            uzelAVelikost = []
            uzelAVelikost.append(uzel)
            uzelAVelikost.append(velikost)

            poleRadekUzly.append(uzelAVelikost)

        return (poleRadekUzly)



    # vytvori pole , ktere bude postupne doplnovat - prepisovat
    def vytvorDataProJSONPrutyPrazdne(self, pocetPrutu):

        polePrazdne = []

        for r in range(0, pocetPrutu):
            poleRadek = []
            for s in range(0, 6):
                poleRadek.append('0')

            polePrazdne.append(poleRadek)

        return (polePrazdne)