
class poleSekci:

    def __init__(self, poleRadku, substring1, substring2):

        self.substring1 = substring1
        self.substring2 = substring2

        self.poleRadku = poleRadku
        self.poleSekci = self.vytvorPoleSekciProSubString(self.poleRadku, self.substring1, self.substring2)
        self.poleTime = self.vratPoleTime(self.poleSekci)

    def getPoleSekci(self):
        return(self.poleSekci)

    def getPoleTime(self):
        return(self.poleTime)


    def vratPoleTime(self, poleSekci):

        poleTime = []

        for i in range(0, len(poleSekci)):
            outputForTimeRadky = poleSekci[i]
            outputForTimePrvniRadek = outputForTimeRadky[0]
            poleTimeHodnota = outputForTimePrvniRadek.replace("Output for time ","")
            poleTimeHodnota = poleTimeHodnota.replace(".", "_")
            poleTimeHodnota = poleTimeHodnota.replace(" ", "")
            poleTimeHodnota = poleTimeHodnota.replace("\n", "")
            poleTime.append(poleTimeHodnota)

        return(poleTime)


    # vytvori pole sekci pro "Output for time"
    def vytvorPoleSekciProSubString(self, poleRadku, subString1, subString2):

        poleSekciSubStringu = []

        for i in range(0, len(poleRadku)):
            sekce = []
            sekce = self.vratSekciProSubString(poleRadku, subString1, subString2, i)

            if(len(sekce) == 0):
                break

            poleSekciSubStringu.append(sekce)

        return(poleSekciSubStringu)


    # najde prvni a posledni radek sekce
    def vratSekciProSubString(self, poleRadku, subString1, subString2, poradi):

        if(subString1 == subString2):
            poradi1 = poradi
            poradi2 = poradi + 1
        else:
            poradi1 = poradi
            poradi2 = poradi

        prvniRadekSekce = self.vratIndexRadkuPodleSubStringu(poleRadku, subString1, 0, poradi1)
        posledniRadekSekce = self.vratIndexRadkuPodleSubStringu(poleRadku, subString2, -1, poradi2)

        # nenajde-li posledni radek, prepise ho indexem konce pole
        if (subString1 == subString2):
            if(prvniRadekSekce > -1 ):
                if(posledniRadekSekce == -1):
                    posledniRadekSekce = len(poleRadku)-1

        sekce = []
        if(prvniRadekSekce > -1):
            if(posledniRadekSekce > -1):
                sekce = self.ziskejSekciPoleRadku(poleRadku, prvniRadekSekce, posledniRadekSekce)

        return(sekce)


    # vrati index radku, ktery obsahuje dany substring
    # parametr pocetRadkuOkolo rika jaky ma vratit radek, zda o dany pocet radku vyse ( < 0 ), ci nize ( > 0 )
    # parametr poradi udava kolikaty substring v poleRadku od shora vybira

    def vratIndexRadkuPodleSubStringu(self, poleRadku, subString, pocetRadkuOkolo, poradiExp):

        poradi = -1
        indexRadku = -1

        for r in range(0, len(poleRadku)):
            radek = poleRadku[r]
            obsahujeSubstring = self.detekujZdaRadekObsahujeSubstring(radek, subString)
            if(obsahujeSubstring == True):
                poradi = poradi + 1

                # pokud nalezne pozadovane poradi, pak ukonci vyhledavani
                if(poradi == poradiExp):
                    indexRadku = r + pocetRadkuOkolo  #posune o pozadovany pocet radku nahoru/dolu
                    break

        return(indexRadku)


    def detekujZdaRadekObsahujeSubstring(self, radek, substring):

        indexSubStringu = radek.find(substring)
        if(indexSubStringu > -1):
            obsahujeSubstring = True
        else:
            obsahujeSubstring = False

        return(obsahujeSubstring)



    # vycleni pole radku mezi jednotlivymi radky
    def ziskejSekciPoleRadku(self, poleRadku, prvniRadekIndex, posledniRadekIndex):

        poleRadkuSekce = []
        posledniRadekObsah = poleRadku[posledniRadekIndex]
        if(posledniRadekObsah != ""):
            posledniRadekIndex = posledniRadekIndex + 1

        for r in range(prvniRadekIndex, posledniRadekIndex):
            radek = poleRadku[r]
            poleRadkuSekce.append(radek)

        return(poleRadkuSekce)


