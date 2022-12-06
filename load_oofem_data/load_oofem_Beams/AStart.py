
import inFileProcessing
import outFileProcessing

import tiskniJSONResults
import tiskniJSONOstatni
import generujBeams2DJSON
import generujPopisJSON
import generujPodporyJSON
import barvyTrojuhelnika
import pripravDataProJSONTrojuhelniky
import generujTrojuhelniky2D
import globalDisplacements


import pripravDataProJSONBeam2D
import pripravDataProJSONPodpory


MeritkoKCE = 50
MeritkoGraf = 20000

zpracujInFile = inFileProcessing.inFile()
zpracujOutFile = outFileProcessing.outFile()

# ziska souradnice jednotlivych prutu (inFileProcessing)
domena = zpracujInFile.getDomena()
uzlyAJejichSouradnice = zpracujInFile.getUzlyASouradnice()

if(domena == '2dBeam'):
    souradnicePrutu = zpracujInFile.getSouradnicePrutu()
else:
    souradniceVsechTrojuhelniku = zpracujInFile.getSouradniceVsechTrojuhelniku()
    uzlyTrojuhelnika = zpracujInFile.getUzlyTrojuhelnika()


# ziska podpory (inFileProcessing)
podporyKloubovePosuvneVodorovne = zpracujInFile.getPodporyKloubovePosuvneVodorovne()
podporyKloubovePosuvneSvisle = zpracujInFile.getPodporyKloubovePosuvneSvisle()
podporyVetknute = zpracujInFile.getPodporyVetknute()

# ziska zatizeni (inFileProcessing)
siloveZatizeniNaPrutech = zpracujInFile.getSiloveZatizeniNaPrutech()
zatizeniTeplotouHorniVlakna = zpracujInFile.getZatizeniTeplotouHorniVlakna()
zatizeniTeplotouDolniVlakna = zpracujInFile.getZatizeniTeplotouDolniVlakna()
vynuceneZatizeniPodpor = zpracujInFile.getVynuceneZatizeniPodpor()
silyAJejichSouradnice = zpracujInFile.getSilyAJejichSouradnice()




# ziska vysledky k jednotlivym prutum (outFileProcessing)
LocalDisplacements = zpracujOutFile.getLocalDisplacements()
LocalForces = zpracujOutFile.getLocalForces()
Strains = zpracujOutFile.getStrains()
Stresses = zpracujOutFile.getStresses()


if(domena == '2dBeam'):

    # ziska vysledky k jednotlivym elementum
    NodalDisplacements = zpracujOutFile.getNodalDisplacement()
    poleTime = zpracujOutFile.getPoleTime()

    # konvertuje NodalDisplacements na LocalDisplacements
    cislaUzluZacatekAKonecKonecElementu = zpracujInFile.getCislaUzluZacatekAKonecKonecElementu()
    konverzeNodalLocal = globalDisplacements.konvertujDisplacements(NodalDisplacements, LocalDisplacements, cislaUzluZacatekAKonecKonecElementu)
    globalDisplacements = konverzeNodalLocal.getLocalDisplacementsKonvertovane()

    # pripravi data pro generovani 2D beams
    dataBeam2DJSON = pripravDataProJSONBeam2D.dataProJSON(souradnicePrutu, LocalDisplacements, globalDisplacements, LocalForces, Strains, Stresses, MeritkoKCE, NodalDisplacements, siloveZatizeniNaPrutech, zatizeniTeplotouHorniVlakna, zatizeniTeplotouDolniVlakna)
    radkyKCEBeam2D = dataBeam2DJSON.getRadkyKCE()
    radkyGrafBeam2DOutput = dataBeam2DJSON.getRadkyGrafOutput()
    radkyGrafBeam2DInput = dataBeam2DJSON.getRadkyGrafInput()
    meritkaGrafy = dataBeam2DJSON.getMeritkaGrafy()
    Dofs = dataBeam2DJSON.getDofs()

    # pripravi data pro generovani podpor
    dataPodporyJSON = pripravDataProJSONPodpory.dataProJSONPodpory(podporyKloubovePosuvneVodorovne, podporyKloubovePosuvneSvisle, podporyVetknute, MeritkoKCE)
    svislyPrutJSON = dataPodporyJSON.getSvislyPrutJSON()
    vodorovnyPrutJSON = dataPodporyJSON.getvodorovnyPrutJSON()

    # generuje JSON - kci a zatizeni - vstupy do vypoctu
    #generujBeams2DInput = generujBeams2DJSON.beam2DJSON(radkyKCEBeam2D, radkyGrafBeam2DInput, meritkaGrafy, poleTime, Dofs)
    #JSONBeam2DPoleInput = generujBeams2DInput.getJSONBeam2D()

    # generuje JSON - kci a deformace/vnitrni sily - vystupy z vypoctu
    generujBeams2DOutput = generujBeams2DJSON.beam2DJSON(radkyKCEBeam2D, radkyGrafBeam2DOutput, meritkaGrafy, poleTime, Dofs)
    JSONBeam2DPoleOutput = generujBeams2DOutput.getJSONBeam2D()

    # generuje JSON popis
    generuJSONPopis = generujPopisJSON.popisJSON(uzlyAJejichSouradnice, MeritkoKCE)
    popisJSON = generuJSONPopis.getPopisJSON()

    # generuje JSON podpory
    generujJSONPodpory = generujPodporyJSON.podporyJSON(vodorovnyPrutJSON, svislyPrutJSON)
    podporyJSON = generujJSONPodpory.getPodporyJSON()

    #vytiskne JSON
    tiskniJSONResults.tiskJSON(JSONBeam2DPoleOutput, poleTime, Dofs, domena)
    #tiskniJSONResults.tiskJSON(generujBeams2DInput, poleTime, Dofs, domena)
    #tiskniJSONOstatni.tiskJSON(popisJSON, "\\JSONOutput\\Structure\\popis")
    #tiskniJSONOstatni.tiskJSON(podporyJSON, "\\JSONOutput\\Structure\\podpory")

else:

    # ziska vysledky k jednotlivym elementum
    NodalDisplacements = zpracujOutFile.getNodalDisplacement()
    poleTime = zpracujOutFile.getPoleTime()

    # vrati HSL hodnoty, aby mohl obarvit elementy v grafice
    barvyElementu = barvyTrojuhelnika.barvy2DElementu(NodalDisplacements, uzlyTrojuhelnika)
    HSLHodnoty = barvyElementu.getHodnotyHsl()
    prumerneHodnoty = barvyElementu.getPrumerneHodnoty()

    # pripravi data pro generovani trojuhelniku
    dataTrojuhelnikyJSON = pripravDataProJSONTrojuhelniky.dataProJSON(souradniceVsechTrojuhelniku, uzlyTrojuhelnika,
                                                                      HSLHodnoty, NodalDisplacements, prumerneHodnoty)
    JSONdataRadky = dataTrojuhelnikyJSON.getJSONdataRadky()
    Dofs = dataTrojuhelnikyJSON.getDofs()

    # vygeneruje JSON
    generujJSONtrojuhelniky = generujTrojuhelniky2D.trojuhelniky2DJSON(JSONdataRadky, poleTime, Dofs)
    elementyJSON = generujJSONtrojuhelniky.getElementyJSON()

    # vytiskne JSON
    tiskniJSONResults.tiskJSON(elementyJSON, poleTime, Dofs, domena)

    print("")


    """
    self.siloveZatizeniNaPrutech = roztridZatizeni.getSiloveZatizeniNaPrutech()
    self.zatizeniTeplotouHorniVlakna = roztridZatizeni.getZatizeniTeplotouHorniVlakna()
    self.zatizeniTeplotouDolniVlakna = roztridZatizeni.getZatizeniTeplotouDolniVlakna()
    self.vynuceneZatizeniPodpor = roztridZatizeni.getVynuceneZatizeniPodpor()
    self.silyAJejichSouradnice = roztridZatizeni.getSilyAJejichSouradnice()
    
    
    """