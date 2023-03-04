import pandas as pd

class dataDoExceluProTestovani:

    def __init__(self, dataDoExcelu):

        self.dataDoExcelu = dataDoExcelu
        self.vsechnyNazvyListu = []

        self.vsechnyNazvyListu.append("poleBeam2d")
        self.vsechnyNazvyListu.append("poleTr1supgaxi")
        self.vsechnyNazvyListu.append("poleSetu")
        self.vsechnyNazvyListu.append("poleBoundaryCondition")
        self.vsechnyNazvyListu.append("poleConstantEdgeLoad")
        self.vsechnyNazvyListu.append("poleNodalLoad")
        self.vsechnyNazvyListu.append("poleStructTemperatureLoad")
        self.vsechnyNazvyListu.append("polePeakFunction")

        self.zapisDataDoExcelu(self.dataDoExcelu, self.vsechnyNazvyListu)



    def zapisDataDoExcelu(self, sparovaneIndexyPodleTagu, vsechnyNazvyTagu):

        nazevSesitu = 'test.xlsx'

        writer = pd.ExcelWriter(nazevSesitu, engine='xlsxwriter')

        for i in range(0, len(sparovaneIndexyPodleTagu)):

            dataNaList = sparovaneIndexyPodleTagu[i]
            nazevListu = vsechnyNazvyTagu[i]

            df = pd.DataFrame(dataNaList)
            df.to_excel(writer, sheet_name=nazevListu)

            workbook = writer.book

        workbook.filename = nazevSesitu
        writer.save()

