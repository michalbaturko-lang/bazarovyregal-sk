#!/usr/bin/env python3
"""
Oprava zbývajících českých textů na slovenštinu
"""

import os
import re

# Dodatečné překlady
ADDITIONAL_TRANSLATIONS = {
    # Meta a popisy
    'Jsme tu pro vás': 'Sme tu pre vás',
    'Odpovídáme na vaše dotazy': 'Odpovedáme na vaše otázky',
    'kovové regály musí pryč': 'kovové regály musia preč',
    'Skladem přes': 'Skladom cez',
    'jsou navrženy tak, aby splnily ty nejnáročnější požadavky': 'sú navrhnuté tak, aby splnili tie najnáročnejšie požiadavky',
    'snadnou montáž a dlouhou životnost': 'jednoduchú montáž a dlhú životnosť',

    # Obecné fráze
    'Zdarma nad': 'Zadarmo nad',
    'Zdarma': 'Zadarmo',
    'zdarma': 'zadarmo',
    'zboží': 'tovar',
    'Zboží': 'Tovar',
    'se zárukou': 'so zárukou',
    'široký výběr': 'široký výber',
    'rozměrů a barev': 'rozmerov a farieb',
    'bezšroubová montáž': 'bezskrutková montáž',
    'nastavitelná výška polic': 'nastaviteľná výška políc',

    # Produkty
    'Regál': 'Regál',
    'čierný': 'čierny',
    'černý': 'čierny',
    'bílý': 'biely',
    'profesionální': 'profesionálny',
    'zinkovaný': 'zinkovaný',

    # Povrchy
    'lakovaný': 'lakovaný',
    'Lakovaný': 'Lakovaný',

    # Kontakt
    'Odpovíme vám': 'Odpovieme vám',
    'dotazy': 'otázky',
    'Dotazy': 'Otázky',

    # Footer
    'Reklamace a vrácení': 'Reklamácia a vrátenie',

    # Další chybějící
    'nosnosti': 'nosnosti',
    'celý regál': 'celý regál',
    'vybrat': 'vybrať',
    'koupit': 'kúpiť',
    'Koupit': 'Kúpiť',
    'Nakoupit': 'Nakúpiť',
    'nakoupit': 'nakúpiť',
    'dodání': 'dodanie',
    'Dodání': 'Dodanie',
    'doručení': 'doručenie',
    'Doručení': 'Doručenie',
    'objednat': 'objednať',
    'Objednat': 'Objednať',
    'přidat': 'pridať',
    'Přidat': 'Pridať',
    'odeslat': 'odoslať',
    'Odeslat': 'Odoslať',
    'vložit': 'vložiť',
    'Vložit': 'Vložiť',
    'vyplnit': 'vyplniť',
    'Vyplnit': 'Vyplniť',
    'potvrdit': 'potvrdiť',
    'Potvrdit': 'Potvrdiť',
    'zobrazit': 'zobraziť',
    'Zobrazit': 'Zobraziť',
    'zvolit': 'zvoliť',
    'Zvolit': 'Zvoliť',
    'najít': 'nájsť',
    'Najít': 'Nájsť',
    'hledat': 'hľadať',
    'Hledat': 'Hľadať',
    'změnit': 'zmeniť',
    'Změnit': 'Zmeniť',
    'stojí': 'stojí',
    'položky': 'položky',
    'produkt': 'produkt',
    'Produkt': 'Produkt',
    'výrobek': 'výrobok',
    'Výrobek': 'Výrobok',
    'záruka': 'záruka',
    'Záruka': 'Záruka',
    'sleva': 'zľava',
    'Sleva': 'Zľava',
    'slevy': 'zľavy',
    'Slevy': 'Zľavy',
    'doprava': 'doprava',
    'Doprava': 'Doprava',
    'platba': 'platba',
    'Platba': 'Platba',
    'objednávka': 'objednávka',
    'Objednávka': 'Objednávka',
    'košík': 'košík',
    'Košík': 'Košík',

    # Slovesné tvary
    'jsme': 'sme',
    'Jsme': 'Sme',
    'jste': 'ste',
    'Jste': 'Ste',
    'máte': 'máte',
    'Máte': 'Máte',
    'můžete': 'môžete',
    'Můžete': 'Môžete',
    'najdete': 'nájdete',
    'Najdete': 'Nájdete',
    'nabízíme': 'ponúkame',
    'Nabízíme': 'Ponúkame',
    'doporučujeme': 'odporúčame',
    'Doporučujeme': 'Odporúčame',
    'garantujeme': 'garantujeme',
    'Garantujeme': 'Garantujeme',

    # Přídavná jména
    'nejlepší': 'najlepšie',
    'Nejlepší': 'Najlepšie',
    'nejnižší': 'najnižšia',
    'Nejnižší': 'Najnižšia',
    'nejvyšší': 'najvyššia',
    'Nejvyšší': 'Najvyššia',
    'levnější': 'lacnejšie',
    'Levnější': 'Lacnejšie',
    'dražší': 'drahšie',
    'Dražší': 'Drahšie',
    'větší': 'väčší',
    'Větší': 'Väčší',
    'menší': 'menší',
    'Menší': 'Menší',
    'širší': 'širší',
    'Širší': 'Širší',
    'užší': 'užší',
    'Užší': 'Užší',
    'vyšší': 'vyššia',
    'Vyšší': 'Vyššia',
    'nižší': 'nižšia',
    'Nižší': 'Nižšia',

    # Číslovky a jednotky
    'tisíce': 'tisíce',
    'Tisíce': 'Tisíce',
    'stovky': 'stovky',
    'Stovky': 'Stovky',
    'desítky': 'desiatky',
    'Desítky': 'Desiatky',

    # Čas
    'dnes': 'dnes',
    'Dnes': 'Dnes',
    'zítra': 'zajtra',
    'Zítra': 'Zajtra',
    'včera': 'včera',
    'Včera': 'Včera',
    'teď': 'teraz',
    'Teď': 'Teraz',
    'právě': 'práve',
    'Právě': 'Práve',
    'ihned': 'ihneď',
    'Ihned': 'Ihneď',
    'brzy': 'čoskoro',
    'Brzy': 'Čoskoro',

    # Spojky a předložky
    'nebo': 'alebo',
    'Nebo': 'Alebo',
    'ale': 'ale',
    'Ale': 'Ale',
    'protože': 'pretože',
    'Protože': 'Pretože',
    'pokud': 'ak',
    'Pokud': 'Ak',
    'když': 'keď',
    'Když': 'Keď',
    'jestli': 'ak',
    'Jestli': 'Ak',

    # Zájmena
    'vy': 'vy',
    'Vy': 'Vy',
    'vás': 'vás',
    'Vás': 'Vás',
    'vám': 'vám',
    'Vám': 'Vám',
    'váš': 'váš',
    'Váš': 'Váš',
    'vaše': 'vaše',
    'Vaše': 'Vaše',
    'vaši': 'vašu',
    'Vaši': 'Vašu',

    # Místní výrazy
    'celé České republice': 'celom Slovensku',
    'celé ČR': 'celom SR',
    'v Česku': 'na Slovensku',
    'do Česka': 'na Slovensko',
    'z Česka': 'zo Slovenska',

    # Opravy specifických frází
    'Čeština': 'Slovenčina',
    'češtině': 'slovenčine',
    'český': 'slovenský',
    'Český': 'Slovenský',
    'české': 'slovenské',
    'České': 'Slovenské',
    'českého': 'slovenského',
    'Českého': 'Slovenského',
    'čeština': 'slovenčina',

    # Opravy konce slov
    'ích': 'ích',
    'ými': 'ými',
    'ími': 'ími',
}

def fix_file(content):
    """Opraví zbývající české texty"""
    for czech, slovak in ADDITIONAL_TRANSLATIONS.items():
        content = content.replace(czech, slovak)
    return content

def main():
    target_dir = '/sessions/exciting-serene-rubin/mnt/Bazarovyregalsk'
    fixed = 0

    # Opravíme hlavní soubory
    for filename in os.listdir(target_dir):
        if filename.endswith('.html'):
            filepath = os.path.join(target_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            fixed_content = fix_file(content)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            fixed += 1

    # Opravíme SEO stránky
    seo_dir = os.path.join(target_dir, 'seo')
    if os.path.exists(seo_dir):
        for filename in os.listdir(seo_dir):
            if filename.endswith('.html'):
                filepath = os.path.join(seo_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    fixed_content = fix_file(content)

                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(fixed_content)
                    fixed += 1
                except:
                    pass

    print(f"✅ Opraveno {fixed} souborů")

if __name__ == '__main__':
    main()
