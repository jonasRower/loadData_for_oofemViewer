

class dataProJSONsipky:

    def __init__(self, silyAJejichSouradnice, MeritkoKCE, poleTime, nazevJSON, Dofs):

        self.silyAJejichSouradnice = silyAJejichSouradnice
        self.MeritkoKCE = MeritkoKCE
        self.delkaSipky = 100
        self.delkaOblouku = 0.5
        self.poleTime = poleTime
        self.nazevJSON = nazevJSON
        self.Dofs = Dofs


        #self.dataJSONVsechnaOFT = self.pripravDataProVsechnaOFT(self.silyAJejichSouradnice, self.MeritkoKCE, self.delkaSipky, self.delkaOblouku)
        self.dataJSONVsechnaOFT = self.pripravDataProVsechnaOFT(self.silyAJejichSouradnice, self.MeritkoKCE, self.delkaSipky, self.delkaOblouku)

    def getSilyJSON(self):
        return(self.dataJSONVsechnaOFT)


    def pripravDataProVsechnaOFT(self, silyAJejichSouradniceVsechnaOFT, MeritkoKCE, delkaSipky, delkaOblouku):

        dataJSONVsechnaOFT = []

        radkySipkyVodorovneVsechnyOFT = self.pripravDataProSipkyOFT(silyAJejichSouradniceVsechnaOFT, MeritkoKCE, delkaSipky, delkaOblouku, 0)
        radkySipkySvisleVsechnyOFT = self.pripravDataProSipkyOFT(silyAJejichSouradniceVsechnaOFT, MeritkoKCE, delkaSipky, delkaOblouku, 1)
        radkySipkyObloukoveVsechnyOFT = self.pripravDataProSipkyOFT(silyAJejichSouradniceVsechnaOFT, MeritkoKCE, delkaSipky, delkaOblouku, 2)

        dataJSONVsechnaOFT.append(radkySipkyVodorovneVsechnyOFT)
        dataJSONVsechnaOFT.append(radkySipkySvisleVsechnyOFT)
        dataJSONVsechnaOFT.append(radkySipkyObloukoveVsechnyOFT)

        return(dataJSONVsechnaOFT)


    def pripravDataProSipkyOFT(self, silyAJejichSouradniceVsechnaOFT, MeritkoKCE, delkaSipky, delkaOblouku, indexData):

        radkySipkyOFT = []

        for OFT in range(0, len(silyAJejichSouradniceVsechnaOFT)):
            if(len(silyAJejichSouradniceVsechnaOFT) > 1):
                time = "_" + self.poleTime[OFT]
            else:
                time = ""

            time = time.replace('+', 'p')
            time = time.replace('-', 'm')

            silyAJejichSouradniceJedenOFT = silyAJejichSouradniceVsechnaOFT[OFT]

            souradniceASlozkyPole = self.vratPoleSouradniceSipkyAPopisu(silyAJejichSouradniceJedenOFT, MeritkoKCE)
            PoleSipkyFxFyM = self.ziskejPoleSipkyFxFyM(souradniceASlozkyPole, delkaSipky, delkaOblouku)

            radkySipky = PoleSipkyFxFyM[indexData]
            dof = self.Dofs[indexData]
            if(indexData < 2):      # generuje sipky vodorovne nebo svisle      - bylo by dobre nekdy v budoucnu urcit kde zobrazovat text
                sipkyTelo = self.vytvorPoleRadkuProSipkySikmeJedenDOF(radkySipky)
                sipkyJSON = self.generujJSONSipky(sipkyTelo, True, time, dof)

            if (indexData == 2):      # generuje sipky obloukove
                sipkyTelo = self.vytvorPoleRadkuProSipkyObloukoveJedenDOF(radkySipky)
                sipkyJSON = self.generujJSONSipky(sipkyTelo, False, time, dof)

            radkySipkyOFT.append(sipkyJSON)

        return(radkySipkyOFT)


    def generujJSONSipky(self, radkySipky, zapisovatSipkySikme, time, dof):

        JSONSipkyPoleRadku = []
        nazevJSON = self.nazevJSON + "_" + str(dof) + time

        JSONSipkyPoleRadku.append(nazevJSON + ' = \'{"sipky": [\'')
        JSONSipkyPoleRadku.append('\'  {"data": {\'')
        JSONSipkyPoleRadku.append('\'     "sikmo": [\'')

        if(zapisovatSipkySikme == True):
            for iRadekSikme in range(0, len(radkySipky)):
                radekSikma = radkySipky[iRadekSikme]
                JSONSipkyPoleRadku.append(radekSikma)

        JSONSipkyPoleRadku.append('\'],\'')
        JSONSipkyPoleRadku.append('\'     "obloukove": [\'')

        if (zapisovatSipkySikme == False):
            for iRadekObloukove in range(0, len(radkySipky)):
                radekObloukova = radkySipky[iRadekObloukove]
                JSONSipkyPoleRadku.append(radekObloukova)

        JSONSipkyPoleRadku.append('\'     ]\'')
        JSONSipkyPoleRadku.append('\'  },\'')
        JSONSipkyPoleRadku.append('\'  "Ox":50,\'')
        JSONSipkyPoleRadku.append('\'  "Oy":100,\'')
        JSONSipkyPoleRadku.append('\'  "id":"test",\'')
        JSONSipkyPoleRadku.append('\'  "class":""\'')
        JSONSipkyPoleRadku.append('\'  }]\'')
        JSONSipkyPoleRadku.append('\'}\'')


        return (JSONSipkyPoleRadku)


    def vratPoleSouradniceSipkyAPopisu(self, silyAJejichSouradnice, Meritko):

        souradniceASlozkyPole = []

        for iUzel in range(0, len(silyAJejichSouradnice)):
            silyAJejichSouradniceRadek = silyAJejichSouradnice[iUzel]
            souradniceSily = silyAJejichSouradniceRadek[1]
            slozkySily = silyAJejichSouradniceRadek[2]

            X = souradniceSily[1] * Meritko
            Y = souradniceSily[2] * Meritko
            Fx = slozkySily[0]
            Fy = slozkySily[1]
            M = slozkySily[2]

            souradniceASlozkyRadek = []
            souradniceASlozkyRadek.append(X)
            souradniceASlozkyRadek.append(Y)
            souradniceASlozkyRadek.append(Fx)
            souradniceASlozkyRadek.append(Fy)
            souradniceASlozkyRadek.append(M)

            souradniceASlozkyPole.append(souradniceASlozkyRadek)

        return(souradniceASlozkyPole)


    def ziskejPoleSipkyFxFyM(self, souradniceASlozkyPole, delkaSipky, delkaOblouku):

        PoleSipkyFxFyM = []
        PoleSipkyFx = self.ziskejPoleSipkyFx(souradniceASlozkyPole, delkaSipky)
        PoleSipkyFy = self.ziskejPoleSipkyFy(souradniceASlozkyPole, delkaSipky)
        PoleSipkyM = self.ziskejPoleSipkyM(souradniceASlozkyPole, delkaOblouku)

        PoleSipkyFxFyM.append(PoleSipkyFx)
        PoleSipkyFxFyM.append(PoleSipkyFy)
        PoleSipkyFxFyM.append(PoleSipkyM)

        return(PoleSipkyFxFyM)


    def ziskejPoleSipkyFx(self, souradniceASlozkyPole, delkaSipky):

        poleSipkyFx = []

        for iUzel in range(0, len(souradniceASlozkyPole)):
            souradniceASlozkyRadek = souradniceASlozkyPole[iUzel]

            Ax = souradniceASlozkyRadek[0]
            Ay = souradniceASlozkyRadek[1]
            if(isinstance(souradniceASlozkyRadek[2], str) == False):
                Fx = float(souradniceASlozkyRadek[2])

                if(abs(Fx) > 0):
                    if(Fx > 0):
                        # jedna se o sipku doprava
                        Bx = Ax - delkaSipky
                        By = Ay

                    if(Fx < 0):
                        # jedna se o sipku doleva
                        Bx = Ax + delkaSipky
                        By = Ay

                    poleSipkyFxRadek = []
                    poleSipkyFxRadek.append(Ax)
                    poleSipkyFxRadek.append(Ay)
                    poleSipkyFxRadek.append(Bx)
                    poleSipkyFxRadek.append(By)
                    poleSipkyFxRadek.append(Fx)

                    poleSipkyFx.append(poleSipkyFxRadek)


            else:   # ne-jedna-li se o cislo, napr. FreeDOF
                Fx = souradniceASlozkyRadek[2]
                Bx = Ax + delkaSipky
                By = Ay

                poleSipkyFxRadek = []
                poleSipkyFxRadek.append(Ax)
                poleSipkyFxRadek.append(Ay)
                poleSipkyFxRadek.append(Bx)
                poleSipkyFxRadek.append(By)
                poleSipkyFxRadek.append(Fx)

                poleSipkyFx.append(poleSipkyFxRadek)

        return(poleSipkyFx)


    def ziskejPoleSipkyFy(self, souradniceASlozkyPole, delkaSipky):

        poleSipkyFy = []

        for iUzel in range(0, len(souradniceASlozkyPole)):
            souradniceASlozkyRadek = souradniceASlozkyPole[iUzel]

            Ax = souradniceASlozkyRadek[0]
            Ay = souradniceASlozkyRadek[1]
            if(isinstance(souradniceASlozkyRadek[3], str) == False):
                Fy = float(souradniceASlozkyRadek[3])

                if(abs(Fy) > 0):
                    if(Fy > 0):
                        # jedna se o sipku dolu
                        Bx = Ax
                        By = Ay - delkaSipky

                    if(Fy < 0):
                        # jedna se o sipku nahoru
                        Bx = Ax
                        By = Ay + delkaSipky

                    poleSipkyFyRadek = []
                    poleSipkyFyRadek.append(Ax)
                    poleSipkyFyRadek.append(Ay)
                    poleSipkyFyRadek.append(Bx)
                    poleSipkyFyRadek.append(By)
                    poleSipkyFyRadek.append(Fy)

                    poleSipkyFy.append(poleSipkyFyRadek)

            else:    # ne-jedna-li se o cislo, napr. FreeDOF
                Fy = souradniceASlozkyRadek[3]
                Bx = Ax
                By = Ay + delkaSipky

                poleSipkyFyRadek = []
                poleSipkyFyRadek.append(Ax)
                poleSipkyFyRadek.append(Ay)
                poleSipkyFyRadek.append(Bx)
                poleSipkyFyRadek.append(By)
                poleSipkyFyRadek.append(Fy)

                poleSipkyFy.append(poleSipkyFyRadek)


        return(poleSipkyFy)


    def ziskejPoleSipkyM(self, souradniceASlozkyPole, delkaOblouku):

        poleSipkyM = []

        for iUzel in range(0, len(souradniceASlozkyPole)):
            souradniceASlozkyRadek = souradniceASlozkyPole[iUzel]

            Ax = souradniceASlozkyRadek[0]
            Ay = souradniceASlozkyRadek[1]
            if(isinstance(souradniceASlozkyRadek[4], str) == False):
                M = float(souradniceASlozkyRadek[4])

                if(abs(M) > 0):
                    if(M > 0):
                        # jedna se o sipku proti smeru hod. rucicek
                        start = 0
                        end = start + delkaOblouku

                    if(M < 0):
                        # jedna se o sipku po smeru hod. rucicek
                        start = 0
                        end = start + delkaOblouku

                    poleSipkyMRadek = []
                    poleSipkyMRadek.append(Ax)
                    poleSipkyMRadek.append(Ay)
                    poleSipkyMRadek.append(start)
                    poleSipkyMRadek.append(end)
                    poleSipkyMRadek.append(M)

                    poleSipkyM.append(poleSipkyMRadek)

            else:    # ne-jedna-li se o cislo, napr. FreeDOF
                M = souradniceASlozkyRadek[4]
                start = 0
                end = start + delkaOblouku

                poleSipkyMRadek = []
                poleSipkyMRadek.append(Ax)
                poleSipkyMRadek.append(Ay)
                poleSipkyMRadek.append(start)
                poleSipkyMRadek.append(end)
                poleSipkyMRadek.append(M)

                poleSipkyM.append(poleSipkyMRadek)

        return(poleSipkyM)



    def vytvorPoleRadkuProSipkySikmeJedenDOF(self, poleSipkySikme):

        vsechnyRadkySipekJedenDOF = []

        for iSipka in range(0, len(poleSipkySikme)):
            poleSipkySikmeRadek = poleSipkySikme[iSipka]
            Ax = str(poleSipkySikmeRadek[0])
            Ay = str(poleSipkySikmeRadek[1])
            Bx = str(poleSipkySikmeRadek[2])
            By = str(poleSipkySikmeRadek[3])

            if (isinstance(poleSipkySikmeRadek[4], str) == False):
                text = str(abs(poleSipkySikmeRadek[4]))
            else:
                text = poleSipkySikmeRadek[4]

            radekJedneSipky = self.pripravRadkySipkySikmoJedenDOF(Ax, Ay, Bx, By, text)

            # doplni carku na konci radku
            if(iSipka < len(poleSipkySikme)-1):
                radekJedneSipky = radekJedneSipky.replace('}\'', '},\'')

            vsechnyRadkySipekJedenDOF.append(radekJedneSipky)

        return(vsechnyRadkySipekJedenDOF)


    def vytvorPoleRadkuProSipkyObloukoveJedenDOF(self, poleSipkyObloukove):

        vsechnyRadkySipekJedenDOF = []

        for iSipka in range(0, len(poleSipkyObloukove)):
            poleSipkyObloukoveRadek = poleSipkyObloukove[iSipka]
            Ax = str(poleSipkyObloukoveRadek[0])
            Ay = str(poleSipkyObloukoveRadek[1])
            start = str(poleSipkyObloukoveRadek[2])
            end = str(poleSipkyObloukoveRadek[3])
            text = str(poleSipkyObloukoveRadek[4])

            if (isinstance(poleSipkyObloukoveRadek[4], str) == False):
                text = str(abs(poleSipkyObloukoveRadek[4]))
            else:
                text = poleSipkyObloukoveRadek[4]

            radekJedneSipky = self.pripravRadkySipkyObloukoveJedenDOF(Ax, Ay, start, end, text)

            # doplni carku na konci radku
            if(iSipka < len(poleSipkyObloukove)-1):
                radekJedneSipky = radekJedneSipky.replace('}\'', '},\'')

            vsechnyRadkySipekJedenDOF.append(radekJedneSipky)

        return(vsechnyRadkySipekJedenDOF)


    def pripravRadkySipkySikmoVsechnyDOF(self):

        poleRadkuSipkySikmoJedenDOF = self.pripravRadkySipkySikmoJedenDOF()

        self.poleRadkuSipkySikmo.append(poleRadkuSipkySikmoJedenDOF)
        self.poleRadkuSipkySikmo.append(poleRadkuSipkySikmoJedenDOF)
        self.poleRadkuSipkySikmo.append(poleRadkuSipkySikmoJedenDOF)


    def pripravRadkySipkyObloukoveVsechnyDOF(self):

        poleRadkuSipkyObloukoveJedenDOF = self.pripravRadkySipkyObloukoveJedenDOF()

        self.poleRadkuSipkyObloukove.append(poleRadkuSipkyObloukoveJedenDOF)
        self.poleRadkuSipkyObloukove.append(poleRadkuSipkyObloukoveJedenDOF)
        self.poleRadkuSipkyObloukove.append(poleRadkuSipkyObloukoveJedenDOF)



    def pripravRadkySipkySikmoJedenDOF(self, Ax, Ay, Bx, By, text):

        radek = '        \'{"Ax":' + Ax + ',"Ay":' + Ay + ',"Bx":' + Bx + ',"By":' + By + ',"text":"' + text + '","zarovnaniKonec":"","zarovnaniStred":"vpravo","tloustkaCary":"1","barvaCary":"darkBlue","odsazeniX":5,"odsazeniY":5}\''
        return(radek)


    def pripravRadkySipkyObloukoveJedenDOF(self, Ax, Ay, start, end, text):

        radek = '        \'{"Ax":' + Ax + ',"Ay":' + Ay + ',"polomer":50,"start":' + start + ',"end":' + end + ',"text":"' + text + '","natoceniSipky":0.3,"tloustkaCary":"1","barvaCary":"darkCyan","delkaHrotu":10,"rozevreniHrotu":3,"zarovnaniKonec":"vpravo","zarovnaniStred":"vpravo","odsazeniX":15,"odsazenyY":15}\''
        return(radek)



    # naplni pole self.poleRadkuJSONVodorovne a self.poleRadkuJSONSvisle  s daty
    def ziskejPoleRadkuJSON(self, silyAJejichSouradnice):

        for iUzel in range(0, len(silyAJejichSouradnice)):
            silaASouradniceJedenUzel = silyAJejichSouradnice[iUzel]
            souradnice = silaASouradniceJedenUzel[1]
            velikostSily = silaASouradniceJedenUzel[2]

            Ax = souradnice[1]
            Ay = souradnice[2]
            Fx = velikostSily[0]
            Fy = velikostSily[1]
            M = velikostSily[2]

            if(Fx != 0):
                radekSipkaVodorovne = self.generujSipkuVodorovneJSONRadek(Ax, Ay, Fx, 100)
                self.poleRadkuJSONVodorovne.append(radekSipkaVodorovne)

            if (Fy != 0):
                radekSipkaSvisle = self.generujSipkuSvisleJSONRadek(Ax, Ay, Fy, 100)
                self.poleRadkuJSONSvisle.append(radekSipkaSvisle)


    def generujJSON(self):

        JSONSipkyPoleRadku = []

        JSONSipkyRadek = '{"sipky": ['
        JSONSipkyPoleRadku.append(JSONSipkyRadek)

        JSONSipkyRadek = '{"data": {'
        JSONSipkyPoleRadku.append(JSONSipkyRadek)

        JSONSipkyRadek = '"sikmo": ['
        JSONSipkyPoleRadku.append(JSONSipkyRadek)

        JSONSipkyRadek = '{"Ax":300,"Ay":100,"Bx":100,"By":50,"text":"F","zarovnaniKonec":"","zarovnaniStred":"vpravo","tloustkaCary":"1","barvaCary":"darkBlue","odsazeniX":5,"odsazeniY":5}'
        JSONSipkyPoleRadku.append(JSONSipkyRadek)

        JSONSipkyRadek = '],'
        JSONSipkyPoleRadku.append(JSONSipkyRadek)

        JSONSipkyRadek = '"obloukove": ['
        JSONSipkyPoleRadku.append(JSONSipkyRadek)

        JSONSipkyRadek = '{"Ax":300,"Ay":100,"polomer":50,"start":0,"end":0.5,"text":"F","natoceniSipky":0.3,"tloustkaCary":"1","barvaCary":"darkCyan","delkaHrotu":10,"rozevreniHrotu":3,"zarovnaniKonec":"vpravo","zarovnaniStred":"vpravo","odsazeniX":15,"odsazenyY":15}'
        JSONSipkyPoleRadku.append(JSONSipkyRadek)

        JSONSipkyRadek = ']'
        JSONSipkyPoleRadku.append(JSONSipkyRadek)

        JSONSipkyRadek = '},'
        JSONSipkyPoleRadku.append(JSONSipkyRadek)

        JSONSipkyRadek = '"Ox":50,'
        JSONSipkyPoleRadku.append(JSONSipkyRadek)

        JSONSipkyRadek = '"Oy":130,'
        JSONSipkyPoleRadku.append(JSONSipkyRadek)

        JSONSipkyRadek = '"id":"konzolaSilaNaKonci",'
        JSONSipkyPoleRadku.append(JSONSipkyRadek)

        JSONSipkyRadek = '"class":"konzolaSilaNaKonci"'
        JSONSipkyPoleRadku.append(JSONSipkyRadek)

        JSONSipkyRadek = '}]'
        JSONSipkyPoleRadku.append(JSONSipkyRadek)

        JSONSipkyRadek = '}'
        JSONSipkyPoleRadku.append(JSONSipkyRadek)

        return(JSONSipkyPoleRadku)


    def generujSipkuVodorovneJSONRadek(self, Ax, Ay, Fx, delkaSipky):

        sipkaDoprava = self.zjistiOrientaciSipky(float(Fx))
        sipkaDopravaJs = self.prevedTrueFalseNaJavascript(sipkaDoprava)
        velikost = abs(float(Fx))

        JSONRadek = '\'{"Ax":' + str(Ax) + ',"Ay":' + str(Ay) + ',"delkaSipky":' + str(delkaSipky) + ',"sipkaDoprava":"' + sipkaDopravaJs + '","text":"A=' + str(velikost) + 'kN"}\''

        return(JSONRadek)


    def generujSipkuSvisleJSONRadek(self, Ax, Ay, Fy, delkaSipky):

        sipkaDolu = self.zjistiOrientaciSipky(float(Fy))
        sipkaDoluJs = self.prevedTrueFalseNaJavascript(sipkaDolu)
        velikost = abs(float(Fy))

        JSONRadek = '{"Ax":' + str(Ax) + ',"Ay":' + str(Ay) + ',"delkaSipky":' + str(delkaSipky) + ',"sipkaDolu":"' + sipkaDoluJs + '","text":"A=' + str(velikost) + 'kN"}'

        return(JSONRadek)



    # upravi True/False do podoby aby bylo citelne javascriptem, tj, zmeni pocatecni pismeno na t/f
    def prevedTrueFalseNaJavascript(self, boolean):

        if (boolean) == True:
            booleanStr = "true"
        else:
            booleanStr = "false"

        return (booleanStr)


    def zjistiOrientaciSipky(self, velikost):

        if(velikost < 0):
            orientaceSipky = False
        else:
            orientaceSipky = True

        return(orientaceSipky)