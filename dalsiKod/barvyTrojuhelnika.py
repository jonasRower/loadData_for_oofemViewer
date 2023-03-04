
# pokracovat-zde - prumerovat hodnoty -- projet data v novem razeni a prumerovat 3 uzly (vsechny casy)
# zprumerujHodnoty - hotove

# dopocitava barvy trojuhelnika, tak aby vykresloval pomoci barev velikosti deformaci
class barvy2DElementu:

    def __init__(self, nodalDisplacements, uzlyTrojuhelnika):

        self.nodalDisplacements = nodalDisplacements
        self.uzlyTrojuhelnika = uzlyTrojuhelnika

        self.VsechnyDof = self.vratVsechnyDof(self.nodalDisplacements)
        self.SeznamUzluPole = self.vratVztahCislaUzluAIndexuPole(self.nodalDisplacements[0])


        # jedna-li se o 3 Dof
        self.dataKrokyDisplacement = [[], [], []]

        # nove se radi data (daji se dobre vykreslovat grafy, jelikoz cas je na posledni urovni)
        # 1. uroven - dof
        # 2. uroven - uzly
        # 3. uroven - casove kroky
        self.nodalDisplacementsProGraf = self.preskupData(self.nodalDisplacements)

        self.prumerneHodnoty = self.zprumerujHodnoty(self.uzlyTrojuhelnika, self.nodalDisplacementsProGraf)

        # zjisti pomer skalovani, vsechny prumerne hodnoty budou vztazene ke stupnici 0-150
        self.poleSkalovani = self.vytvorSkalovani(self.prumerneHodnoty)

        #preskaluje vsechny prumerne hodnoty, tak aby byly na stupnici mezi 0-150
        self.prumerneHodnotySkalovane = self.preskalujPrumerneHodnoty(self.prumerneHodnoty, self.poleSkalovani)

        # vrati hodnoty HSL, tak aby se cele pole dalo pohodlne zapsat
        # je tedy potreba ke skalovane hodnote pricist 200 a zaokrouhlit, HSL hodnota je vzdy kladna (tedy absolutni)
        self.prumerneHodnotySkalovaneHSL = self.priradPrumernymHodnotamHSL(self.prumerneHodnotySkalovane)


        print("")

    #oddelit jeste data a vracet self.nodalDisplacementsProGraf, coz jsou data pro grafy

    def getHodnotyHsl(self):
        return(self.prumerneHodnotySkalovaneHSL)

    def getNodalDisplacementsProGraf(self):
        return(self.nodalDisplacementsProGraf)

    def getPrumerneHodnoty(self):
        return(self.prumerneHodnoty)


    def vratPoleVsechPrumernychHodnotProDofAOFT(self, prumerneHodnoty, dofExp, OFTExp):

        prumerneHodnotyDof = prumerneHodnoty[dofExp]
        polePrumernychHodnotProDOFAOFT = []

        for iElement in range(0, len(prumerneHodnotyDof)):
            prumerneHodnotyOFTPole = prumerneHodnotyDof[iElement]
            prumernaHodnotaOFT = prumerneHodnotyOFTPole[OFTExp]
            polePrumernychHodnotProDOFAOFT.append(prumernaHodnotaOFT)

        return(polePrumernychHodnotProDOFAOFT)


    # vrati pole maximalnich prumernych hhodnot, ktere jsou razeny:
    # 1) DOF
    # 2) OFT
    def vytvorSkalovani(self, prumerneHodnoty):

        maximalniPrumerneHodnotyPoleDof = []
        pomerSkalovaniDOF = []

        for iDof in range(0, len(prumerneHodnoty)):
            prumerneHodnotyDof = prumerneHodnoty[iDof]
            maximalniPrumerneHodnotyPoleOFT = []
            pomerSkalovaniOFT = []

            for OFT in range(0, len(prumerneHodnotyDof[0])):
                polePrumernychHodnot = self.vratPoleVsechPrumernychHodnotProDofAOFT(prumerneHodnoty, iDof, OFT)
                maximalniPrumernaHodnota = self.vratMaximalniHodnotu2(polePrumernychHodnot)
                PomerSkalovani = 100 / maximalniPrumernaHodnota

                maximalniPrumerneHodnotyPoleOFT.append(maximalniPrumernaHodnota)
                pomerSkalovaniOFT.append(PomerSkalovani)

            maximalniPrumerneHodnotyPoleDof.append(maximalniPrumerneHodnotyPoleOFT)
            pomerSkalovaniDOF.append(pomerSkalovaniOFT)

        return(pomerSkalovaniDOF)


    def vratMaximalniHodnotu2(self, polePrumernychHodnot):

        maximalniPrumernaHonota = 0

        for i in range(0, len(polePrumernychHodnot)):
            prumernaHodnota = polePrumernychHodnot[i]
            if(abs(prumernaHodnota) > maximalniPrumernaHonota):
                maximalniPrumernaHonota = abs(prumernaHodnota)

        return(maximalniPrumernaHonota)


    def priradPrumernymHodnotamHSL(self, prumerneHodnotySkalovane):

        prumerneHodnotyHSL= []

        for iDof in range(0, len(prumerneHodnotySkalovane)):
            prumerneHodnotyDof = prumerneHodnotySkalovane[iDof]
            prumerneHodnotyDofHSL = []

            for iUzel in range(0, len(prumerneHodnotyDof)):
                prumerneHodnotyUzel = prumerneHodnotyDof[iUzel]
                prumerneHodnotyUzelHSL = []

                for OFT in range(0, len(prumerneHodnotyUzel)):
                    hodnotaOFT = prumerneHodnotyUzel[OFT]
                    hodnotaHSL = 250 + abs(round(hodnotaOFT))

                    prumerneHodnotyUzelHSL.append(hodnotaHSL)

                prumerneHodnotyDofHSL.append(prumerneHodnotyUzelHSL)

            prumerneHodnotyHSL.append(prumerneHodnotyDofHSL)

        return (prumerneHodnotyHSL)



    def preskalujPrumerneHodnoty(self, prumerneHodnoty, poleSkalovani):

        prumerneHodnotySkalovane = []

        for iDof in range(0, len(prumerneHodnoty)):
            prumerneHodnotyDof = prumerneHodnoty[iDof]
            pomerSkalovaniDof = poleSkalovani[iDof]
            prumerneHodnotyDofSkalovane = []

            for iUzel in range(0, len(prumerneHodnotyDof)):
                prumerneHodnotyUzel = prumerneHodnotyDof[iUzel]
                prumerneHodnotyUzelSkalovane = []

                for OFT in range(0, len(prumerneHodnotyUzel)):
                    hodnotaOFT = prumerneHodnotyUzel[OFT]
                    pomerSkalovani = pomerSkalovaniDof[OFT]
                    hodnotaOFTSkalovana = abs(hodnotaOFT) * pomerSkalovani

                    prumerneHodnotyUzelSkalovane.append(hodnotaOFTSkalovana)

                prumerneHodnotyDofSkalovane.append(prumerneHodnotyUzelSkalovane)

            prumerneHodnotySkalovane.append(prumerneHodnotyDofSkalovane)

        return(prumerneHodnotySkalovane)

    # zjisti maximalni absoultni hodnotu, aby mohl vsechny hodnoty preskalovat
    def vratMaximalniHodnotu(self, prumerneHodnoty):

        maximalniHodnota = 0

        for iDof in range(0, len(prumerneHodnoty)):
            prumerneHodnotyDof = prumerneHodnoty[iDof]

            for iUzel in range(0, len(prumerneHodnotyDof)):
                prumerneHodnotyUzel = prumerneHodnotyDof[iUzel]

                for OFT in range(0, len(prumerneHodnotyUzel)):
                    hodnotaOFT = prumerneHodnotyUzel[OFT]

                    if(abs(hodnotaOFT) > maximalniHodnota):
                        maximalniHodnota = hodnotaOFT

        return(maximalniHodnota)

    # zprumeruje hodnoty, aby mohl je vykreslit v grafice barvou
    def zprumerujHodnoty(self, uzlyTrojuhelnika, nodalDisplacementsProGraf):

        prumerneHodnotyDof = []

        for iDof in range(0, len(self.VsechnyDof)):
            nodalDisplacementsDof = nodalDisplacementsProGraf[iDof]
            prumerneHodnotyVsechnyUzly = []

            for i in range(0, len(uzlyTrojuhelnika)):
                element = uzlyTrojuhelnika[i]
                uzel1 = element[0]
                uzel2 = element[1]
                uzel3 = element[2]

                indexPole1 = self.najdiIndexPole(self.SeznamUzluPole, uzel1)
                indexPole2 = self.najdiIndexPole(self.SeznamUzluPole, uzel2)
                indexPole3 = self.najdiIndexPole(self.SeznamUzluPole, uzel3)

                nodalDisplacementVsechnyOFTUzel1 = nodalDisplacementsDof[indexPole1]
                nodalDisplacementVsechnyOFTUzel2 = nodalDisplacementsDof[indexPole2]
                nodalDisplacementVsechnyOFTUzel3 = nodalDisplacementsDof[indexPole3]

                nodalDisplacementVsechnyOFTElement = self.zprumerujPosunyNaElementuVsechnyOFT(nodalDisplacementVsechnyOFTUzel1, nodalDisplacementVsechnyOFTUzel2, nodalDisplacementVsechnyOFTUzel3)
                prumerneHodnotyVsechnyUzly.append(nodalDisplacementVsechnyOFTElement)

            prumerneHodnotyDof.append(prumerneHodnotyVsechnyUzly)

        return(prumerneHodnotyDof)


    # zprumeruje nodal displacements ve vseh OFT, v danych 3 uzlech (elementu) a danym DOF
    def zprumerujPosunyNaElementuVsechnyOFT(self, NodalDisplUzel1, NodalDisplUzel2, NodalDisplUzel3):

        NodalDispElementOFT = []

        for i in range(0, len(NodalDisplUzel1)):
            uzel1OFT = NodalDisplUzel1[i]
            uzel2OFT = NodalDisplUzel2[i]
            uzel3OFT = NodalDisplUzel3[i]

            prumernaHodnota = (float(uzel1OFT) + float(uzel2OFT) + float(uzel3OFT))/3
            NodalDispElementOFT.append(prumernaHodnota)

        return(NodalDispElementOFT)




    # preskupuje data aby byla lepe razena
    def preskupData(self, nodalDisplacements):

        nodalDisplacementData = []

        # predpokladam, ze pocet uzlu je stejny jako v 1. kroce
        nodalDisplacements0 = nodalDisplacements[0]

        for i in range(0, len(self.VsechnyDof)):
            dof = self.VsechnyDof[i]

            nodalDisplacementDOF = []

            for iUz in range(0, len(nodalDisplacements0)):
                nodalDisplacementsOFTuzel = nodalDisplacements0[iUz]
                uzel = nodalDisplacementsOFTuzel[0]

                # opakovane hledam data
                nodalDisplacementVsechnyOFT = self.vratProDanyUzelADofDeformaceVeVsechOFT(nodalDisplacements, uzel, dof)
                nodalDisplacementDOF.append(nodalDisplacementVsechnyOFT)

            nodalDisplacementData.append(nodalDisplacementDOF)


        return(nodalDisplacementData)


    # vrati pole, kde je vztah mezi cislem uzlu a indexem v poli,
    # pole je pripraveno, aby se data nemusela vyhledavat opakovane
    def vratVztahCislaUzluAIndexuPole(self, nodalDisplacements0):

        seznamUzluPole = []

        for i in range(0, len(nodalDisplacements0)):
            radek = nodalDisplacements0[i]
            cisloUzlu = radek[0]
            seznamUzluPole.append(cisloUzlu)

        return(seznamUzluPole)


    #vrati Pole deformaci pro vsechny OFT
    def vratProDanyUzelADofDeformaceVeVsechOFT(self, nodalDisplacements, uzelExp, dofExp):

        nodalDisplacementVsechnyOFT = []

        for i in range(0, len(nodalDisplacements)):
            nodalDisplacementsOFT = nodalDisplacements[i]

            for iUz in range(0, len(nodalDisplacementsOFT)):
                nodalDisplacementsOFTuzel = nodalDisplacementsOFT[iUz]
                uzel = nodalDisplacementsOFTuzel[0]

                if(uzel == uzelExp):
                    dofPole = nodalDisplacementsOFTuzel[1]
                    nodalDisplacementPole = nodalDisplacementsOFTuzel[2]

                    for iDof in range(0, len(dofPole)):
                        dof = dofPole[iDof]
                        if(dof == dofExp):
                            nodalDisplacement = nodalDisplacementPole[iDof]
                            nodalDisplacementVsechnyOFT.append(nodalDisplacement)

                            break


        return(nodalDisplacementVsechnyOFT)



    # preuklada data do nove datove struktury, kde na podelne ose je cas
    def pridejDataDoPole(self, hodnota, index):

        dataPoleNew = []
        dataPole = self.dataKrokyDisplacement
        sloupec = dataPole[index]

        # rozsiri sloupec pole pod indexem "index" o jednu polozku
        sloupec.append(hodnota)
        sloupecRozsireny = sloupec

        # preulozi pole do pole noveho
        for i in range(0, len(dataPole)):
            if(i == index):
                sloupecNovy = sloupecRozsireny
            else:
                sloupecNovy = dataPole[i]

            dataPoleNew.append(sloupecNovy)
            print("")

        return(dataPoleNew)


    # function to get unique values
    def unique(self, list1):

        # intilize a null list
        unique_list = []

        # traverse for all elements
        for x in list1:
            # check if exists in unique_list or not
            if x not in unique_list:
                unique_list.append(x)

        return(unique_list)


    # zjistuje vsechny dof (aby vyloucil ze na nejakem radku jsou dof jine)
    def vratVsechnyDof(self, nodalDisplacements):  # pro jistotu projede vsechny data a proveri zda skutecne vsude se jedna o stejna dofs

        vsechnaDofs = []

        for i in range(0, len(nodalDisplacements)):
            nodalDisplacementsOFT = nodalDisplacements[i]

            for iUz in range(0, len(nodalDisplacementsOFT)):
                nodalDisplacementsOFTuzel = nodalDisplacementsOFT[iUz]
                dofPole = nodalDisplacementsOFTuzel[1]

                vsechnaDofs = vsechnaDofs + dofPole

        jedinecneDofs = self.unique(vsechnaDofs)

        return(jedinecneDofs)


    # prohleda seznam uzlu a vrati index, na jakym je dany uzel umisten
    def najdiIndexPole(self, seznamUzluPole, cisloUzluExp):

        for i in range(0, len(seznamUzluPole)):
            cisloUzlu = seznamUzluPole[i]
            if(cisloUzlu == cisloUzluExp):
                index = i
                break

        return(index)