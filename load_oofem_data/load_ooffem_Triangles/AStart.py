
import inFileProcessing
import outFileProcessing

import NactiSoubor
import generujTrojuhelniky2D
import barvyTrojuhelnika
import pripravDataProJSONTrojuhelniky
import tiskniJSON
import TiskniJSONResults


zpracujInFile = inFileProcessing.inFile()
zpracujOutFile = outFileProcessing.outFile()

# ziska souradnice jednotlivych prutu (inFileProcessing)
uzlyAJejichSouradnice = zpracujInFile.getUzlyASouradnice()
souradniceVsechTrojuhelniku = zpracujInFile.getSouradniceVsechTrojuhelniku()
uzlyTrojuhelnika = zpracujInFile.getUzlyTrojuhelnika()

# ziska podpory (inFileProcessing)
podporyKloubovePosuvneVodorovne = zpracujInFile.getPodporyKloubovePosuvneVodorovne()
podporyKloubovePosuvneSvisle = zpracujInFile.getPodporyKloubovePosuvneSvisle()
podporyVetknute = zpracujInFile.getPodporyVetknute()

# ziska vysledky k jednotlivym prutum/uzlum (outFileProcessing)
LocalDisplacements = zpracujOutFile.getLocalDisplacements()
LocalForces = zpracujOutFile.getLocalForces()
Strains = zpracujOutFile.getStrains()
Stresses = zpracujOutFile.getStresses()
NodalDisplacements = zpracujOutFile.getNodalDisplacement()
poleTime = zpracujOutFile.getPoleTime()

# vrati HSL hodnoty, aby mohl obarvit elementy v grafice
barvyElementu = barvyTrojuhelnika.barvy2DElementu(NodalDisplacements, uzlyTrojuhelnika)
HSLHodnoty = barvyElementu.getHodnotyHsl()
prumerneHodnoty = barvyElementu.getPrumerneHodnoty()

# pripravi data pro generovani trojuhelniku
dataTrojuhelnikyJSON = pripravDataProJSONTrojuhelniky.dataProJSON(souradniceVsechTrojuhelniku, uzlyTrojuhelnika, HSLHodnoty, NodalDisplacements, prumerneHodnoty)
JSONdataRadky = dataTrojuhelnikyJSON.getJSONdataRadky()
Dofs = dataTrojuhelnikyJSON.getDofs()




####################################

#adresaXML = "axi01.oofem.in"
#dataIn = NactiSoubor.XML(adresaXML)
#poleRadku = dataIn.getPole()

#souradniceVsechTrojuhelniku = []
#trojuhelnikoveElementy = roztridData2.data(poleRadku)
#souradniceVsechTrojuhelniku = trojuhelnikoveElementy.getSouradniceVsechTrojuhelniku()
#uzlyTrojuhelnika = trojuhelnikoveElementy.getUzlyTrojuhelnika()

#vygeneruje JSON
generujJSONtrojuhelniky = generujTrojuhelniky2D.trojuhelniky2DJSON(JSONdataRadky, poleTime, Dofs)
elementyJSON = generujJSONtrojuhelniky.getElementyJSON()

#vytiskne JSON
TiskniJSONResults.tiskJSON(elementyJSON, poleTime, Dofs)


print("")