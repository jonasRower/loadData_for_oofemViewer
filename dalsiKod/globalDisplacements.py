
# konvertuje nodal displacement na local displacement
class konvertujDisplacements:

    def __init__(self, NodalDisplacements, localDisplacements, cislaUzluZacatekAKonecElementu):

        self.NodalDisplacements = NodalDisplacements
        self.cislaUzluZacatekAKonecElementu = cislaUzluZacatekAKonecElementu
        self.localDisplacements = localDisplacements

        # nove pole
        self.localDisplacementKonvertovane = []

        # vyhleda data podle cisla uzlu a aktualniho OFT
        #self.NodalDisplacementPodleUzlu = self.vyhledejNodalDisplacementPodleUzlu(0, 1, self.NodalDisplacements)
        #self.zapisLocalDisplacementJedenPrut(self.NodalDisplacements, 0, 0, self.cislaUzluZacatekAKonecKonecElementu)
        self.localDisplacementKonvertovane = self.vratLocalDisplacementsKonvertovane(self.NodalDisplacements, self.cislaUzluZacatekAKonecElementu)



    # vrati data - geter
    def getLocalDisplacementsKonvertovane(self):
        return(self.localDisplacementKonvertovane)



    # vrati Local Displacement konvertovane z NodalDisplacement pro dany iOFT
    def vratLocalDisplacementsKonvertovane(self, NodalDisplacements, cislaUzluZacatekAKonecElementu):

        localDisplacementKonvertovane = []

        for iOFT in range(0, len(NodalDisplacements)):
            localDisplacementJedenPrut = []
            localDisplacementJedenPrut = self.vratLocalDisplacementsProOFT(NodalDisplacements, cislaUzluZacatekAKonecElementu, iOFT)

            localDisplacementKonvertovane.append(localDisplacementJedenPrut)

        return(localDisplacementKonvertovane)


    # vrati Local Displacement konvertovane z NodalDisplacement pro dany iOFT
    def vratLocalDisplacementsProOFT(self, NodalDisplacements, cislaUzluZacatekAKonecKonecElementu, iOFT):

        localDisplacementProOFT = []

        for iPrut in range(0, len(cislaUzluZacatekAKonecKonecElementu)):
            localDisplacementJedenPrut = self.zapisLocalDisplacementJedenPrut(NodalDisplacements, iOFT, iPrut, cislaUzluZacatekAKonecKonecElementu)
            localDisplacementProOFT.append(localDisplacementJedenPrut)

        return(localDisplacementProOFT)


    def zapisLocalDisplacementJedenPrut(self, NodalDisplacements, iOFT, cisloPrutu, cislaUzluZacatekAKonecKonecElementu):

        cislaUzluNaPrutu = []
        cislaUzluNaPrutu = cislaUzluZacatekAKonecKonecElementu[cisloPrutu]
        cisloUzluZacatekPrutu = cislaUzluNaPrutu[0]
        cisloUzluKonecPrutu = cislaUzluNaPrutu[1]

        localDisplacementsZacatekPrutu = self.vyhledejNodalDisplacementPodleUzlu(iOFT, cisloUzluZacatekPrutu, NodalDisplacements)
        localDisplacementsKonecPrutu = self.vyhledejNodalDisplacementPodleUzlu(iOFT, cisloUzluKonecPrutu, NodalDisplacements)

        localDisplacementsJedenPrut = localDisplacementsZacatekPrutu
        localDisplacementsJedenPrut = localDisplacementsJedenPrut + localDisplacementsKonecPrutu

        return(localDisplacementsJedenPrut)


    def vyhledejNodalDisplacementPodleUzlu(self, OFT, cisloUzluExp, NodalDisplacements):

        NodalDisplacementOFT = NodalDisplacements[OFT]

        for iUzel in range(0, len(NodalDisplacementOFT)):
            NodalDisplacementIUzel = NodalDisplacementOFT[iUzel]
            cisloUzlu = NodalDisplacementIUzel[0]

            if(cisloUzlu == cisloUzluExp):
                NodalDisplacementPodleUzlu = NodalDisplacementIUzel[2]
                break

        return(NodalDisplacementPodleUzlu)