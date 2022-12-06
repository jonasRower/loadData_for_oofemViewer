
import NactiSoubor
import roztridData
import podpory

class inFile:

    def __init__(self):

        # pracuje s in-souborem
        adresaIn = "axi01.oofem.in"
        dataIn = NactiSoubor.txt(adresaIn)
        self.poleRadkuIn = dataIn.getPole()


        # ziska souradnice zacatku a konce prutu
        elementyBeam2D = roztridData.data(self.poleRadkuIn)
        self.uzlyAJejichSouradnice = elementyBeam2D.getUzlyASouradnice()
        self.souradniceVsechTrojuhelniku = elementyBeam2D.getSouradniceVsechTrojuhelniku()
        self.uzlyTrojuhelnika = elementyBeam2D.getUzlyTrojuhelnika()

        self.boundaryConditionPole = elementyBeam2D.getBoundaryCondition()
        self.setyDataPole = elementyBeam2D.getSetyDataPole()

        # souradnice podpor dopocitava z BoundaryConditions a dopocitava je ve tride podpory
        roztridPodpory = podpory.podporyData(self.boundaryConditionPole, self.setyDataPole, self.uzlyAJejichSouradnice)

        self.podporyKloubovePosuvneVodorovne = roztridPodpory.getPodporyKloubovePosuvneVodorovne()
        self.podporyKloubovePosuvneSvisle = roztridPodpory.getPodporyKloubovePosuvneSvisle()
        self.podporyVetknute = roztridPodpory.getPodporyVetknute()



    # data ziskane zde
    def getSouradnicePrutu(self):
        return(self.souradnicePrutu)

    def getUzlyASouradnice(self):
        return(self.uzlyAJejichSouradnice)

    def getSouradniceVsechTrojuhelniku(self):
        return(self.souradniceVsechTrojuhelniku)

    def getUzlyTrojuhelnika(self):
        return (self.uzlyTrojuhelnika)


    # data ziskane z tridy podpory
    def getPodporyKloubovePosuvneVodorovne(self):
        return (self.podporyKloubovePosuvneVodorovne)

    def getPodporyKloubovePosuvneSvisle(self):
        return (self.podporyKloubovePosuvneSvisle)

    def getPodporyVetknute(self):
        return (self.podporyVetknute)



