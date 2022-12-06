
# generuje JSON pro zobrazeni podpor
# podpory se generuji duplicitne, jak pro vodorovny, tak svisly smer, je potreba vysledny JSON promazat rucne

class podporyJSON:

    def __init__(self, vodorovnyPrutJSON, svislyPrutJSON):

        self.vodorovnyPrutJSON = vodorovnyPrutJSON
        self.svislyPrutJSON = svislyPrutJSON

        self.podporyJSON = self.generujJSON(self.vodorovnyPrutJSON, self.svislyPrutJSON)


    def generujJSON(self, vodorovnyPrutJSON, svislyPrutJSON):
        # generuje celyJSON

        podporyJSON = [];
        podporyJSON.append('\'{"podpory": [\'')
        podporyJSON.append('\' {"data": {\'')
        podporyJSON.append('\'   "vodorovnyPrut": [\'')

        for i in range(0, len(vodorovnyPrutJSON)):
            radekVodorovnyPrut = vodorovnyPrutJSON[i]
            podporyJSON.append(radekVodorovnyPrut)

        podporyJSON.append('\'    ],\'')
        podporyJSON.append('\'   "svislyPrut": [\'')

        for i in range(0, len(svislyPrutJSON)):
            radekSvislyPrut = svislyPrutJSON[i]
            podporyJSON.append(radekSvislyPrut)

        podporyJSON.append('\'    ]\'')
        podporyJSON.append('\'   },\'')
        podporyJSON.append('\'   "Ox":50,\'')
        podporyJSON.append('\'   "Oy":100,\'')
        podporyJSON.append('\'   "id":"test",\'')
        podporyJSON.append('\'   "class":"XX"\'')
        podporyJSON.append('\' }]\'')
        podporyJSON.append('\'}\'')


        return (podporyJSON)

    # getry
    def getPodporyJSON(self):
        return(self.podporyJSON)