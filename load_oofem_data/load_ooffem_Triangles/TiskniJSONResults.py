# tiskne vysledky a konstrukci

import os

class tiskJSON:

    def __init__(self, dataKTisku, poleTime, Dofs):

        self.aktualniCesta = os.path.dirname(os.path.realpath(__file__))
        self.poleTime = poleTime
        self.Dofs = Dofs

        # vytvori slozky u, v, fi
        self.vytvorSystemSlozekLocalDisplacements(self.aktualniCesta + "\\JSONOutput\\NodalDisplacement", self.Dofs)

        # zapise vsechny data
        self.zapisujVsechnyData(dataKTisku, self.poleTime, self.Dofs)


    def vytvorSystemSlozekLocalDisplacements(self, cestaSem, Dofs):

        for iDof in range(0, len(Dofs)):
            dof = Dofs[iDof]
            Cesta = cestaSem + "\\" + str(dof)

            self.vytvorSlozku(Cesta)


    def zapisujVsechnyData(self, dataKTisku, poleTime, Dofs):

        cestaSem = self.aktualniCesta + "\\JSONOutput\\NodalDisplacement"

        for iDof in range(0, len(dataKTisku)):

            dof = Dofs[iDof]
            cesta = cestaSem + "\\" + str(dof)

            dataKTiskuDOF = dataKTisku[iDof]
            self.tiskniDataOFT(dataKTiskuDOF, cesta, poleTime)


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
            if(i < len(dataKTisku)-1):
                radek = radek + ' +'
            else:
                radek = radek + ';'

            dataWrite = dataWrite + radek + '\n'

        f.write(dataWrite)
        f.close()

        print("")

