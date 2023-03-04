
class beam2DJSON:

    # vraci pole JSONu pro tisk Beam2D - kce + vnitrni sily/deformace
    def __init__(self, radkyKCEBeam2D, radkyGrafBeam2DPole, meritkaGrafy, poleTime, Dofs, output):

        self.radkyKCEBeam2D = radkyKCEBeam2D
        self.radkyGrafBeam2DPole = radkyGrafBeam2DPole
        self.meritkaGrafy = meritkaGrafy
        self.poleTime = poleTime
        self.Dofs = Dofs
        self.output = output

        # pokud se jedna o input
        if(output == False):
            self.JSONBeam2D = self.rozdelRadkyGrafBeam2DInput(self.radkyGrafBeam2DPole, self.meritkaGrafy)

        # pokud se jedna o output
        if (output == True):
            self.JSONBeam2D = self.rozdelRadkyGrafBeam2DOutput(self.radkyGrafBeam2DPole, self.meritkaGrafy)


    #getry
    def getJSONBeam2D(self):
        return(self.JSONBeam2D)


    # z vnorene struktury ziskava jednotliva data pro Inputs
    def rozdelRadkyGrafBeam2DInput(self, radkyGrafBeam2DPole, meritkaGrafy):
        ElementLoadBeams2D = radkyGrafBeam2DPole[0]
        ElementLoadMeritka = meritkaGrafy[0]
        TemperatureHorniBeams2D = radkyGrafBeam2DPole[1]
        TemperatureHorniMeritka = meritkaGrafy[1]
        TemperatureDolniBeams2D = radkyGrafBeam2DPole[2]
        TemperatureDolniMeritka = meritkaGrafy[2]

        ElementLoadJSON = self.ziskejRadkyGrafBeam2D(ElementLoadBeams2D, ElementLoadMeritka, "ElementLoads", False)
        TemperatureHorniJSON = self.ziskejRadkyGrafBeam2D(TemperatureHorniBeams2D, TemperatureHorniMeritka, "TemperatureHorni", False)
        TemperatureDolniJSON = self.ziskejRadkyGrafBeam2D(TemperatureDolniBeams2D, TemperatureDolniMeritka, "TemperatureDolni", False)

        JSONBeam2D = []
        JSONBeam2D.append(ElementLoadJSON)
        JSONBeam2D.append(TemperatureHorniJSON)
        JSONBeam2D.append(TemperatureDolniJSON)

        return (JSONBeam2D)


    # z vnorene struktury ziskava jednotliva data pro Outputs
    def rozdelRadkyGrafBeam2DOutput(self, radkyGrafBeam2DPole, meritkaGrafy):

        LocalDisplacementBeams2D = radkyGrafBeam2DPole[0]
        LocalDisplacementMeritka = meritkaGrafy[0]
        LocalForcesBeams2D = radkyGrafBeam2DPole[1]
        LocalForcesMeritka = meritkaGrafy[1]
        GlobalDisplacementBeams2D = radkyGrafBeam2DPole[2]
        GlobalDisplacementMeritka = meritkaGrafy[2]

        LocalDisplacementJSON = self.ziskejRadkyGrafBeam2D(LocalDisplacementBeams2D, LocalDisplacementMeritka, "LocalDisplacements", True)
        LocalForcesJSON = self.ziskejRadkyGrafBeam2D(LocalForcesBeams2D, LocalForcesMeritka, "LocalForces", True)
        GlobalDisplacementJSON = self.ziskejRadkyGrafBeam2D(GlobalDisplacementBeams2D, GlobalDisplacementMeritka, "GlobalDisplacements", True)

        JSONBeam2D = []
        JSONBeam2D.append(LocalDisplacementJSON)
        JSONBeam2D.append(LocalForcesJSON)
        JSONBeam2D.append(GlobalDisplacementJSON)

        return(JSONBeam2D)


    def ziskejRadkyGrafBeam2D(self, velicinaData, meritkaGrafy, nazevJSON, pridejTime):

        velicinaSmerJSON = []

        for smer in range(0, len(velicinaData)):
            velicinaSmer = velicinaData[smer]
            meritkoSmer = meritkaGrafy[smer]
            dof = self.Dofs[smer]
            velicinaOFTJSON = []

            for OFT in range(0, len(velicinaSmer)):
                velicinaOFT = velicinaSmer[OFT]

                if (isinstance(meritkoSmer, list) == True):
                    meritkoOFT = meritkoSmer[OFT]
                    time = self.poleTime[OFT]
                    dataJSON = self.generujJSON(velicinaOFT, meritkoOFT, dof, time, nazevJSON, pridejTime)
                else:
                    dataJSON = self.generujJSON(velicinaOFT, meritkoSmer, dof, smer, nazevJSON, pridejTime)

                velicinaOFTJSON.append(dataJSON)


            velicinaSmerJSON.append(velicinaOFTJSON)

        return(velicinaSmerJSON)


    def generujJSON(self, radkyGraf, meritko, dof, time, nazevJSON, pridejTime):

        # generuje celyJSON

        time = str(time)
        time = time.replace("+", "p")
        time = time.replace("-", "m")
        time = time.replace(".", "_")

        if(pridejTime == True):
            jsonPromenna = nazevJSON + '_' + str(dof) + '_' + time + ' = '

        if (pridejTime == False):
            jsonPromenna = nazevJSON + '_' + str(dof) + ' = '


        grafyKCEJSON = [];
        grafyKCEJSON.append(jsonPromenna + '\'{"grafyKCE": [\'')
        grafyKCEJSON.append('\'  {"data": [\'')

        for i in range(0, len(self.radkyKCEBeam2D)):
            radekKce = self.radkyKCEBeam2D[i]
            radekGraf = radkyGraf[i]

            # prida pruty do JSONu
            grafyKCEJSON.append('\'     {"prut": {\'')
            grafyKCEJSON.append(radekKce)
            grafyKCEJSON.append(radekGraf)
            grafyKCEJSON.append('\'       }},\'')

        grafyKCEJSON.append('\'       {"Ox":50},\'')
        grafyKCEJSON.append('\'       {"Oy":100},\'')
        grafyKCEJSON.append('\'       {"meritkoGraf":' + str(meritko) + '},\'')
        grafyKCEJSON.append('\'       {"id":"test"},\'')
        grafyKCEJSON.append('\'       {"class":""}\'')
        grafyKCEJSON.append('\'   ]}\'')
        grafyKCEJSON.append('\'   ]}\'')

        return (grafyKCEJSON)




