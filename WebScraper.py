"""
WebScraper.py: třetí projekt 
author: Petr Svetr
email: petr.svetr@gmail.com
discord: Petr Svetr#4490
"""

import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_results(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Najdeme tabulku s výsledky voleb
    table = soup.find('table', {'class': 'table'})
    
    # Získáme názvy všech stran
    header_row = table.find_all('tr')[1]
    headers = header_row.find_all('th')[1:]  # První th je prázdný
    
    party_names = [header.text.strip() for header in headers]
    
    # Získáme data z řádků tabulky
    rows = table.find_all('tr')[2:]  # Přeskočíme první dva řádky, které obsahují hlavičky
    
    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append(cols)
    
    return data, party_names

def save_to_csv(data, party_names, output_file):
    # Definujeme sloupce podle očekávané struktury
    columns = ['code', 'location', 'registered', 'envelopes', 'valid'] + party_names
    
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Použití: WebScraper.py <URL> <výstupní_soubor>")
        sys.exit(1)
    
    url = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        data, party_names = fetch_results(url)
        save_to_csv(data, party_names, output_file)
        print(f"Výsledky uloženy do {output_file}")
    except Exception as e:
        print(f"Došlo k chybě: {e}")
        sys.exit(1)