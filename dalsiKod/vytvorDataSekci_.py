
import vratPoleSekci
import roztridDataBeamElement

class vytvorSekce:

    def __init__(self, poleRadku):

        self.poleRadku = poleRadku
        self.sekceBeamElementRadky = self.vytvorSekceRadkyBeamElement(poleRadku)
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



    def vytvorSekceRadkyBeamElement(self, poleRadku):

        dataOutputForTime = vratPoleSekci.poleSekci(poleRadku, "Output for time", "Output for time")
        vsechnySekceOutputForTime = dataOutputForTime.getPoleSekci()
        vsechnySubSekceOutputForTime = []

        for OFT in range(0, len(vsechnySekceOutputForTime)):
            jednaSekceOutputForTime = vsechnySekceOutputForTime[OFT]
            dataElementOutput = vratPoleSekci.poleSekci(jednaSekceOutputForTime, "Element output:", "R E A C T I O N S  O U T P U T:")
            vsechnySekceElementOutput = dataElementOutput.getPoleSekci()

            vsechnySubSekceElementOutput = []

            for EO in range(0, len(vsechnySekceElementOutput)):
                jednaSekceElementOutput = vsechnySekceElementOutput[EO]
                dataBeamElement = vratPoleSekci.poleSekci(jednaSekceElementOutput, "beam element", "beam element")
                vsechnySekceBeamElement = dataBeamElement.getPoleSekci()

                vsechnySubSekceOutputForTime.append(vsechnySekceBeamElement)


        return(vsechnySubSekceOutputForTime)