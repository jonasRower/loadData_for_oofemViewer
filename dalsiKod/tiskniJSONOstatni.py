# vytiskne konkretni JSON na konkretni cestu
import os

class tiskJSON:

    def __init__(self, dataKTisku, cestaProTisk):

        aktualniCesta = os.path.dirname(os.path.realpath(__file__))
        cesta = aktualniCesta + cestaProTisk

        # vytvori slozky, kam se budou zapisovat další výsledky
        self.vytvorSlozku(cesta)

        # vytiskneJSON
        self.tiskniJSON(dataKTisku, cesta)


    def vytvorSlozku(self, cesta):

        try:
            os.makedirs(cesta)
        except OSError:
            print("Neuspesne vytvorena slozka %s " % cesta)
        else:
            print("Uspesne vytvorena slozka %s " % cesta)


    def tiskniJSON(self, dataKTisku, cestaKSouboru):

        dataWrite = ""
        nazevSouboru = cestaKSouboru + "\\data.json"
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


    """
    def vytvorSystemSlozek(self, cestaSem):

        konstrukceCesta = cestaSem + "\\Konstrukce"
        podporyCesta = cestaSem + "\\Podpory"
        cislaUzluCesta = cestaSem + "\\cislaUzlu"
        cislaPrutuCesta = cestaSem + "\\cislaPrutu"
        zatizeniSiloveCesta = cestaSem + "\\zatizeniSilove"
        zatizeniDeformacniCesta = cestaSem + "\\zatizeniDeformacni"
        zatizeniTeplotouCesta = cestaSem + "\\zatizeniTeplotou"

        self.vytvorSlozku(konstrukceCesta)
        self.vytvorSlozku(podporyCesta)
        self.vytvorSlozku(cislaUzluCesta)
        self.vytvorSlozku(cislaPrutuCesta)
        self.vytvorSlozku(zatizeniSiloveCesta)
        self.vytvorSlozku(zatizeniDeformacniCesta)
        self.vytvorSlozku(zatizeniTeplotouCesta)
    
    """