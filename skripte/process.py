#!/usr/bin/env python

import xlrd
import pickle
import glob
import pprint

import matplotlib.pyplot as plt

DATA_DIR = 'podaci/'
TEMP_DATA_DIR = 'privremeni_podaci/'

# Pitanja na koja sam htio dobiti odgovor:
#
# - raste li ponuda racunarstva i kojim tempom?
# - raste li interes za racunarstvom i kojim tempom?
#   => ovdje treba uzeti u obzir da populacija pada sto sigurno utjece na interes pa nije tako jednostavno usporediti medusobno godine!
# - kakav je trend mjesta koji se nude na privatnim ucilistima?
# - koliko od ostvarenog prava upisa doista upise?
# - raste li ponuda studija na engleskom?
# - raste li potraznja studija na engleskom?
# - kakav je trend redovnih i izvanrednih studija?
# - koliko studija je po pojedinim gradovima


# Neka pitanja koja su se pojavila tijekom rada na ovome:
#
# - zasto Medicinski fakultet u Zagrebu nema istaknut studij na EN? A gotovo sigurno ga ima...

# Neke natuknice
#
# - imamo punudu mjesta, u ljetnom upisnom roku sto je maksimum koji se moze upisati te u jesenskom roku - koji indicira nepopularnost pojedinih studija


# Indeksi kolona u svim podacima, sa dodanom godinom i upisnim rokovom
KOLONA_GODINA = 0
KOLONA_UPISNI_ROK = 1
KOLONA_NOSITELJ = 2
KOLONA_VRSTA_NOSITELJA = 3
KOLONA_IZVODAC = 4
KOLONA_TIP_STUDIJA = 5
KOLONA_STUDIJ = 6
KOLONA_MJESTO = 7
KOLONA_UPISNA_KVOTA = 8
KOLONA_BROJ_PRIJAVA = 9
KOLONA_PRVI_IZBOR = 10
KOLONA_OMJER_PRVI_UKUPNO = 11
KOLONA_PROSJECNI_PRIORITET_IZBORA = 12      # Ovo je objavljeno 2021. godine, ali sigurno ne 2022!
KOLONA_OSTVARILO_PRAVO_UPISA = 13

# Kod tagiranja se dodaje kolona sa tagovima
KOLONA_TAG = 14

# Posebna oznaka za kraj tagiranja, tako da se svi netagirani oznace kao nerazvrstani
FINISH = 255

def ucitaj_sve_datoteke(write_data_to_file = True):
    """
    Metoda koja ucitava sve raw podatke koje objavljuje AZVO te
    sve to smjesta u jedno polje. Osim kolona koje objavljuje
    AZVO, ova metoda dodaje jos kolonu za godinu kada je neki
    datapoint objavljen te radi li se o podacima za ljetni (l)
    ili jesenki (j) upisni rok.

    AZVO nije konzistentan u svim podacima i to se ovdje pokusava
    anulirati. Trenutno su prisutne sljedece nekonzistencije:

    - jedne godine su objavili dodatnu kolonu koja je nekakva
      prosjecni ponder pozeljnosti studija s obzirom na rang
      odabira pojedinca
    """

    print("Ucitavanje svih podataka...")

    svi_podaci = []

    for f in glob.glob(DATA_DIR + '*.xls'):
        ime = f.split('/')[1]
        godina = int(ime[:4])
        rok = ime[4]

        book = xlrd.open_workbook(f)
        sh = book.sheet_by_index(0)

        for row in range(sh.nrows - 2):
            data_point = [godina, rok]
            data_point.extend([ sh.cell_value(rowx=row+1,colx=c) for c in range(sh.ncols) ])

            if len(data_point) == 13:
                # Radi se o tablici kada nisu naveli prosjecni prioritet izbora i zbog toga se to mora simulirati!
                data_point.append(data_point[-1])
                data_point[-2] = 0

            for idx in range(KOLONA_UPISNA_KVOTA, KOLONA_OSTVARILO_PRAVO_UPISA + 1):
                # Ima celija koja nema upisane podatke! Pretpostavljamo nule.
                if data_point[idx] == '':
                    data_point[idx] = 0

            assert(len(data_point) == 14)
            svi_podaci.append(data_point)

    if write_data_to_file:
        with open(TEMP_DATA_DIR + 'ucitaj_sve_datoteke15.data', 'w') as f:
            for e in svi_podaci:
                f.write(str(e))
                f.write('\n')

    print("\t... ucitavanje zavrseno.")

    return svi_podaci

def __jedinstveni_podaci(svi_podaci, kolona, tekst, write_data_to_file = None):
    """
    Parametrizirana metoda koja generira jedinstvene podatke u nekom stupcu.
    """

    jedinstveni_podaci = set()

    for e in svi_podaci:
        podatak = e[kolona].strip()
        jedinstveni_podaci.add(podatak)

    print("{}: {}".format(tekst, len(nositelji)))

    if write_data_to_file:
        with open(TEMP_DATA_DIR + write_data_to_file, 'w') as f:
            for e in jedinstveni_podaci:
#                f.write(str(e) + '\n')
                f.write(str(e) + '\t' + str(e) + '\n')

def jedinstveni_nositelji(svi_podaci, write_data_to_file = False):
    """
    Metoda koja trazi jedinstvene nositelje studija.
    """
    if write_data_to_file:
        return __jedinstveni_podaci(svi_podaci, KOLONA_NOSITELJ, "Ukupno nositelja", write_data_to_file = 'nositelji.data')
    else:
        return __jedinstveni_podaci(svi_podaci, KOLONA_NOSITELJ, "Ukupno nositelja")

def jedinstveno_mjesto(svi_podaci, write_data_to_file = False):
    """
    Metoda koja trazi jedinstvena mjesta u kojima se provodi studij.
    """
    if write_data_to_file:
        return __jedinstveni_podaci(svi_podaci, KOLONA_MJESTO, "Ukupno mjesta", write_data_to_file = 'mjesta.data')
    else:
        return __jedinstveni_podaci(svi_podaci, KOLONA_MJESTO, "Ukupno mjesta")

def jedinstvena_vrsta_nositelja(svi_podaci, write_data_to_file = False):
    """
    Metoda koja trazi jedinstvene vrste nositelja.
    """
    if write_data_to_file:
        return __jedinstveni_podaci(svi_podaci, KOLONA_VRSTA_NOSITELJA, "Ukupno vrsta nositelja", write_data_to_file = 'vrste_nositelja.data')
    else:
        return __jedinstveni_podaci(svi_podaci, KOLONA_VRSTA_NOSITELJA, "Ukupno vrsta nositelja")

def jedinstveni_izvodaci(svi_podaci, write_data_to_file = False):
    """
    Metoda koja trazi jedinstvene izvodace.
    """
    if write_data_to_file:
        return __jedinstveni_podaci(svi_podaci, KOLONA_IZVODAC, "Ukupno izvodaca", write_data_to_file = 'izvodaci.data')
    else:
        return __jedinstveni_podaci(svi_podaci, KOLONA_IZVODAC, "Ukupno izvodaca")

def jedinstveni_tipovi_studija(svi_podaci, write_data_to_file = False):
    """
    Metoda koja trazi jedinstvene tipove studija. Pri tome radi i
    dodatnu normalizaciju. Prvo, uklanja tekst u zagradama koji 
    naznacava da se radi o strucnom studiju. Takoder, uklanja tekst
    iza znaka tocka-zarez nakon kojega obicno dolaze specificniji
    smjerovi.
    """

    studiji = set()
    studiji_normirani = set()
    studiji_normirani2 = set()

    for e in svi_podaci:
        studij = studij_normiran = e[KOLONA_STUDIJ].strip()
        studiji.add(studij)

        if studij.find('(') > -1:
            studij_normiran = studij[:studij.find('(')].strip()
            studiji_normirani.add(studij_normiran)
        else:
            studiji_normirani.add(studij)

        if studij_normiran.find(';') > -1:
            studij_normiran2 = studij_normiran[:studij_normiran.find(';')].strip()
            studiji_normirani2.add(studij_normiran2)
        else:
            studiji_normirani2.add(studij_normiran)

    print("Ukupno studija: {}".format(len(studiji)))
    print("Ukupno normiranih studija: {}".format(len(studiji_normirani)))
    print("Ukupno studija nakon dvostruke normalizacije: {}".format(len(studiji_normirani2)))

    if write_data_to_file:

        with open(TEMP_DATA_DIR + 'studiji.data', 'w') as f:
            for e in studiji:
                f.write(str(e))
                f.write('\n')

        with open(TEMP_DATA_DIR + 'studiji_normirani.data', 'w') as f:
            for e in studiji_normirani:
                f.write(str(e))
                f.write('\n')

        with open(TEMP_DATA_DIR + 'studiji_normirani2.data', 'w') as f:
            for e in studiji_normirani2:
                f.write(str(e))
                f.write('\n')

def _ucitaj_tagove(tag_datoteka):

    tagovi = []
    with open(tag_datoteka) as f:
        for l in f.readlines():
            if len(l.strip()) == 0 or l[0] == '#':
                continue

            a = l.split('\t')
            tagovi.append((a[0].lower(), a[1].strip()))

    return tagovi

def _tagiraj_podatke(svi_podaci, kolona_za_tagiranje, datoteke_tagova = None, jedinstvena_oznaka = False, write_data_to_file = False):

    # Ako nam nije proslijedena datoteka tagova, a nije ni kraj tagiranja,
    # onda izaci van...
    if kolona_za_tagiranje != FINISH and (datoteke_tagova is None or len(datoteke_tagova) == 0):
        return svi_podaci

    # Ako se trazi kraj tagiranja, onda treba provjeriti koji su zapisi
    # neoznaceni i dodati nepoznatu oznaku tako da svi budu uniformni.
    if kolona_za_tagiranje == FINISH:
        for e in svi_podaci:
            if len(e) == 14:
                e.append('netagiran')

        return svi_podaci

    # Slijedi oznacavanje...
    for dat in datoteke_tagova:

        tagovi = _ucitaj_tagove(dat)

        for e in svi_podaci:

            if len(e) == 15 and jedinstvena_oznaka:
                continue

            for t in tagovi:
                if e[kolona_za_tagiranje].lower().find(t[0].lower()) > -1:
                    if len(t) == 2 and len(t[1]) > 0:
                        if len(e) == 15:
                            e[KOLONA_TAG] = "{},{}".format(e[KOLONA_TAG], t[1])
                        else:
                            e.append(t[1])
                        break

    if write_data_to_file:
        with open(TEMP_DATA_DIR + 'tagirani_podaci.data', 'w') as f:
            for e in svi_podaci:
                f.write(str(e))
                f.write('\n')

    return svi_podaci

def suma_kolona_po_tagovima_i_po_godinama(svi_podaci,
        kolona_za_statistiku = KOLONA_UPISNA_KVOTA,
        tagovi_studija = None,
        tagovi_izvodaca = None,
        tagovi_mjesta = None,
        tagovi_vrsta_nositelja = None,
        tagovi_nositelja = None,
        upisni_rok = 'l',
        xlabel = "Godina",
        ylabel = ""):
    """
    Ova metoda prvo tagira podatke prema zadanim mapiranjima kroz
    argumente tagovi_*. Svaki argument tagira po nekoj koloni.
    Datoteka za tagiranje treba imati podniz u prvoj koloni te
    odgovarajuci tag u drugoj koloni, odvojeni tabulatorom.

    Nakon toga, metoda za svaki tag zbraja po godini kolonu
    zadanu ulaznim parametrom kolona_za_statistiku. I onda to
    sve iscrtava.
    """

    # Ovakvo sumiranje ne radi za kolonu koja predstavlja omjer dvije postojece kolone!
    assert (kolona_za_statistiku != KOLONA_OMJER_PRVI_UKUPNO)

    print("Izdrada statistike...")

    svi_podaci = _tagiraj_podatke(svi_podaci, KOLONA_IZVODAC, tagovi_izvodaca)
    svi_podaci = _tagiraj_podatke(svi_podaci, KOLONA_STUDIJ, tagovi_studija)
    svi_podaci = _tagiraj_podatke(svi_podaci, KOLONA_MJESTO, tagovi_mjesta)
    svi_podaci = _tagiraj_podatke(svi_podaci, KOLONA_VRSTA_NOSITELJA, tagovi_vrsta_nositelja)
    svi_podaci = _tagiraj_podatke(svi_podaci, KOLONA_NOSITELJ, tagovi_nositelja)
    svi_podaci = _tagiraj_podatke(svi_podaci, FINISH)

    po_tagovima = {}

    for dp in svi_podaci:
        if dp[KOLONA_UPISNI_ROK] != upisni_rok:
            continue

        key = str(dp[KOLONA_GODINA]) + dp[KOLONA_TAG]
        if dp[KOLONA_TAG] not in po_tagovima:
            po_tagovima[dp[KOLONA_TAG]] = {}

        if dp[KOLONA_GODINA] not in po_tagovima[dp[KOLONA_TAG]]:
            po_tagovima[dp[KOLONA_TAG]][dp[KOLONA_GODINA]] = 0

        po_tagovima[dp[KOLONA_TAG]][dp[KOLONA_GODINA]] += dp[kolona_za_statistiku]

    print("\t...izrada zavrsena.")

    for tag in po_tagovima:

        if tag == 'netagiran':
            continue

        lists = sorted(po_tagovima[tag].items())
        xvals, yvals = zip(*lists)

        plt.clf()
        plt.bar(xvals, yvals)
        plt.plot(xvals, yvals, '-o', color='orange')
        plt.title(tag)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        #plt.savefig(tag + "-" + upisni_rok + ".png")
        plt.show()

def upisano_u_prvom_roku(svi_podaci, grupiranje = set(range(KOLONA_NOSITELJ, KOLONA_UPISNA_KVOTA))):
    """
    Ova metoda trazi koliko je upisanih u prvom roku. Te informacije
    nema direktno vec ono sto je na raspolaganju je broj onih koji su
    ostvarili pravo upisa (a ne moraju nuzno i upisati!). Pouzdanija
    informacija je broj slobodnih mjesta na jesenskom roku! Ova metoda
    koristi taj pristup.
    """

    studiji = {}

    for dp in svi_podaci:

        # Dok ne prode jesenski upisni rok...
        if dp[KOLONA_GODINA] == 2022:
            continue

        key1_array = []
        for idx in range(KOLONA_NOSITELJ, KOLONA_UPISNA_KVOTA):
            if idx in grupiranje:
                key1_array.append(dp[idx])

        key1 = str(key1_array)
        if key1 not in studiji:
            studiji[key1] = {}

        key2 = str(dp[KOLONA_GODINA])
        if key2 not in studiji[key1]:
            studiji[key1][key2] = {
                        'kolona_upisna_kvota_ljeto': 0,
                        'kolona_ostvarilo_pravo_upisa_ljeto': 0,
                        'kolona_upisna_kvota_jesen': 0,
                        'kolona_ostvarilo_pravo_upisa_jesen': 0,
                        'kolona_prvi_izbor_ljeto': 0,
                        'kolona_prvi_izbor_jesen': 0,
                    }

        if dp[KOLONA_UPISNI_ROK] == 'l':
            studiji[key1][key2]['kolona_upisna_kvota_ljeto'] += dp[KOLONA_UPISNA_KVOTA]
            studiji[key1][key2]['kolona_ostvarilo_pravo_upisa_ljeto'] += dp[KOLONA_OSTVARILO_PRAVO_UPISA]
            studiji[key1][key2]['kolona_prvi_izbor_ljeto'] += dp[KOLONA_PRVI_IZBOR]
        else:
            studiji[key1][key2]['kolona_upisna_kvota_jesen'] += dp[KOLONA_UPISNA_KVOTA]
            studiji[key1][key2]['kolona_ostvarilo_pravo_upisa_jesen'] += dp[KOLONA_OSTVARILO_PRAVO_UPISA]
            studiji[key1][key2]['kolona_prvi_izbor_jesen'] += dp[KOLONA_PRVI_IZBOR]

    for key1 in studiji:
        print("Iscrtavanje grafa za: " + key1)

        xvals = []
        yvals = []

        for dp in sorted(studiji[key1].items()):
            if dp[1]['kolona_upisna_kvota_ljeto'] == 0:
                continue

            xvals.append(dp[0])
            #yvals.append(dp[1]['kolona_upisna_kvota_ljeto'] - dp[1]['kolona_ostvarilo_pravo_upisa_ljeto'] - dp[1]['kolona_ostvarilo_pravo_upisa_jesen'])
            yvals.append(dp[1]['kolona_prvi_izbor_ljeto'] * 100 / dp[1]['kolona_upisna_kvota_ljeto'])

        plt.clf()
        plt.bar(xvals, yvals)
        plt.xlabel('Godina')
        plt.ylabel('Omjer prvog odabira i ukupnog broja mjesta [%]')
        plt.title(key1)
        plt.show()

def sveucilista_vs_veleucilista():

    svi_podaci = ucitaj_sve_datoteke()
    suma_kolona_po_tagovima_i_po_godinama(svi_podaci, 
            kolona_za_statistiku = KOLONA_UPISNA_KVOTA,
            tagovi_vrsta_nositelja = [ "mapiranje_tagova/veleucilista_vs_sveucilista.csv" ],
            upisni_rok = 'l',
            ylabel = "Ukupan broj mjesta na ljetnom upisnom roku")

    svi_podaci = ucitaj_sve_datoteke()
    suma_kolona_po_tagovima_i_po_godinama(svi_podaci, 
            kolona_za_statistiku = KOLONA_UPISNA_KVOTA,
            tagovi_vrsta_nositelja = [ "mapiranje_tagova/veleucilista_vs_sveucilista.csv" ],
            upisni_rok = 'j',
            ylabel = "Ukupan broj mjesta na jesenskom upisnom roku")

    svi_podaci = ucitaj_sve_datoteke()
    suma_kolona_po_tagovima_i_po_godinama(svi_podaci, 
            kolona_za_statistiku = KOLONA_PRVI_IZBOR,
            tagovi_vrsta_nositelja = [ "mapiranje_tagova/veleucilista_vs_sveucilista.csv" ],
            upisni_rok = 'l',
            ylabel = "Broj prvih izbora na ljetnom upisnom roku")

    svi_podaci = ucitaj_sve_datoteke()
    suma_kolona_po_tagovima_i_po_godinama(svi_podaci, 
            kolona_za_statistiku = KOLONA_PRVI_IZBOR,
            tagovi_vrsta_nositelja = [ "mapiranje_tagova/veleucilista_vs_sveucilista.csv" ],
            upisni_rok = 'j',
            ylabel = "Broj prvih izbora na jesenskom upisnom roku")

    svi_podaci = ucitaj_sve_datoteke()
    suma_kolona_po_tagovima_i_po_godinama(svi_podaci, 
            kolona_za_statistiku = KOLONA_OSTVARILO_PRAVO_UPISA,
            tagovi_vrsta_nositelja = [ "mapiranje_tagova/veleucilista_vs_sveucilista.csv" ],
            upisni_rok = 'l',
            ylabel = "Ostvarilo pravo upisa na ljetnom upisnom roku")

    svi_podaci = ucitaj_sve_datoteke()
    suma_kolona_po_tagovima_i_po_godinama(svi_podaci, 
            kolona_za_statistiku = KOLONA_OSTVARILO_PRAVO_UPISA,
            tagovi_vrsta_nositelja = [ "mapiranje_tagova/veleucilista_vs_sveucilista.csv" ],
            upisni_rok = 'j',
            ylabel = "Ostvarilo pravo upisa na jesenskom upisnom roku")

def sveucilista_strucni_studij():

    svi_podaci = ucitaj_sve_datoteke()
    suma_kolona_po_tagovima_i_po_godinama(svi_podaci, 
            kolona_za_statistiku = KOLONA_UPISNA_KVOTA,
            tagovi_studija = [ "mapiranje_tagova/strucni_studij_tag.csv" ],
            tagovi_vrsta_nositelja = [ "mapiranje_tagova/veleucilista_vs_sveucilista.csv" ],
            upisni_rok = 'l',
            ylabel = "Ukupan broj mjesta na ljetnom upisnom roku")

    svi_podaci = ucitaj_sve_datoteke()
    suma_kolona_po_tagovima_i_po_godinama(svi_podaci, 
            kolona_za_statistiku = KOLONA_PRVI_IZBOR,
            tagovi_studija = [ "mapiranje_tagova/strucni_studij_tag.csv" ],
            tagovi_vrsta_nositelja = [ "mapiranje_tagova/veleucilista_vs_sveucilista.csv" ],
            upisni_rok = 'l',
            ylabel = "Broj prvih izbora na ljetnom upisnom roku")

    svi_podaci = ucitaj_sve_datoteke()
    suma_kolona_po_tagovima_i_po_godinama(svi_podaci, 
            kolona_za_statistiku = KOLONA_OSTVARILO_PRAVO_UPISA,
            tagovi_studija = [ "mapiranje_tagova/strucni_studij_tag.csv" ],
            tagovi_vrsta_nositelja = [ "mapiranje_tagova/veleucilista_vs_sveucilista.csv" ],
            upisni_rok = 'l',
            ylabel = "Ostvarilo pravo upisa na ljetnom upisnom roku")

    svi_podaci = ucitaj_sve_datoteke()
    suma_kolona_po_tagovima_i_po_godinama(svi_podaci, 
            kolona_za_statistiku = KOLONA_UPISNA_KVOTA,
            tagovi_studija = [ "mapiranje_tagova/strucni_studij_tag.csv" ],
            tagovi_vrsta_nositelja = [ "mapiranje_tagova/veleucilista_vs_sveucilista.csv" ],
            upisni_rok = 'j',
            ylabel = "Ukupan broj mjesta na jesenskom upisnom roku")

    svi_podaci = ucitaj_sve_datoteke()
    suma_kolona_po_tagovima_i_po_godinama(svi_podaci, 
            kolona_za_statistiku = KOLONA_PRVI_IZBOR,
            tagovi_studija = [ "mapiranje_tagova/strucni_studij_tag.csv" ],
            tagovi_vrsta_nositelja = [ "mapiranje_tagova/veleucilista_vs_sveucilista.csv" ],
            upisni_rok = 'j',
            ylabel = "Broj prvih izbora na jesenskom upisnom roku")

    svi_podaci = ucitaj_sve_datoteke()
    suma_kolona_po_tagovima_i_po_godinama(svi_podaci, 
            kolona_za_statistiku = KOLONA_OSTVARILO_PRAVO_UPISA,
            tagovi_studija = [ "mapiranje_tagova/strucni_studij_tag.csv" ],
            tagovi_vrsta_nositelja = [ "mapiranje_tagova/veleucilista_vs_sveucilista.csv" ],
            upisni_rok = 'j',
            ylabel = "Ostvarilo pravo upisa na jesenskom upisnom roku")

if __name__ == '__main__':
    sveucilista_strucni_studij()
    exit(1)
        
if __name__ == '__main__':
    sveucilista_strucni_studij()
    exit(1)
        
if __name__ == '__main__':
    sveucilista_strucni_studij()
    exit(1)
        
if __name__ == '__main__':
    sveucilista_strucni_studij()
    exit(1)

    #jedinstveni_tipovi_studija(svi_podaci, True)
    #jedinstveni_izvodaci(svi_podaci, True)
    #jedinstveno_mjesto(svi_podaci, True)
    #jedinstvena_vrsta_nositelja(svi_podaci, True)
    #jedinstveni_nositelji(svi_podaci, True)

#    svi_podaci = ucitaj_sve_datoteke()
#    suma_kolona_po_tagovima_i_po_godinama(svi_podaci, 
#            kolona_za_statistiku = KOLONA_UPISNA_KVOTA,
##            tagovi_studija = [ "mapiranje_tagova/racunarstvo_po_studijima.csv" ],
#            tagovi_studija = [ "mapiranje_tagova/strucni_studij.csv" ],
##            tagovi_izvodaca = [ "mapiranje_tagova/tag_po_izvodacu.csv" ],
##            tagovi_mjesta = [ "mapiranje_tagova/tag_po_mjestima.csv" ],
##            tagovi_vrsta_nositelja = [ "mapiranje_tagova/javni_vs_privatni.csv" ],
#            tagovi_vrsta_nositelja = [ "mapiranje_tagova/veleucilista_vs_sveucilista.csv" ],
##            tagovi_nositelja = [ "mapiranje_tagova/veleucilista_vs_sveucilista.csv" ],
#            upisni_rok = 'j',
#            ylabel = "Ukupan broj mjesta na ljetnom upisnom roku")

#    upisano_u_prvom_roku(svi_podaci, grupiranje = set([KOLONA_NOSITELJ]))

