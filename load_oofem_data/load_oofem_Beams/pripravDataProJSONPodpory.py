

class dataProJSONPodpory:

    def __init__(self, podporyKloubovePosuvneVodorovne, podporyKloubovePosuvneSvisle, podporyVetknute, MeritkoKCE):

        self.podporyKloubovePosuvneVodorovne = podporyKloubovePosuvneVodorovne
        self.podporyKloubovePosuvneSvisle = podporyKloubovePosuvneSvisle
        self.podporyVetknute = podporyVetknute
        self.MeritkoKCE = MeritkoKCE

        svislyPrutPosun = self.vratPoleRadkuPodpory(self.podporyKloubovePosuvneVodorovne, "kloubPosun", "podporaDolu")
        svislyPrutVetknuti = self.vratPoleRadkuPodpory(self.podporyVetknute, "vetknuti", "podporaDolu")

        vodorovnyPrutPosun = self.vratPoleRadkuPodpory(self.podporyKloubovePosuvneSvisle, "kloubPosun", "podporaZleva")
        vodorovnyPrutVetknuti = self.vratPoleRadkuPodpory(self.podporyVetknute, "vetknuti", "podporaZleva")

        self.svislyPrutJSON = svislyPrutPosun + svislyPrutVetknuti
        self.vodorovnyPrutJSON = vodorovnyPrutPosun + vodorovnyPrutVetknuti

        # dopise carky na konce radku
        self.svislyPrutJSON = self.dodatecneDopisCarkuNaKonecRadku(self.svislyPrutJSON)
        self.vodorovnyPrutJSON = self.dodatecneDopisCarkuNaKonecRadku(self.vodorovnyPrutJSON)



    def getSvislyPrutJSON(self):
        return(self.svislyPrutJSON)

    def getvodorovnyPrutJSON(self):
        return(self.vodorovnyPrutJSON)



    def vratPoleRadkuPodpory(self, podporyData, typ, podporaSmerKlic):

        poleRadkuJSONPodpory = []

        poleSouradnic = self.ziskejPoleSouradnic(podporyData)
        for i in range(0, len(poleSouradnic)):
            souradnice = poleSouradnic[i]
            Ax = souradnice[0] * self.MeritkoKCE
            Ay = souradnice[1] * self.MeritkoKCE

            radekPodpora = self.vratRadekPodporyJSOn(Ax, Ay, typ, podporaSmerKlic)
            poleRadkuJSONPodpory.append(radekPodpora)

        return(poleRadkuJSONPodpory)


    # dodatecne dopisuje data, protoze sklada dohromady dve pole a neni jasny posledni radek
    def dodatecneDopisCarkuNaKonecRadku(self, poleRadkuJSONPodpory):

        poleRadkuJSONPodporyNew = []

        for i in range(0, len(poleRadkuJSONPodpory)):
            radekJSON = poleRadkuJSONPodpory[i]

            if (i < len(poleRadkuJSONPodpory) - 1):
                radekJSON = radekJSON + ',\''
            else:
                radekJSON = radekJSON + '\''

            poleRadkuJSONPodporyNew.append(radekJSON)

        return(poleRadkuJSONPodporyNew)




    def vratRadekPodporyJSOn(self, Ax, Ay, typ, podporaSmerKlic):

        velikost = 15
        #typ = "vetknuti"
        #podporaSmerKlic = "podporaZleva"
        barvaCary = "darkcyan"
        tloustkaCary = 2

        radekPodpora = '\'       {"Ax":' + str(Ax) + ',"Ay":' + str(Ay) + ',"velikost":' + str(velikost) + ',"typ":"' + typ + '","' + podporaSmerKlic + '":true,"barvaCary":"' + barvaCary + '","tloustkaCary":"' + str(tloustkaCary) + '"}'

        return(radekPodpora)


    # ziska poleSouradnic, jelikoz pole je zatim nadbytecne vnorene
    def ziskejPoleSouradnic(self, pole):

        souradnicePole = []

        if(len(pole) > 0):
            pole0 = pole[0]
            for i in range(0, len(pole0)):
                souradnice = pole0[i]
                souradnicePole.append(souradnice)

        return(souradnicePole)