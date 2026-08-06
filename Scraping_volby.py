import csv
import sys
import requests
from bs4 import BeautifulSoup as bs


def zpracuj_argumenty():
    if len(sys.argv) != 3:
        print("Chyba: Zadej URL a jméno výstupního souboru")
        sys.exit(1)

    url = sys.argv[1]
    jmeno_souboru = sys.argv[2]
    return url, jmeno_souboru

def nacti_obsah_stranky(url):
    request = requests.get(url)
    if request.ok:
        rozdeleny_html = bs(request.text, features="html.parser")
        return rozdeleny_html
    else:
        return None


def ziskej_volice(rozdeleny_text):
    volici = rozdeleny_text.find("td", headers="sa2")

    if volici is not None:
        return vycisti_cislo(volici.get_text())
    else:
        return None

def ziskej_obalky(rozdeleny_text):
    obalky =  rozdeleny_text.find("td" , headers="sa3")

    if obalky is not None:
        return vycisti_cislo(obalky.get_text())
    else:
        return None


def ziskej_hlasy(rozdeleny_text):
    hlasy = rozdeleny_text.find("td" , headers="sa6")

    if hlasy is not None:
        return vycisti_cislo(hlasy.get_text())
    else:
        return None

def ziskej_strany(rozdeleny_text):
    nazvy_strany = rozdeleny_text.find_all("td", attrs={"class":"overflow_name"})

    vysledky = []
    for nazev in nazvy_strany:
        hlasy = nazev.find_next_sibling("td", attrs={"class":"cislo"})
        vysledky.append((nazev.get_text(), vycisti_cislo(hlasy.get_text())))

    return vysledky

def ziskej_obce(rozdeleny_text):
    nazvy_obci = rozdeleny_text.find_all("td", attrs={"class" : "overflow_name"})

    obce = []
    for obec in nazvy_obci:
        odkaz_td = obec.find_next_sibling("td", attrs={"class" : "center"})
        odkaz =  odkaz_td.find("a")
        href = odkaz.get("href")
        obce.append((obec.get_text(), href))

    return obce

def sestav_url(href):
    zakladni_url = "https://volby.gov.cz/pls/ps2017nss/"
    return zakladni_url + href

def oprav_href(href):
    if "ps33" in href:
        href = href.replace("ps33", "ps311")
        if "xvyber" not in href:
            href = href + "&xvyber=2110"
    return href

def ziskej_kod_obce(href):
    cast_s_kodem = href.split("xobec=")[1]
    kod = cast_s_kodem.split("&")[0]
    return kod

def zpracuje_obce(nazev, href):
    href = oprav_href(href)
    kod = ziskej_kod_obce(href)
    url = sestav_url(href)
    obsah = nacti_obsah_stranky(url)

    if obsah is None:
        return None

    volici = ziskej_volice(obsah)
    obalky = ziskej_obalky(obsah)
    hlasy = ziskej_hlasy(obsah)
    strany = ziskej_strany(obsah)

    radek = [kod, nazev, volici, obalky, hlasy]

    for nazev_strany, pocet_hlasu in strany:
        radek.append(pocet_hlasu)

    return radek

def vycisti_cislo(text):
    if text is None:
        return None
    return text.replace("\xa0", "").replace(" ", "")

def zapis_do_csv(vsechny_radky, hlavicka, jmeno_souboru):
    with open(jmeno_souboru, mode="w", encoding='utf-8-sig', newline='') as soubor_csv:
        writer = csv.writer(soubor_csv)
        writer.writerow(hlavicka)
        writer.writerows(vsechny_radky)

def main():

    url_hlavni, jmeno_souboru = zpracuj_argumenty()

    obsah_hlavni = nacti_obsah_stranky(url_hlavni)
    obce = ziskej_obce(obsah_hlavni)

    vsechny_radky = []
    for nazev, href in obce:
        radek = zpracuje_obce(nazev, href)
        if radek is not None:
            vsechny_radky.append(radek)

    prvni_href = obce[0][1]
    prvni_url = sestav_url(prvni_href)
    prvni_obsah = nacti_obsah_stranky(prvni_url)
    strany = ziskej_strany(prvni_obsah)
    nazvy_stran = [nazev_strany for nazev_strany, pocet_hlasu in strany]

    hlavicka = ["kod obce", "nazev", "volici", "obalky", "hlasy"] + nazvy_stran

    zapis_do_csv(vsechny_radky, hlavicka ,jmeno_souboru)

main()