"""
projekt_3.py: třetí projekt 
author: Tadeáš Žežulka
email: grumpysilver@seznam.cz
discord: grumpy6666
"""

#Importy
import requests
from bs4 import BeautifulSoup
import argparse

# Funkce pro sestavení úplné URL z relativní URL
def sestav_url(base_url, relative_url):
    if '/' in base_url:
        return base_url[:base_url.rfind('/')] + "/" + relative_url
    return base_url

# Funkce pro získání názvů stran z dané URL
def ziskej_nazvy_stran(stranky_url):
    response = requests.get(stranky_url)  # Odeslání HTTP GET požadavku
    if response.status_code == 200:  # Kontrola zda byl požadavek úspěšný
        soup = BeautifulSoup(response.content, 'html.parser')  # Pokud byl požadavek úspěšný HTML obsah odpovědi se zpracuje pomocí knihovny BeautifulSoup.
        radky = soup.find_all('tr')  # Vyhledání všech řádků tabulky
        seznam_stran = []
        for radek in radky:
            bunky = radek.find_all("td")  # Vyhledání všech buněk v řádku
            if len(bunky) == 5:  #Pokud řádek obsahuje přesně 5 buněk předpokládá se že druhá buňka obsahuje název strany.
                nazev_strany = bunky[1].get_text().strip() #Odstranení mezer v názvech strany
                if nazev_strany not in seznam_stran:
                    seznam_stran.append(nazev_strany)  # Přidání názvu strany do seznamu pokud již nebyl přidán
        return seznam_stran
    else:
        print("Nepodařilo se stáhnout data")
        return []

# Funkce pro zpracování hlavních dat z první URL
def zpracuj_data(prvni_url, soubor, strany_url):
    response = requests.get(prvni_url)  #Odeslání HTTP GET požadavek na zadanou první URL adresu uloží odpověď.

    if response.status_code == 200:  # Kontrola, zda byl požadavek úspěšný
        soup = BeautifulSoup(response.content, 'html.parser')  # HTML obsah odpovědi se zpracuje pomocí modulu BeautifulSoup.
        radky = soup.find_all('tr') 
        cislo_radku = 0
        with open(soubor, 'w', encoding='cp1250') as f:  # Otevření souboru soubor pro zápis
            # Zápis záhlaví CSV souboru
            f.write("Kod oblasti;Nazev oblasti;Registrovany volici;Obalky;Platné hlasy;") #Zapsání všech pevně stanovených sloupců do csv
            seznam_stran = ziskej_nazvy_stran(strany_url)  # Zapsání všech stran do csv
            f.write(";".join(seznam_stran))
            f.write("\n")
            for radek in radky:
                bunky = radek.find_all("td")  # Vyhledání všech buněk v řádku

                if len(bunky) >= 2:  # Pokud řádek obsahuje alespoň 2 buňky zvýší se cislo_radku o 1
                    cislo_radku += 1
                    prvni_bunka = bunky.pop(0) #  Z prvních dvou bunek se zápis odstraní a napíše do prvni_bunky
                    druha_bunka = bunky.pop(0) # do druhy_bunky
                    odkazy = prvni_bunka.find_all("a")  # Vyhledá všechny odkazů v první buňce
                    if odkazy:
                        prvni_odkaz = odkazy.pop(0)
                        relativni_url = prvni_odkaz.get('href')  # Získání neúplné url z odkazu
                        druha_url = sestav_url(prvni_url, relativni_url)  # Sestavení úplné url

                        radek_data = prvni_bunka.get_text().strip() + ";" + druha_bunka.get_text().strip() #spojeni prvni a druhy bunky do radek_datek
                        seznam_stran = zpracuj_podrobnosti(druha_url, f, radek_data, cislo_radku, seznam_stran)  # Zpracování podrobností a vrácení seznamu stran
                        # Pokud je zpracováván první řádek a seznam stran není prázdný názvy stran se zapíší do CSV souboru
            if cislo_radku == 1 and seznam_stran: 
                f.write(";".join(seznam_stran))
                f.write("\n")
    else:
        print("Nepodařilo se stáhnout data")

# Funkce pro zpracování podrobných dat z druhé URL
def zpracuj_podrobnosti(druha_url, soubor, radek_data, cislo_radku, seznam_stran):
    response = requests.get(druha_url)  # Odeslání HTTP GET požadavku

    if response.status_code == 200:  
        soup = BeautifulSoup(response.content, 'html.parser') # Zpracování pomocí soup
        radky = soup.find_all('tr')  # Vyhledání všech řádků tabulky

        radek_info = "" # Sem se uloží info o radcich
        seznam_hlasu = [] # Seznam kde se uloží hlasy
        for radek in radky:
            bunky = radek.find_all("td")  # Vyhledání všech buněk v řádku

            if len(bunky) == 9:  # Pokud řádek obsahuje 9 buněk
                prvni_bunka = bunky.pop(3) #Zpracuje se 3 buňka
                druha_bunka = bunky.pop(3) #6 buňka
                platne_hlasy_bunka = bunky.pop(5) #9 buňka
                radek_info = prvni_bunka.get_text().strip() + ";" + druha_bunka.get_text().strip() + ";" + platne_hlasy_bunka.get_text().strip() #Spojí zpracováváné buňky a uloží do radek_info
            if len(bunky) == 5:  # Pokud řádek obsahuje 5 buněk
                nazev_strany = bunky.pop(1) #Zpracuje se 2
                hlasy_strany = bunky.pop(1) #3 buňka
                if cislo_radku == 1: #Když je cislo radku 1 
                    seznam_stran.append(nazev_strany.get_text().strip())  # Přidá název strany
                seznam_hlasu.append(hlasy_strany.get_text().strip())  # Přidá hlasy strany


        # Zápis dat do souboru
        soubor.write(radek_data + ";" + radek_info + ";" + ";".join(seznam_hlasu)) #Spojí se všechna data a zapíší se do souboru
        soubor.write("\n") #Každý řádek se ukončí nový řádek
        return seznam_stran
    else:
        print("Nepodařilo se stáhnout data")
        return seznam_stran

# Hlavní funkce skriptu
def hlavni(url, soubor, strany_url): #Stará o stažení dat z webové stránky, zpracováním a uložením do souboru
    zpracuj_data(url, soubor, strany_url)

if __name__ == '__main__':
    # Přidání poviných argumentů
    parser = argparse.ArgumentParser(description='Skript pro web scraping')
    parser.add_argument('url', type=str, help='URL stránky pro stažení') #Povinný argument s url odkud chci data čerpat
    parser.add_argument('strany_url', type=str, help='URL pro získání názvů stran') #Poviný argument s url kde jsou strany
    parser.add_argument('soubor', type=str, help='Výstupní soubor') #Povinný argument s názvem stran
    args = parser.parse_args() #Uložení argumentů do args
    hlavni(args.url, args.soubor, args.strany_url) 