
import NactiSoubor
import roztridData
import podpory
import zatizeni

class inFile:

    def __init__(self):

        # pracuje s in-souborem
        # pokud je nastaveno "beam2d_1.in", pak je treba nastavit  self.HledatVDofManager = False ve vytvorDataSekci

        #adresaIn = "axi01.oofem.in"
        adresaIn = "beam2d_1.in"
        dataIn = NactiSoubor.txt(adresaIn)
        self.poleRadkuIn = dataIn.getPole()
        self.obsahDomeny = self.zjistiDomenu(self.poleRadkuIn)

        # ziska souradnice zacatku a konce prutu
        elementyBeam2D = roztridData.data(self.poleRadkuIn)
        self.uzlyAJejichSouradnice = elementyBeam2D.getUzlyASouradnice()


        # ziska cisla uzlu zacatku a konce prutu
        self.cislaUzluZacatekAKonecKonecElementu = elementyBeam2D.getCislaUzluZacatekAKonecKonecElementu()


        # data pro vynucene pretvoreni podpor
        self.ConstantEdgeLoadDataPole = elementyBeam2D.getConstantEdgeLoadDataPole()

        # data pro vynucene pretvoreni podpor
        self.StructTemperatureLoadPole = elementyBeam2D.getStructTemperatureLoadPole()

        # data pro zatizeni na pruty
        self.boundaryConditionsDataPole = elementyBeam2D.getBoundaryConditionsDataPole()

        # data pro zatizeni teplotou (na pruty)
        self.NodalLoadDataPole = elementyBeam2D.getNodalLoadDataPole()


        if(self.obsahDomeny == '2dBeam'):
            self.souradnicePrutu = elementyBeam2D.getSouradniceVsechPrutu()
        else:
            self.souradniceVsechTrojuhelniku = elementyBeam2D.getSouradniceVsechTrojuhelniku()
            self.uzlyTrojuhelnika = elementyBeam2D.getUzlyTrojuhelnika()


        self.boundaryConditionPole = elementyBeam2D.getBoundaryCondition()
        self.setyDataPole = elementyBeam2D.getSetyDataPole()

        # souradnice podpor dopocitava z BoundaryConditions a dopocitava je ve tride podpory
        roztridPodpory = podpory.podporyData(self.boundaryConditionPole, self.setyDataPole, self.uzlyAJejichSouradnice)

        # dopocitava data pro zatizeni
        pocetPrutu = len(self.cislaUzluZacatekAKonecKonecElementu)
        roztridZatizeni = zatizeni.zatizeniData(self.ConstantEdgeLoadDataPole, self.StructTemperatureLoadPole, self.boundaryConditionsDataPole, self.NodalLoadDataPole, self.setyDataPole, pocetPrutu, self.uzlyAJejichSouradnice)

        # data z tridy podpory
        self.podporyKloubovePosuvneVodorovne = roztridPodpory.getPodporyKloubovePosuvneVodorovne()
        self.podporyKloubovePosuvneSvisle = roztridPodpory.getPodporyKloubovePosuvneSvisle()
        self.podporyVetknute = roztridPodpory.getPodporyVetknute()
        self.cislaUzluZacatekAKonecKonecElementu = elementyBeam2D.getCislaUzluZacatekAKonecKonecElementu()

        # data z tridy zatizeni
        self.siloveZatizeniNaPrutech = roztridZatizeni.getSiloveZatizeniNaPrutech()
        self.zatizeniTeplotouHorniVlakna = roztridZatizeni.getZatizeniTeplotouHorniVlakna()
        self.zatizeniTeplotouDolniVlakna = roztridZatizeni.getZatizeniTeplotouDolniVlakna()
        self.vynuceneZatizeniPodpor = roztridZatizeni.getVynuceneZatizeniPodpor()
        self.silyAJejichSouradnice = roztridZatizeni.getSilyAJejichSouradnice()


        # aby bezel kod stejnym kodem, je treba pridat "silyAJejichSouradnice" do fiktivniho 0. OFT
        self.silyAJejichSouradniceOFT = []
        self.silyAJejichSouradniceOFT.append(self.silyAJejichSouradnice)



    # data ziskane zde
    def getSouradnicePrutu(self):
        return(self.souradnicePrutu)

    def getUzlyASouradnice(self):
        return(self.uzlyAJejichSouradnice)

    def getSouradniceVsechTrojuhelniku(self):
        return(self.souradniceVsechTrojuhelniku)

    def getUzlyTrojuhelnika(self):
        return (self.uzlyTrojuhelnika)

    def getDomena(self):
        return(self.obsahDomeny)

    def getCislaUzluZacatekAKonecKonecElementu(self):
        return(self.cislaUzluZacatekAKonecKonecElementu)


    # data ziskane z tridy podpory
    def getPodporyKloubovePosuvneVodorovne(self):
        return (self.podporyKloubovePosuvneVodorovne)

    def getPodporyKloubovePosuvneSvisle(self):
        return (self.podporyKloubovePosuvneSvisle)

    def getPodporyVetknute(self):
        return (self.podporyVetknute)



    # vraci zatizeni
    def getSiloveZatizeniNaPrutech(self):
        return(self.siloveZatizeniNaPrutech)

    def getZatizeniTeplotouHorniVlakna(self):
        return(self.zatizeniTeplotouHorniVlakna)

    def getZatizeniTeplotouDolniVlakna(self):
        return(self.zatizeniTeplotouDolniVlakna)

    def getVynuceneZatizeniPodpor(self):
        return(self.vynuceneZatizeniPodpor)

    def getSilyAJejichSouradnice(self):
        return(self.silyAJejichSouradniceOFT)



    # vrati typ domeny, aby vedel, jake data ma vyhledavat
    def zjistiDomenu(self, poleRadkuIn):

        indexRadku = -1
        obsahDomeny = ""

        for i in range(0, len(poleRadkuIn)):
            radek = poleRadkuIn[i]
            try:
                radek.index('domain')
            except ValueError:
                neprovedeNic = -1
            else:
                obsahDomeny = poleRadkuIn[i]
                obsahDomeny = obsahDomeny.replace("\n", "")
                obsahDomeny = obsahDomeny.replace("domain ", "")
                break

        return (obsahDomeny)





