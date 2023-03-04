
import pripravSipkyJSON

class sipkyJSON:

    def __init__(self, reakceAJejichSouradnice, silyAJejichSouradnice, vynuceneZatizeniPodpor, MeritkoKCE, poleTime, Dofs):

        self.silyAJejichSouradnice = silyAJejichSouradnice
        self.reakceAJejichSouradnice = reakceAJejichSouradnice
        self.vynuceneZatizeniPodpor = vynuceneZatizeniPodpor
        self.MeritkoKCE = MeritkoKCE
        self.poleTime = poleTime
        self.Dofs = Dofs

        self.vynuceneZatizeniPodpor = self.pridejPodurovenVynuceneZatizeniPodpor(self.vynuceneZatizeniPodpor)

        generujJSONreakce = pripravSipkyJSON.dataProJSONsipky(self.reakceAJejichSouradnice, self.MeritkoKCE, self.poleTime, "Reactions", self.Dofs)
        generujJSONSily = pripravSipkyJSON.dataProJSONsipky(self.silyAJejichSouradnice, self.MeritkoKCE, self.poleTime, "NodalLoads", self.Dofs)
        generujJSONVynuceneZatizeni = pripravSipkyJSON.dataProJSONsipky(self.vynuceneZatizeniPodpor, self.MeritkoKCE, self.poleTime, "ForcedDisplacement", self.Dofs)
        JSONReakceVsechnyOFT = generujJSONreakce.getSilyJSON()
        JSONSily = generujJSONSily.getSilyJSON()
        JSONVynuceneDeformace = generujJSONVynuceneZatizeni.getSilyJSON()

        self.JSONSilyReakce = self.vlozReakceASilyDoJednohoPole(JSONReakceVsechnyOFT, JSONSily, JSONVynuceneDeformace)



    def getJSONSilyReakce(self):
        return(self.JSONSilyReakce)


    # vzhledem k tomu, ze vynuceneZatizeniPodpor neni vlozene do podurovne, spolecny kod ma problem
    # proto se poduroven pridava zde
    def pridejPodurovenVynuceneZatizeniPodpor(self, vynuceneZatizeniPodpor):
        vynuceneZatizeniPodpor1 = []
        vynuceneZatizeniPodpor1.append(vynuceneZatizeniPodpor)

        return(vynuceneZatizeniPodpor1)


    # aby byla zachovana konzistence dat a bylo mozne tisknout data, je treba vlozit data do jednoho pole
    def vlozReakceASilyDoJednohoPole(self, JSONReakceVsechnyOFT, JSONSily, JSONVynuceneDeformace):

        JSONSilyReakce = []
        JSONSilyReakce.append(JSONReakceVsechnyOFT)
        JSONSilyReakce.append(JSONSily)
        JSONSilyReakce.append(JSONVynuceneDeformace)

        return(JSONSilyReakce)
