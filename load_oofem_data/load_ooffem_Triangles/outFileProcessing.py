
import NactiSoubor
import vytvorDataSekci

class outFile:

    def __init__(self):

        # pracuje s out-souborem
        adresaOut = "axi01.oofem.out"
        dataOut = NactiSoubor.txt(adresaOut)
        poleRadkuOut = dataOut.getPole()

        dataSekci = vytvorDataSekci.vytvorSekce(poleRadkuOut)

        self.NodalDisplacement = dataSekci.getNodalDisplacements()
        self.LocalDisplacements = dataSekci.getLocalDisplacements()
        self.LocalForces = dataSekci.getLocalForces()
        self.Strains = dataSekci.getStrains()
        self.Stresses = dataSekci.getStresses()
        self.poleTime = dataSekci.getPoleTime()


    def getLocalDisplacements(self):
        return(self.LocalDisplacements)

    def getLocalForces(self):
        return(self.LocalForces)

    def getStrains(self):
        return(self.Strains)

    def getStresses(self):
        return (self.Stresses)

    def getNodalDisplacement(self):
        return(self.NodalDisplacement)

    def getPoleTime(self):
        return (self.poleTime)