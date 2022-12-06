
import vratPoleSekci
import roztridDataBeamElement
import roztridDofManagerOutput

class vytvorSekce:

    def __init__(self, poleRadku):

        # nastaveni - hledat data v "DofManager output:" nebo "Element output:"
        self.HledatVDofManager = True
        self.poleTime = []  # ziska data pro vystup - jednotlive casy, ktere budou urcovat nazvy Jsonu

        self.poleRadku = poleRadku
        self.sekceBeamElementRadky = self.vytvorSekceRadkyBeamElement(poleRadku, self.HledatVDofManager)

        self.nodalDisplacements = []
        self.sekceBeamLocalDisplacements = []
        self.sekceBeamLocalForces = []
        self.sekceBeamStrains = []
        self.sekceBeamstresses = []


        if(self.HledatVDofManager == True):
            for OFT in range(0, len(self.sekceBeamElementRadky)):
                sekceBeamElementRadkyOFT = self.sekceBeamElementRadky[OFT]
                dofManagerOutput = roztridDofManagerOutput.dofManager(sekceBeamElementRadkyOFT)
                uzelDofDeformacePoleProJedenOFT = dofManagerOutput.getUzelDofDeformacePoleProJedenOFT()

                self.nodalDisplacements.append(uzelDofDeformacePoleProJedenOFT)
        else:
            self.sekceBeamLocalDisplacements = self.priradVelicinuKBeamElement(self.sekceBeamElementRadky, "local displacements")
            self.sekceBeamLocalForces = self.priradVelicinuKBeamElement(self.sekceBeamElementRadky, "local end forces")
            self.sekceBeamStrains = self.priradVelicinuKBeamElement(self.sekceBeamElementRadky, "strains")
            self.sekceBeamstresses = self.priradVelicinuKBeamElement(self.sekceBeamElementRadky, "stresses")


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

            if(HledatVDofManager == True):
                dofManagerOutput = vratPoleSekci.poleSekci(jednaSekceOutputForTime, "DofManager output:", "Element output:")
                vsechnySekceDofManagerOutput = dofManagerOutput.getPoleSekci()

                # malezne-li "DofManager output", pokracuje tudy
                for N in range(0, len(vsechnySekceDofManagerOutput)):
                    jednaSekceDofManagerOutput = vsechnySekceDofManagerOutput[N]
                    dataNode = vratPoleSekci.poleSekci(jednaSekceDofManagerOutput, "Node", "Node")
                    vsechnySekceNode = dataNode.getPoleSekci()

                    vsechnySubSekceOutputForTime.append(vsechnySekceNode)
            else:
                dataElementOutput = vratPoleSekci.poleSekci(jednaSekceOutputForTime, "Element output:", "R E A C T I O N S  O U T P U T:")
                vsechnySekceElementOutput = dataElementOutput.getPoleSekci()

                # nalezne-li "Element output", pokracuje tudy
                for EO in range(0, len(vsechnySekceElementOutput)):
                    jednaSekceElementOutput = vsechnySekceElementOutput[EO]
                    dataBeamElement = vratPoleSekci.poleSekci(jednaSekceElementOutput, "beam element", "beam element")
                    vsechnySekceBeamElement = dataBeamElement.getPoleSekci()

                    vsechnySubSekceOutputForTime.append(vsechnySekceBeamElement)


        return(vsechnySubSekceOutputForTime)


    #def vytvorSekceRadkyDofManagerOutput(self, poleRadku):

    #dofManagerOutput =