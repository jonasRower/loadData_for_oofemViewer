
class beam2DJSON:

    # vraci pole JSONu pro tisk Beam2D - kce + vnitrni sily/deformace
    def __init__(self, radkyKCEBeam2D, radkyGrafBeam2DPole, meritkaGrafy, poleTime, Dofs):

        self.radkyKCEBeam2D = radkyKCEBeam2D
        self.radkyGrafBeam2DPole = radkyGrafBeam2DPole
        self.meritkaGrafy = meritkaGrafy
        self.poleTime = poleTime
        self.Dofs = Dofs

        self.JSONBeam2D = self.rozdelRadkyGrafBeam2D(self.radkyGrafBeam2DPole, self.meritkaGrafy)

    #getry
    def getJSONBeam2D(self):
        return(self.JSONBeam2D)

    # z vnorene struktury ziskava jednotliva data
    def rozdelRadkyGrafBeam2D(self, radkyGrafBeam2DPole, meritkaGrafy):

        LocalDisplacementBeams2D = radkyGrafBeam2DPole[0]
        LocalDisplacementMeritka = meritkaGrafy[0]
        LocalForcesBeams2D = radkyGrafBeam2DPole[1]
        LocalForcesMeritka = meritkaGrafy[1]
        GlobalDisplacementBeams2D = radkyGrafBeam2DPole[2]
        GlobalDisplacementMeritka = meritkaGrafy[2]

        LocalDisplacementJSON = self.ziskejRadkyGrafBeam2D(LocalDisplacementBeams2D, LocalDisplacementMeritka, "LocalDisplacements")
        LocalForcesJSON = self.ziskejRadkyGrafBeam2D(LocalForcesBeams2D, LocalForcesMeritka, "LocalForces")
        GlobalDisplacementJSON = self.ziskejRadkyGrafBeam2D(GlobalDisplacementBeams2D, GlobalDisplacementMeritka, "GlobalDisplacements")

        JSONBeam2D = []
        JSONBeam2D.append(LocalDisplacementJSON)
        JSONBeam2D.append(LocalForcesJSON)
        JSONBeam2D.append(GlobalDisplacementJSON)

        return(JSONBeam2D)


    def ziskejRadkyGrafBeam2D(self, velicinaData, meritkaGrafy, nazevJSON):

        velicinaSmerJSON = []

        for smer in range(0, len(velicinaData)):
            velicinaSmer = velicinaData[smer]
            meritkoSmer = meritkaGrafy[smer]
            dof = self.Dofs[smer]
            velicinaOFTJSON = []

            for OFT in range(0, len(velicinaData)):
                velicinaOFT = velicinaSmer[OFT]
                meritkoOFT = meritkoSmer[OFT]
                time = self.poleTime[OFT]

                dataJSON = self.generujJSON(velicinaOFT, meritkoOFT, dof, time, nazevJSON)
                velicinaOFTJSON.append(dataJSON)

            velicinaSmerJSON.append(velicinaOFTJSON)

        return(velicinaSmerJSON)


    def generujJSON(self, radkyGraf, meritko, dof, time, nazevJSON):

        # generuje celyJSON

        time = time.replace("+", "p")
        time = time.replace("-", "m")
        time = time.replace(".", "_")
        jsonPromenna = nazevJSON + '_' + str(dof) + '_' + time + ' = '

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




