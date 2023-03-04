
class trojuhelniky2DJSON:

    def __init__(self, JSONdataRadky, poleTime, Dofs):

        self.JSONdataRadky = JSONdataRadky
        self.poleTime = poleTime
        self.Dofs = Dofs
        self.JSONdataVsechnyUrovne = self.generujJSONPole(self.JSONdataRadky, self.poleTime, self.Dofs)



    # getry
    def getElementyJSON(self):
        return(self.JSONdataVsechnyUrovne)

    def generujJSONPole(self, JSONdataRadky, poleTime, Dofs):

        JSONdataAll = []
        JSONdataRadky = JSONdataRadky[0]  # asi je tam někde chyba a data jsou vnorena jeste jedenkrat nadbytecne

        for iDof in range(0, len(JSONdataRadky)):
            JSONdataDof = JSONdataRadky[iDof]
            dof = Dofs[iDof]
            JSONDOF = []

            for OFT in range(0, len(JSONdataDof)):
                JSONdataOFT = JSONdataDof[OFT]
                time = poleTime[OFT]
                JSONOFT = self.generujJSONProKazdouUrovenOFT(JSONdataOFT, dof, time)

                JSONDOF.append(JSONOFT)

            JSONdataAll.append(JSONDOF)

        return(JSONdataAll)


    def generujJSONProKazdouUrovenOFT(self, radkyJSON, dof, time):
    # generuje celyJSON

        elementyJSON = [];

        time = time.replace("+", "p")
        time = time.replace("-", "m")
        time = time.replace(".", "_")
        jsonPromenna = 'elementyJSON_' + str(dof) + '_' + time + ' = '

        elementyJSON.append(jsonPromenna + '\'{"elementy": [\'')
        elementyJSON.append('\'{"data":\'')
        elementyJSON.append('   \'{"element": [\'')

        for i in range(0, len(radkyJSON)):
            elementJSONradek = radkyJSON[i]
            elementyJSON.append(elementJSONradek)

        elementyJSON.append('   \']\'')
        elementyJSON.append('   \'},\'')
        elementyJSON.append('   \'"Ox":50,\'')
        elementyJSON.append('   \'"Oy":50,\'')
        elementyJSON.append('   \'"BarvaCaryElementuZvyrazneni":"blue",\'')
        elementyJSON.append('   \'"tloustkaCaryElementuZvyrazneni":"5",\'')
        elementyJSON.append('   \'"cisloElementuZvyrazneni":-1,\'')
        elementyJSON.append('   \'"nevyplnitCisloEelemntu":-1,\'')
        elementyJSON.append('   \'"cislaVsechUzlu":false,\'')
        elementyJSON.append('   \'"HodnotyVsechUzlu":false,\'')
        elementyJSON.append('   \'"nasobek":1,\'')
        elementyJSON.append('   \'"zaokrouhliNaPocetMist":0,\'')
        elementyJSON.append('   \'"id":"test",\'')
        elementyJSON.append('   \'"class":"XX"}\'')
        elementyJSON.append('\']}\'')

        return(elementyJSON)




