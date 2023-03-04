
import inFileProcessing
import outFileProcessing

import tiskniJSONResults
import tiskniJSONOstatni
import generujBeams2DJSON
import generujPopisJSON
import generujPodporyJSON
import generujSipkyJSON
import barvyTrojuhelnika
import pripravDataProJSONTrojuhelniky
import generujTrojuhelniky2D
import globalDisplacements
import reakce


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
vynuceneZatizeniPodporAJejichSouradnice = zpracujInFile.getVynuceneZatizeniPodpor()
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
    reactionsOutput = zpracujOutFile.getReactionsOutput()

    # aby mohl generovat JSON, je treba k reakcim dovyjhledat souradnice
    dopisKreakcimSouradnice = reakce.reakceData(reactionsOutput, uzlyAJejichSouradnice)
    #dopisKsilamSouradnice = reakce.reakceData(silyInput, uzlyAJejichSouradnice)
    reakceAJejichSouradnice = dopisKreakcimSouradnice.getReakceAJejichSouradnice()
    #silyAJejichSouradnice = dopisKsilamSouradnice.getReakceAJejichSouradnice()

    # konvertuje NodalDisplacements na LocalDisplacements
    cislaUzluZacatekAKonecKonecElementu = zpracujInFile.getCislaUzluZacatekAKonecKonecElementu()
    konverzeNodalLocal = globalDisplacements.konvertujDisplacements(NodalDisplacements, LocalDisplacements, cislaUzluZacatekAKonecKonecElementu)
    globalDisplacements = konverzeNodalLocal.getLocalDisplacementsKonvertovane()

    # pripravi data pro generovani 2D beams
    dataBeam2DJSON = pripravDataProJSONBeam2D.dataProJSON(souradnicePrutu, LocalDisplacements, globalDisplacements, LocalForces, Strains, Stresses, MeritkoKCE, NodalDisplacements, siloveZatizeniNaPrutech, zatizeniTeplotouHorniVlakna, zatizeniTeplotouDolniVlakna, cislaUzluZacatekAKonecKonecElementu)


    radkyKCEBeam2D = dataBeam2DJSON.getRadkyKCE()
    radkyGrafBeam2DOutput = dataBeam2DJSON.getRadkyGrafOutput()
    radkyGrafBeam2DInput = dataBeam2DJSON.getRadkyGrafInput()
    meritkaGrafyInputs = dataBeam2DJSON.getMeritkaGrafyInputs()
    meritkaGrafyOutputs = dataBeam2DJSON.getMeritkaGrafyOutputs()
    Dofs = dataBeam2DJSON.getDofs()

    # pripravi data pro generovani podpor
    dataPodporyJSON = pripravDataProJSONPodpory.dataProJSONPodpory(podporyKloubovePosuvneVodorovne, podporyKloubovePosuvneSvisle, podporyVetknute, MeritkoKCE)
    svislyPrutJSON = dataPodporyJSON.getSvislyPrutJSON()
    vodorovnyPrutJSON = dataPodporyJSON.getvodorovnyPrutJSON()

    # generuje JSON - kci a zatizeni - vstupy do vypoctu
    generujBeams2DInput = generujBeams2DJSON.beam2DJSON(radkyKCEBeam2D, radkyGrafBeam2DInput, meritkaGrafyInputs, poleTime, Dofs, False)
    JSONBeam2DPoleInput = generujBeams2DInput.getJSONBeam2D()

    # generuje JSON - kci a deformace/vnitrni sily - vystupy z vypoctu
    generujBeams2DOutput = generujBeams2DJSON.beam2DJSON(radkyKCEBeam2D, radkyGrafBeam2DOutput, meritkaGrafyOutputs, poleTime, Dofs, True)
    JSONBeam2DPoleOutput = generujBeams2DOutput.getJSONBeam2D()

    # generuje JSON popis
    generuJSONPopis = generujPopisJSON.popisJSON(uzlyAJejichSouradnice, MeritkoKCE)
    popisJSON = generuJSONPopis.getPopisJSON()

    # generuje JSON podpory
    generujJSONPodpory = generujPodporyJSON.podporyJSON(vodorovnyPrutJSON, svislyPrutJSON)
    podporyJSON = generujJSONPodpory.getPodporyJSON()

    # generuje JSON sipky
    generujJSONSilyReakce = generujSipkyJSON.sipkyJSON(reakceAJejichSouradnice, silyAJejichSouradnice, vynuceneZatizeniPodporAJejichSouradnice, MeritkoKCE, poleTime, Dofs)
    JSONSilyReakce = generujJSONSilyReakce.getJSONSilyReakce()




    #vytiskne JSON - Input
    tiskniJSONResults.tiskJSON(JSONBeam2DPoleInput, poleTime, Dofs, domena, False, "GrafyKceInput")

    # vytiskne JSON - Output
    tiskniJSONResults.tiskJSON(JSONBeam2DPoleOutput, poleTime, Dofs, domena, True, "GrafyKce")

    # vytiskne JSON - sipky = zatížení + reakce
    tiskniJSONResults.tiskJSON(JSONSilyReakce, poleTime, Dofs, domena, True, "Sipky")


    #tiskniJSONOstatni.tiskJSON(popisJSON, "\\JSONOutput\\Structure\\popis")
    tiskniJSONOstatni.tiskJSON(podporyJSON, "\\JSONOutput\\Supports")

else:

    # ziska vysledky k jednotlivym elementum
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

    # vygeneruje JSON
    generujJSONtrojuhelniky = generujTrojuhelniky2D.trojuhelniky2DJSON(JSONdataRadky, poleTime, Dofs)
    elementyJSON = generujJSONtrojuhelniky.getElementyJSON()

    # vytiskne JSON
    tiskniJSONResults.tiskJSON(elementyJSON, poleTime, Dofs, domena)

    print("")

