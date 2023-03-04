
import vratPoleSekci
import roztridDataBeamElement
import roztridDofManagerOutput
import vytvorDataSekciReactions

class vytvorSekce:

    def __init__(self, poleRadku):

        # nastaveni - hledat data v "DofManager output:" nebo "Element output:"
        self.HledatVDofManager = False
        self.poleTime = []  # ziska data pro vystup - jednotlive casy, ktere budou urcovat nazvy Jsonu
        self.sekceReactionsOutput = []
        self.poleDof = []

        self.poleRadku = poleRadku
        self.sekceBeamElementRadky = self.vytvorSekceRadkyBeamElement(poleRadku, self.HledatVDofManager)
        self.sekceDofManager = self.vytvorSekceRadkyDofManager(poleRadku, self.HledatVDofManager)



        self.nodalDisplacements = []
        self.sekceBeamLocalDisplacements = []
        self.sekceBeamLocalForces = []
        self.sekceBeamStrains = []
        self.sekceBeamstresses = []
        self.reactionsOutput = []


        #ziska nodal displacement z dat dof manageru
        for OFT in range(0, len(self.sekceDofManager)):
            sekceBeamElementRadkyOFT = self.sekceDofManager[OFT]
            dofManagerOutput = roztridDofManagerOutput.dofManager(sekceBeamElementRadkyOFT)
            uzelDofDeformacePoleProJedenOFT = dofManagerOutput.getUzelDofDeformacePoleProJedenOFT()

            self.nodalDisplacements.append(uzelDofDeformacePoleProJedenOFT)


        self.sekceBeamLocalDisplacements = self.priradVelicinuKBeamElement(self.sekceBeamElementRadky, "local displacements")
        self.sekceBeamLocalForces = self.priradVelicinuKBeamElement(self.sekceBeamElementRadky, "local end forces")
        self.sekceBeamStrains = self.priradVelicinuKBeamElement(self.sekceBeamElementRadky, "strains")
        self.sekceBeamstresses = self.priradVelicinuKBeamElement(self.sekceBeamElementRadky, "stresses")

        # ziska poleDof z posledni instance "dofManagerOutput", jelikoz se predpoklada, ze pro vsechny instance jsou data DOF stejna
        self.poleDof = dofManagerOutput.getDOF()


        # usporada data pro reakce (self.sekceReactionsOutput je ziskavana v metode "self.sekceBeamElementRadky")
        self.reactionsOutput = self.vytvorSekceReactions(self.sekceReactionsOutput, self.poleDof)



    # getry
    def getLocalDisplacements(self):
        return(self.sekceBeamLocalDisplacements)

    def getLocalForces(self):
        return(self.sekceBeamLocalForces)

    def getStrains(self):
        return(self.sekceBeamStrains)

    def getStresses(self):
        return(self.sekceBeamstresses)

    def getNodalDisplacements(self):
        return(self.nodalDisplacements)

    def getPoleTime(self):
        return (self.poleTime)

    def getReactionsOutput(self):
        return(self.reactionsOutput)


    def priradVelicinuKBeamElement(self, sekceBeamElementData, velicina):

        outputForTimeNew = []
        for OFT in range(0, len(sekceBeamElementData)):
            outputForTime = sekceBeamElementData[OFT]
            BeamElementDataNew = []

            for BE in range(0, len(outputForTime)):
                BeamElementData = outputForTime[BE]
                BeamElementVelicina = roztridDataBeamElement.beamElement(BeamElementData)

                if(velicina == "local displacements"):
                    BeamElementLocalDisplacements = BeamElementVelicina.getLocalDisplacements()
                    BeamElementDataNew.append(BeamElementLocalDisplacements)

                if(velicina == "local end forces"):
                    BeamElementLocalForces = BeamElementVelicina.getLocalForces()
                    BeamElementDataNew.append(BeamElementLocalForces)

                if (velicina == "strains"):
                    BeamElementStrains = BeamElementVelicina.getStrains()
                    BeamElementDataNew.append(BeamElementStrains)

                if (velicina == "stresses"):
                    BeamElementStresses = BeamElementVelicina.getStresses()
                    BeamElementDataNew.append(BeamElementStresses)

            outputForTimeNew.append(BeamElementDataNew)

        return(outputForTimeNew)


    def vytvorSekceRadkyBeamElement(self, poleRadku, HledatVDofManager):

        dataOutputForTime = vratPoleSekci.poleSekci(poleRadku, "Output for time", "Output for time")
        vsechnySekceOutputForTime = dataOutputForTime.getPoleSekci()

        # vrati casy pro vytvoreni nazvu souboru JSON
        self.poleTime = dataOutputForTime.getPoleTime()

        vsechnySubSekceOutputForTime = []

        for OFT in range(0, len(vsechnySekceOutputForTime)):
            jednaSekceOutputForTime = vsechnySekceOutputForTime[OFT]
            vsechnySubSekceElementOutput = []


            dataElementOutput = vratPoleSekci.poleSekci(jednaSekceOutputForTime, "Element output:", "R E A C T I O N S  O U T P U T:")
            dataReactionsOutput = vratPoleSekci.poleSekci(jednaSekceOutputForTime, "R E A C T I O N S  O U T P U T:", "User time consumed by solution step")

            vsechnySekceElementOutput = dataElementOutput.getPoleSekci()
            sekceReactionsOutput = dataReactionsOutput.getPoleSekci()

            #vrati sekceReactionsOutput pripsanim do self.sekceReactionsOutput
            self.sekceReactionsOutput.append(sekceReactionsOutput)

            # nalezne-li "Element output", pokracuje tudy
            for EO in range(0, len(vsechnySekceElementOutput)):
                jednaSekceElementOutput = vsechnySekceElementOutput[EO]
                dataBeamElement = vratPoleSekci.poleSekci(jednaSekceElementOutput, "beam element", "beam element")
                vsechnySekceBeamElement = dataBeamElement.getPoleSekci()

                vsechnySubSekceOutputForTime.append(vsechnySekceBeamElement)


        return(vsechnySubSekceOutputForTime)



    def vytvorSekceRadkyDofManager(self, poleRadku, HledatVDofManager):

        dataOutputForTime = vratPoleSekci.poleSekci(poleRadku, "Output for time", "Output for time")
        vsechnySekceOutputForTime = dataOutputForTime.getPoleSekci()

        # vrati casy pro vytvoreni nazvu souboru JSON
        self.poleTime = dataOutputForTime.getPoleTime()

        vsechnySubSekceOutputForTime = []

        for OFT in range(0, len(vsechnySekceOutputForTime)):
            jednaSekceOutputForTime = vsechnySekceOutputForTime[OFT]
            vsechnySubSekceElementOutput = []


            dofManagerOutput = vratPoleSekci.poleSekci(jednaSekceOutputForTime, "DofManager output:", "Element output:")
            vsechnySekceDofManagerOutput = dofManagerOutput.getPoleSekci()

            # malezne-li "DofManager output", pokracuje tudy
            for N in range(0, len(vsechnySekceDofManagerOutput)):
                jednaSekceDofManagerOutput = vsechnySekceDofManagerOutput[N]
                dataNode = vratPoleSekci.poleSekci(jednaSekceDofManagerOutput, "Node", "Node")
                vsechnySekceNode = dataNode.getPoleSekci()

                vsechnySubSekceOutputForTime.append(vsechnySekceNode)

        return (vsechnySubSekceOutputForTime)


    def vytvorSekceReactions(self, sekceReactionsOutput, poleDOF):

        # aby se nemichal kod, reakce se usporadavaji ve vlastni tride
        usporadaniReakci = vytvorDataSekciReactions.vytvorSekceReactions(sekceReactionsOutput, self.poleDof)
        reactionsOutput = usporadaniReakci.getDataReakce()

        return(reactionsOutput)