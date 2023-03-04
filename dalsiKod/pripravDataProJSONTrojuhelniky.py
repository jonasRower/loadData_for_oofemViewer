
class dataProJSON:

    def __init__(self, souradniceVsechTrojuhelniku, uzlyTrojuhelnika, HSLHodnoty, NodalDisplacements, prumerneHodnoty):

        self.meritko = 100
        self.souradniceVsechTrojuhelniku = souradniceVsechTrojuhelniku
        self.uzlyTrojuhelnika = uzlyTrojuhelnika
        self.HSLHodnoty = HSLHodnoty
        self.NodalDisplacements = NodalDisplacements
        self.prumerneHodnoty = prumerneHodnoty

        self.souradniceVsechTrojuhelnikuMeritko = self.prepocitejMeritko(self.souradniceVsechTrojuhelniku, self.meritko)
        self.JSONdataRadky = self.generujJSONdata(HSLHodnoty, self.NodalDisplacements, self.prumerneHodnoty, self.souradniceVsechTrojuhelnikuMeritko)
        self.DOFs = self.ziskejPoleVsechDOF(self.NodalDisplacements)

    def getJSONdataRadky(self):
        return(self.JSONdataRadky)

    def getDofs(self):
        return(self.DOFs)


    def generujJSONdata(self, HSLHodnoty, NodalDisplacements, prumerneHodnoty, souradniceVsechTrojuhelnikuMeritko):

        poleRadkuJSONProdaneDOF = []
        vsechnyPoleRadkuJSON = []

        for iDof in range(0, len(HSLHodnoty)):
            HSLDof = HSLHodnoty[iDof]
            prumerneHodnotyDof = prumerneHodnoty[iDof]
            poleRadkuJSONProdanyElement = []

            for OFT in range(0, len(HSLDof[0])):
                poleRadkuJSONProdanyOFT = []

                for iElement in range(0, len(HSLDof)):
                    #souradnice = self.souradniceVsechTrojuhelniku[iElement]    # bez meritka
                    souradnice = souradniceVsechTrojuhelnikuMeritko[iElement]   # s meritkem
                    cisloElementu = iElement
                    OznaceniVrcholu = self.uzlyTrojuhelnika[iElement]
                    hodnotyVrcholu = self.vratHodnotyVrcholuProOznaceniVrcholu(NodalDisplacements, OznaceniVrcholu, iDof, OFT)

                    radekJSON = self.vratJSONradekProElementAOFT(HSLDof, cisloElementu, OFT, souradnice, cisloElementu, OznaceniVrcholu, hodnotyVrcholu, prumerneHodnotyDof)
                    if (iElement < len(HSLDof) - 1):
                        radekJSON = radekJSON + '},\''
                    else:
                        radekJSON = radekJSON + '}\''

                    poleRadkuJSONProdanyOFT.append(radekJSON)

                poleRadkuJSONProdanyElement.append(poleRadkuJSONProdanyOFT)

            poleRadkuJSONProdaneDOF.append(poleRadkuJSONProdanyElement)

        vsechnyPoleRadkuJSON.append(poleRadkuJSONProdaneDOF)

        return(vsechnyPoleRadkuJSON)


    def vratHodnotyVrcholuProOznaceniVrcholu(self, NodalDisplacements, OznaceniVrcholuPole, DofExpIndex, OFT):

        hodnotyVrcholu = []

        for i in range(0, len(OznaceniVrcholuPole)):
            oznaceniVrcholu = OznaceniVrcholuPole[i]
            uzelDofADisplacement = self.vratNodalDisplacementProDanyDOFUzelAOFT(NodalDisplacements, DofExpIndex, oznaceniVrcholu, OFT)
            displacement = uzelDofADisplacement[2]
            hodnotyVrcholu.append(displacement)

        return(hodnotyVrcholu)


    def vratNodalDisplacementProDanyDOFUzelAOFT(self, NodalDisplacements, DofExpIndex, uzelExp, OFT):

        NodalDisplacementsOFT = NodalDisplacements[OFT]

        for iUz in range(0, len(NodalDisplacementsOFT)):
            uzelRadek = NodalDisplacementsOFT[iUz]
            cisloUzlu = uzelRadek[0]

            if (cisloUzlu == uzelExp):
                dofPole = uzelRadek[1]
                displacementPole = uzelRadek[2]

                cisloDof = dofPole[DofExpIndex]
                displacement = displacementPole[DofExpIndex]

                uzelDofADisplacement = []
                uzelDofADisplacement.append(cisloUzlu)
                uzelDofADisplacement.append(cisloDof)
                uzelDofADisplacement.append(displacement)

                break

        return (uzelDofADisplacement)


    def vratJSONradekProElementAOFT(self, HSLDof, element, OFT, souradnice, cisloElementu, OznaceniVrcholu, hodnotyVrcholu, prumerneHodnotyDof):

        barvaElementu = self.vratHslHodnotuProDanyElementAOFT(HSLDof, element, OFT)
        hodnotaNaElementu = self.vratHslHodnotuProDanyElementAOFT(prumerneHodnotyDof, element, OFT) # jelikoz se jedna o stejnou strukturu dat, vyuzivam funkci pro HSL
        barvaHSLKod = 'hsl(' + str(barvaElementu) + ', 100%, 50%)'
        radekJSON = '        \'{"Souradnice":' + str(souradnice) + ',"cisloElementu":' + str(cisloElementu) + ',"barva":"' + barvaHSLKod + '","OznaceniVrcholu":' + str(OznaceniVrcholu) + ',"HodnotyVrcholu":' + str(hodnotyVrcholu) + ',"HodnotaElementu":' + str(hodnotaNaElementu) + ',"BarvaCaryElementu":"black","tloustkaCaryElementu":"1"'

        return(radekJSON)


    def vratHslHodnotuProDanyElementAOFT(self, HSLDof, element, OFT):

        HSLelement = HSLDof[element]
        HSLOFT = HSLelement[OFT]

        return(HSLOFT)


    def vratHSLHodnotuProDanyOFT(self, HSLUzel, OFT):
        HSLHodnota = HSLUzel[OFT]

        return(HSLHodnota)


    def vratHSLproDOFUzelAOFT(self, HSLHodnoty, Dof, uzel, OFT):

        HSLHodnotyDof = HSLHodnoty[Dof]
        HSLHodnotyUzel = HSLHodnotyDof[uzel]
        HSLHodnotaOFT = HSLHodnotyUzel[OFT]

        return(HSLHodnotaOFT)


    # vynasobi souradnice meritkem
    def prepocitejMeritko(self, souradniceVsechTrojuhelniku, meritko):

        souradniceTrojuhelnikMeritko = []

        for i in range(0, len(self.souradniceVsechTrojuhelniku)):
            souradniceTrojuhelnik = souradniceVsechTrojuhelniku[i]
            souradniceUzelMeritko = []

            for sour in range(0, len(souradniceTrojuhelnik)):
                souradniceUzel = souradniceTrojuhelnik[sour]

                uzelX = souradniceUzel[0]
                uzelY = souradniceUzel[1]
                uzelZ = souradniceUzel[2]

                # prenasobi meritkem
                uzelXMeritko = uzelX * meritko
                uzelYMeritko = uzelY * meritko
                uzelZMeritko = uzelZ * meritko

                # slozi data do puvodni struktury
                UzelMeritko = []
                UzelMeritko.append(uzelXMeritko)
                UzelMeritko.append(uzelYMeritko)
                UzelMeritko.append(uzelZMeritko)

                souradniceUzelMeritko.append(UzelMeritko)

            souradniceTrojuhelnikMeritko.append(souradniceUzelMeritko)

        return(souradniceTrojuhelnikMeritko)


    #ziska pole vsech DOF, tak, aby je mohl zapsat jako nazvy slozek
    def ziskejPoleVsechDOF(self, nodalDisplacements):

        # zatim uvazuje dof pouze z 1. radku
        nodalDisplacementPrvniRadek = nodalDisplacements[0]
        nodalDisplacementPrvniRadek = nodalDisplacementPrvniRadek[0]
        DOFS = nodalDisplacementPrvniRadek[1]

        return(DOFS)


    def ziskejPoleRadkuKCE(self, souradniceVsechTrojuhelnikuMeritko, uzlyTrojuhelnika, HSLHodnota):

        poleRadkuKCEJSON = []

        for i in range(0, len(souradniceVsechTrojuhelnikuMeritko)):
            souradnice = souradniceVsechTrojuhelnikuMeritko[i]
            uzly = str(uzlyTrojuhelnika[i])

            radekJSON = '        \'{"Souradnice":' + str(souradnice) + ',"cisloElementu":' + str(i) + ',"barva":"red","OznaceniVrcholu":' + uzly

            if(i < len(souradniceVsechTrojuhelnikuMeritko)-1):
                radekJSON = radekJSON + '},\''
            else:
                radekJSON = radekJSON + '}\''

            poleRadkuKCEJSON.append(radekJSON)

        return(poleRadkuKCEJSON)




