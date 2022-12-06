
class tiskJSON:

    def __init__(self, dataKTisku):
        self.dataKTisku = dataKTisku
        self.nazevSouboru = "trojuhelniky2D.json"

        self.tiskniJSON(self.dataKTisku, self.nazevSouboru)


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