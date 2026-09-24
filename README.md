# Volby Scraper

Python skript, který stahuje výsledky parlamentních voleb z oficiálního portálu [volby.gov.cz](https://volby.gov.cz) a ukládá je do přehledného CSV souboru.

## Co skript dělá

1. Načte zadanou stránku s přehledem obcí (např. za okres nebo kraj)
2. Pro každou obec dohledá její detailní výsledkovou stránku
3. Z ní vytáhne:
   - počet voličů v seznamu
   - počet vydaných obálek
   - počet platných hlasů
   - počet hlasů pro každou politickou stranu/hnutí
4. Vše uloží do jednoho CSV souboru — jeden řádek na obec

## Použité technologie

- Python 3
- [requests](https://pypi.org/project/requests/) — stahování HTML stránek
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) — parsování HTML

## Instalace

1. Naklonuj si repozitář:
```bash
   git clone https://github.com/Lahouir-23/Volby_scraper.git
   cd Volby_scraper
```

2. (Volitelné) Vytvoř a aktivuj virtuální prostředí:
```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
```

3. Nainstaluj závislosti:
```bash
   pip install -r requirements.txt
```

## Použití

Skript se spouští ze terminálu se dvěma argumenty — URL adresou přehledové stránky obcí a jménem výstupního CSV souboru:

```bash
python Scraping_volby.py <URL_prehledu_obci> <vystupni_soubor.csv>
```

Příklad:
```bash
python Scraping_volby.py "https://volby.gov.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=..." vysledky.csv
```

> URL musí vést na přehledovou stránku obcí v rámci portálu `volby.gov.cz` (systém `ps2017nss`), odkud skript dokáže dohledat odkazy na jednotlivé obce.

## Formát výstupu

Výsledné CSV obsahuje jeden řádek na obec s těmito sloupci:

| kod obce | nazev | volici | obalky | hlasy | Strana 1 | Strana 2 | ... |
|---|---|---|---|---|---|---|---|

Sloupce s jednotlivými stranami se generují automaticky podle toho, jaké strany se objevily ve výsledcích první zpracované obce.

## Poznámka

Skript je napsaný pro konkrétní strukturu stránek portálu `volby.gov.cz` (systém `ps2017nss`) — při změně struktury webu nebo použití na jiný typ voleb může být potřeba selektory (`headers="sa2"`, `class="overflow_name"` apod.) upravit.
