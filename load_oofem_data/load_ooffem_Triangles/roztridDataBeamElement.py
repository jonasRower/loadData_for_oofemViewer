
# roztridi data BeamElement
class beamElement:

    def __init__(self, poleRadkuBeamElement):
        self.poleRadkuBeamElement = poleRadkuBeamElement

        self.poleRadkuLocalDisplacement = self.roztridPodleSubsringu(self.poleRadkuBeamElement, "local displacements")
        self.poleRadkuLocalEndForces = self.roztridPodleSubsringu(self.poleRadkuBeamElement, "local end forces")
        self.poleRadkuStrains = self.roztridPodleSubsringu(self.poleRadkuBeamElement, "strains")
        self.poleRadkuStresses = self.roztridPodleSubsringu(self.poleRadkuBeamElement, "stresses")

        self.vektoryLocalDisplacement = self.vytvorPoleVektoru(self.poleRadkuLocalDisplacement, "displacements")
        self.vektoryLocalEndForces = self.vytvorPoleVektoru(self.poleRadkuLocalEndForces, "forces")
        self.vektoryStrains = self.vytvorPoleVektoru(self.poleRadkuStrains, "strains")
        self.vektoryStresses = self.vytvorPoleVektoru(self.poleRadkuStresses, "stresses")


    def getLocalDisplacements(self):
        return(self.vektoryLocalDisplacement)

    def getLocalForces(self):
        return(self.vektoryLocalEndForces)

    def getStrains(self):
        return(self.vektoryStrains)

    def getStresses(self):
        return(self.vektoryStresses)



    def roztridPodleSubsringu(self, poleRadku, substring):

        radkyObsahujiciSubstring = []

        for r in range(0, len(poleRadku)):
            radek = poleRadku[r]
            obsahujeSubstring = self.detekujZdaRadekObsahujeSubstring(radek, substring)
            if(obsahujeSubstring):
                radkyObsahujiciSubstring.append(radek)

        return(radkyObsahujiciSubstring)


    def detekujZdaRadekObsahujeSubstring(self, radek, substring):

        indexSubStringu = radek.find(substring)
        if (indexSubStringu > -1):
            obsahujeSubstring = True
        else:
            obsahujeSubstring = False

        return (obsahujeSubstring)


    # poleRozlozenyRadek jakozto vektor seskupi do pole
    def vytvorPoleVektoru(self, poleRadkuVelicina, klicoveSlovo):

        poleVektoruVelicina = []

        for i in range(0, len(poleRadkuVelicina)):
            radekVelicina = poleRadkuVelicina[i]
            vektorVelicina = self.rozlozRadekDoPole(radekVelicina, klicoveSlovo)

        return(vektorVelicina)


    # polozky za klicovym slovem ulozi do pole
    def rozlozRadekDoPole(self, radek, klicoveSlovo):

        poleRozlozenyRadek = []
        zapisovatDoPole = False
        wordArr = radek.split()

        for i in range(0, len(wordArr)):
            slovo = wordArr[i]

            #pokud je zapisovatDoPole == True pak zapisuje do pole
            if(zapisovatDoPole == True):
                poleRozlozenyRadek.append(slovo)

            # nalezne-li slovo == klicoveSlovo, pak v nasledujicim cyklu vytvari pole
            if(slovo == klicoveSlovo):
                zapisovatDoPole = True

        return(poleRozlozenyRadek)