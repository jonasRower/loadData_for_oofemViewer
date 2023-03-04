
# generuje JSON pro popis uzlu a elementu
# (zatim jen uzlu)
class popisJSON:

    def __init__(self, uzlyAJejichSouradnice, MeritkoKCE):

        self.MeritkoKCE = MeritkoKCE
        self.uzlyAJejichSouradnice = uzlyAJejichSouradnice
        self.popisJSON = []
        self.radkyPopis = []

        self.radkyPopis = self.vratRadkyPopis(self.uzlyAJejichSouradnice)
        self.popisJSON = self.generujJSON(self.radkyPopis)


    def vratRadkyPopis(self, uzlyAJejichSouradnice):

        radkyPopisPole = []

        for i in range(0, len(uzlyAJejichSouradnice)):
            uzel = uzlyAJejichSouradnice[i]

            radekPopis = self.vratRadekPopis(uzel)
            if(i < len(uzlyAJejichSouradnice)-1):
                radekPopis = radekPopis + '},\''
            else:
                radekPopis = radekPopis + '}\''

            radkyPopisPole.append(radekPopis)

        return(radkyPopisPole)


    def vratRadekPopis(self, uzel):

        Ax = uzel[1] * self.MeritkoKCE
        Ay = uzel[2] * self.MeritkoKCE
        popis = uzel[0]
        index = ""
        zarovnani = "HS"
        odstupX = 5
        odstupY = 5

        radekPopis = '\'      {"Ax":' + str(Ax) + ',"Ay":' + str(Ay) + ',"popis":"' + str(popis) + '","index":"' + str(index) + '","zarovnani":"' + zarovnani + '","odstupX":' + str(odstupX) + ',"odstupY":' + str(odstupY)

        return(radekPopis)


    def generujJSON(self, radkyPopis):

        # generuje celyJSON
        popisJSON = [];
        popisJSON.append('\'{"popis": [\'')
        popisJSON.append('\'  {"data":\'')
        popisJSON.append('\'    {"popis": [\'')

        for i in range(0, len(radkyPopis)):
            radekPopis = radkyPopis[i]
            popisJSON.append(radekPopis)

        popisJSON.append('\'    ]\'')
        popisJSON.append('\'  },\'')
        popisJSON.append('\'  "Ox":50,\'')
        popisJSON.append('\'  "Oy":130,\'')
        popisJSON.append('\'  "id":"test",\'')
        popisJSON.append('\'  "class":"konzolaSilaNaKonciXX"}\'')
        popisJSON.append('\']}\'')

        return(popisJSON)


    # getry
    def getPopisJSON(self):
        return(self.popisJSON)


