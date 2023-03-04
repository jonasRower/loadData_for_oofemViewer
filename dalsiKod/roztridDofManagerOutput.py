
# roztridi data DofManager Output
class dofManager:

    def __init__(self, dofManagerData):

        self.prvniVolani = True
        self.vratDofPole = []

        self.dofManagerData = dofManagerData
        self.uzelDofDeformacePoleProJedenOFT = self.vratUzlyDofDeformace(self.dofManagerData)


    # getry
    def getUzelDofDeformacePoleProJedenOFT(self):
        return(self.uzelDofDeformacePoleProJedenOFT)

    def getDOF(self):
        return(self.vratDofPole)


    #vrati pole, kde na kazdem radku je
    # 1) cislo uzlu
    # 2) dof
    # 3) deformace
    def vratUzlyDofDeformace(self, dofManagerData):

        uzelDofDeformacePole = []

        for i in range(0, len(dofManagerData)):
            sekceNode = dofManagerData[i]

            uzelDofDeformace = self.rozdelSekciNodeNaRadky(sekceNode)
            uzelDofDeformacePole.append(uzelDofDeformace)

        return(uzelDofDeformacePole)


    def rozdelSekciNodeNaRadky(self, sekceNode):

        dofPole = []
        NodalDisplacementPole = []
        radekPole = []

        for r in range(0, len(sekceNode)):
            radekNode = sekceNode[r]
            WordArr = radekNode.split()
            if(len(WordArr) > 0):
                if(r == 0):
                    cisloUzlu = int(WordArr[1])
                else:
                    dof = int(WordArr[1])
                    nodalDisplacement = float(WordArr[3])

                    dofPole.append(dof)
                    NodalDisplacementPole.append(nodalDisplacement)



        radekPole.append(cisloUzlu)
        radekPole.append(dofPole)
        radekPole.append(NodalDisplacementPole)


        # pokud se jedna o prvni volani vrati data DOF
        # predpoklada se, ze data dof budou pro vsechny smycky stejna
        if(self.prvniVolani == True):
            self.vratDofPole = dofPole
            self.prvniVolani = False


        return(radekPole)




