# tiskne vysledky a konstrukci

import os

class tiskJSON:

    def __init__(self, dataKTisku, poleTime, Dofs, domena):

        self.aktualniCesta = os.path.dirname(os.path.realpath(__file__))
        self.poleTime = poleTime
        self.Dofs = Dofs
        self.domena = domena
        self.dataKTisku = dataKTisku

        # vytvori slozky "LocalDisplacements" a "LocalForces"
        self.vytvorSystemSlozekVysledky(self.aktualniCesta)

        # vytvori system slozek
        if(self.domena == '2dBeam'):
            self.vytvorSystemSlozek(self.aktualniCesta + "\\JSONOutput\\LocalDisplacements", self.Dofs)
            self.vytvorSystemSlozek(self.aktualniCesta + "\\JSONOutput\\LocalForces", self.Dofs)
            self.vytvorSystemSlozek(self.aktualniCesta + "\\JSONOutput\\GlobalDisplacements", self.Dofs)
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

        if(self.domena == '2dBeam'):
            LocalDisplacementData = dataKTisku[0]
            LocalForcesData = dataKTisku[1]
            GlobalDisplacementData = dataKTisku[2]

            LocalDisplacementCesta = self.aktualniCesta + "\\JSONOutput\\LocalDisplacements"
            LocalForcesCesta = self.aktualniCesta + "\\JSONOutput\\LocalForces"
            GlobalDisplacementCesta = self.aktualniCesta + "\\JSONOutput\\GlobalDisplacements"

            self.zapisujData(LocalDisplacementData, LocalDisplacementCesta, poleTime, Dofs, "GrafyKce")
            self.zapisujData(LocalForcesData, LocalForcesCesta, poleTime, Dofs, "GrafyKce")
            self.zapisujData(GlobalDisplacementData, GlobalDisplacementCesta, poleTime, Dofs, "GrafyKce")
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
            cesta = cestaSem + "\\" + str(dof)

            LocalDisplacementSmer = LocalDisplacement[smer]
            self.ziskejDataOft(LocalDisplacementSmer, cesta, poleTime, nazevSouboruKoren)



    def ziskejDataOft(self, dataJSON, cestaSem, poleTime, nazevSouboruKoren):

        for OFT in range(0, len(poleTime)):
            time = poleTime[OFT]
            time = time.replace("+", "p")
            time = time.replace("-", "m")
            nazevSouboru = nazevSouboruKoren + "_" + time + ".json"
            cesta = cestaSem + "\\" + nazevSouboru

            dataKTisku = dataJSON[OFT]
            self.tiskniJSON(dataKTisku, cesta)


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
            if(i < len(dataKTisku)-1):
                radek = radek + ' +'
            else:
                radek = radek + ';'

            dataWrite = dataWrite + radek + '\n'

        f.write(dataWrite)
        f.close()

        print("")

