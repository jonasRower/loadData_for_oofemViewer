# tiskne vysledky a konstrukci

import os

class tiskJSON:

    # puvodne byla tato trida koncipovana jen na tisk vysledku
    # dodatecne dodelavam, aby se daly tisknout i vstupy
    def __init__(self, dataKTisku, poleTime, Dofs, domena, output, nazevSouboru):

        self.aktualniCesta = os.path.dirname(os.path.realpath(__file__))
        self.poleTime = poleTime
        self.Dofs = Dofs
        self.domena = domena
        self.dataKTisku = dataKTisku
        self.output = output
        self.nazevSouboru = nazevSouboru


        # cesty ke slozkam jsou obsazeny v poli, v zavislosti zda se jedna o input nebo output
        self.cestyKeSlozkam = self.definujCestyPodleOutputInput(self.nazevSouboru)

        # vytvori system slozek
        if(self.domena == '2dBeam'):

            # cesty ke slozkam jsou ulozeny v poli
            for iCesta in range(0, len(self.cestyKeSlozkam)):
                self.vytvorSystemSlozek(self.cestyKeSlozkam[iCesta], self.Dofs)

        else:
            self.vytvorSystemSlozek(self.aktualniCesta + "\\JSONOutput\\NodalDisplacement", self.Dofs)

        # zapise vsechny data
        self.zapisujVsechnyData(self.dataKTisku, self.poleTime, self.Dofs)


    def vytvorSystemSlozek(self, cestaSem, Dofs):

        for iDof in range(0, len(Dofs)):
            dof = Dofs[iDof]
            Cesta = cestaSem + "\\" + str(dof)

            self.vytvorSlozku(Cesta)


    def zapisujVsechnyData(self, dataKTisku, poleTime, Dofs):

        nazevSouboru = self.nazevSouboru

        if(self.domena == '2dBeam'):

            for iCesta in range(0, len(self.cestyKeSlozkam)):
                data = dataKTisku[iCesta]
                cesta = self.cestyKeSlozkam[iCesta]


                #nazevSouboru = "GrafyKce"

                # jedna-li se o input, prepisuje se poleTime (urcujici nazvy souboru),
                # tak aby se soubory pro jednotlivy typ vysledku jmenoval jinak
                # je to z toho duvodu, ze zatizeni teplotou pro horni a dolni vlakna se zapisuji do stejne slozky, aby se data neprepisovala
                # stejne input ma vzdy jen jeden soubor (1 casovy krok = 1 OFT), takze je prostor to prepisovat zde

                if (self.output == False):
                    nazvySouboru = []


                    #nazevSouboru = "GrafyKceInput"

                    nazvySouboru.append(str(iCesta))

                    # pokud se jedna o ElementLoad, pak se tisknou vsechny 3 smery, pokud TemperatureLoad, pak pouze Dofs[1]
                    if(iCesta > 0): # jedna se o TemperatueLoad
                        DofsInput = []
                        DofsInput.append(-1)
                        DofsInput.append(Dofs[1])
                        DofsInput.append(-1)
                    else:           # jedna se o ElementLoad
                        DofsInput = Dofs

                    self.zapisujData(data, cesta, nazvySouboru, DofsInput, nazevSouboru)

                else:
                    # zapisuji se data bud s puvodnim poleTime (pro bezny output)
                    self.zapisujData(data, cesta, poleTime, Dofs, nazevSouboru)


        else:
            cestaSem = self.aktualniCesta + "\\JSONOutput\\NodalDisplacement"
            self.zapisujData(dataKTisku, cestaSem, poleTime, Dofs, "elementy2D")


    def tiskniDataOFT(self, dataKTiskuDOF, cestaSem, poleTime):

        for OFT in range(0, len(dataKTiskuDOF)):
            time = poleTime[OFT]
            time = time.replace("+", "p")
            time = time.replace("-", "m")
            nazevSouboru = "elementy2D_" + time + ".json"
            cesta = cestaSem + "\\" + nazevSouboru

            dataKTiskuOFT = dataKTiskuDOF[OFT]
            self.tiskniJSON(dataKTiskuOFT, cesta)


    def vytvorSlozku(self, cesta):

        try:
            os.makedirs(cesta)
        except OSError:
            print("Neuspesne vytvorena slozka %s " % cesta)
        else:
            print("Uspesne vytvorena slozka %s " % cesta)


    def tiskniJSON(self, dataKTisku, nazevSouboru):

        dataWrite = ""
        f = open(nazevSouboru, 'w')

        for i in range(0, len(dataKTisku)):
            radek = dataKTisku[i]
            if (i < len(dataKTisku) - 1):
                radek = radek + ' +'
            else:
                radek = radek + ';'

            dataWrite = dataWrite + radek + '\n'

        f.write(dataWrite)
        f.close()


    def vytvorSystemSlozekVysledky(self, cestaSem):

        LocalDisplacementCesta = cestaSem + "\\JSONOutput\\LocalDisplacements"
        LocalForcesCesta = cestaSem + "\\JSONOutput\\LocalForces"
        GlobalDisplacementCesta = cestaSem + "\\JSONOutput\\GlobalDisplacements"

        self.vytvorSlozku(LocalDisplacementCesta)
        self.vytvorSlozku(LocalForcesCesta)
        self.vytvorSlozku(GlobalDisplacementCesta)


    def zapisujData(self, LocalDisplacement, cestaSem, poleTime, Dofs, nazevSouboruKoren):

        for smer in range(0, len(Dofs)):
            dof = Dofs[smer]

            # tiskne se pouze kdyz je Dof > -1
            if(dof > -1):
                cesta = cestaSem + "\\" + str(dof)

                LocalDisplacementSmer = LocalDisplacement[smer]
                self.ziskejDataOft(LocalDisplacementSmer, cesta, poleTime, nazevSouboruKoren)



    def ziskejDataOft(self, dataJSON, cestaSem, poleTime, nazevSouboruKoren):

        # spusti smycku jen v pripade, ze dataJSON je jeste jedenkrat vnorene
        #if(isinstance(dataJSON[0], list) == True):

        for OFT in range(0, len(dataJSON)):
            time = poleTime[OFT]
            time = time.replace("+", "p")
            time = time.replace("-", "m")
            nazevSouboru = nazevSouboruKoren + "_" + time + ".json"
            cesta = cestaSem + "\\" + nazevSouboru

            dataKTisku = dataJSON[OFT]
            self.tiskniJSON(dataKTisku, cesta)

        #else:
        #    nazevSouboru = nazevSouboruKoren + ".json"
        #   cesta = cestaSem + "\\" + nazevSouboru
        #    self.tiskniJSON(dataJSON, cesta)


    def vytvorSlozku(self, cesta):

        try:
            os.makedirs(cesta)
        except OSError:
            print("Neuspesne vytvorena slozka %s " % cesta)
        else:
            print("Uspesne vytvorena slozka %s " % cesta)


    # nastavuje seznam cest v zavislosti na tom, zda se jedna o output nebo input
    def definujCestyPodleOutputInput(self, nazevSouboru):

        cestyKeSlozkam = []

        if(nazevSouboru == "Sipky"):
            cestyKeSlozkam.append(self.aktualniCesta + "\\JSONOutput\\Reactions")
            cestyKeSlozkam.append(self.aktualniCesta + "\\JSONOutput\\NodalLoad")
            cestyKeSlozkam.append(self.aktualniCesta + "\\JSONOutput\\ForcedDisplacement")

        else:

            # zrejme predelat na cestu, tak aby se rozpoznavali moznosti podle cesty
            if(self.domena == '2dBeam'):
                if (self.output == True):
                    cestyKeSlozkam.append(self.aktualniCesta + "\\JSONOutput\\LocalDisplacements")
                    cestyKeSlozkam.append(self.aktualniCesta + "\\JSONOutput\\LocalForces")
                    cestyKeSlozkam.append(self.aktualniCesta + "\\JSONOutput\\GlobalDisplacements")
                else:
                    cestyKeSlozkam.append(self.aktualniCesta + "\\JSONOutput\\ElementLoad")
                    cestyKeSlozkam.append(self.aktualniCesta + "\\JSONOutput\\TemperatureLoad")
                    cestyKeSlozkam.append(self.aktualniCesta + "\\JSONOutput\\TemperatureLoad")
            else:
                cestyKeSlozkam.append(self.aktualniCesta + "\\JSONOutput\\" + self.domena)
                self.domena = '2dBeam'

        return (cestyKeSlozkam)



    def tiskniJSON(self, dataKTisku, nazevSouboru):

        dataWrite = ""
        f = open(nazevSouboru, 'w')

        for i in range(0, len(dataKTisku)):
            radek = dataKTisku[i]
            if(i < len(dataKTisku)-1):
                radek = radek + ' +'
            else:
                radek = radek + ';'

            dataWrite = dataWrite + radek + '\n'

        f.write(dataWrite)
        f.close()

        print("")

