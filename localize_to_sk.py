#!/usr/bin/env python3
"""
Lokalizační skript pro převod českého webu bazarovyregal.cz na slovenskou verzi bazarovyregal.sk
"""

import os
import re
import shutil

# Slovník pro překlad českých textů do slovenštiny
TRANSLATIONS = {
    # Doména a značka
    'Bazarovyregal.cz': 'Bazarovyregal.sk',
    'bazarovyregal.cz': 'bazarovyregal.sk',
    'Bazarovyregal<span class="text-primary-500">.cz</span>': 'Bazarovyregal<span class="text-primary-500">.sk</span>',

    # Měna - Kč na € (euro)
    'Kč': '€',
    '99 €': '3,99 €',  # Doprava
    '2000 €': '79 €',  # Limit pro dopravu zdarma
    '489 €': '19,49 €',
    '599 €': '23,99 €',
    '622 €': '24,99 €',
    '626 €': '24,99 €',
    '649 €': '25,99 €',
    '663 €': '26,49 €',
    '569 €': '22,79 €',
    '689 €': '27,49 €',
    '739 €': '29,49 €',
    '759 €': '30,29 €',
    '849 €': '33,99 €',
    '899 €': '35,99 €',
    '1 149 €': '45,99 €',
    '1 478 €': '59,19 €',
    '2 949 €': '117,99 €',
    '3 459 €': '138,39 €',
    '1000 €': '39 €',
    '1198 €': '47,99 €',
    '1258 €': '50,39 €',
    '1298 €': '51,99 €',
    '1378 €': '55,19 €',
    '1518 €': '60,79 €',
    '1698 €': '67,99 €',
    '1798 €': '71,99 €',
    '2298 €': '91,99 €',
    '400 €': '15,99 €',
    '611 €': '24,49 €',
    '100 €': '3,99 €',

    # Telefonní prefix
    '+420 123 456 789': '+421 123 456 789',
    '+420123456789': '+421123456789',
    'tel:+420123456789': 'tel:+421123456789',

    # Email
    'info@bazarovyregal.cz': 'info@bazarovyregal.sk',
    'mailto:info@bazarovyregal.cz': 'mailto:info@bazarovyregal.sk',

    # HTML lang attribute
    'lang="cs"': 'lang="sk"',

    # Lokace
    'Praha 5': 'Bratislava',
    'Praha': 'Bratislava',
    'Česká republika': 'Slovenská republika',
    'České republiky': 'Slovenska',
    'Českou republiku': 'Slovensko',
    'ČR': 'SR',
    'Brno': 'Košice',
    'Ostrava': 'Prešov',
    'Plzeň': 'Žilina',
    'Liberec': 'Nitra',
    'Olomouc': 'Banská Bystrica',
    'České Budějovice': 'Trnava',
    'Hradec Králové': 'Trenčín',

    # Navigace a UI
    'Úvod': 'Úvod',  # Same in Slovak
    'Všechny regály': 'Všetky regály',
    'O nás': 'O nás',  # Same
    'FAQ': 'FAQ',  # Same
    'Kontakt': 'Kontakt',  # Same
    'Košík': 'Košík',  # Same
    'Do košíku': 'Do košíka',
    'Hledat regály': 'Hľadať regály',
    'Hledat v FAQ': 'Hľadať v FAQ',
    'Hledat': 'Hľadať',
    'HLEDAT': 'HĽADAŤ',

    # Urgency bar
    'LIKVIDACE SKLADU': 'LIKVIDÁCIA SKLADU',
    'Likvidace skladu': 'Likvidácia skladu',
    'Slevy až 40%': 'Zľavy až 40%',
    'Akce končí za:': 'Akcia končí za:',
    'Doprava ZDARMA nad': 'Doprava ZADARMO nad',
    'Doprava zdarma nad': 'Doprava zadarmo nad',

    # Hlavní texty
    'Všechny regály musí pryč!': 'Všetky regály musia preč!',
    'Pouze nové a nerozbalené': 'Iba nové a nerozbalené',
    '7 let záruka': '7 rokov záruka',
    'Záruka 7 let': 'Záruka 7 rokov',
    '7letou zárukou': '7-ročnou zárukou',
    '7 let': '7 rokov',
    '30 dní': '30 dní',  # Same
    '30 dní na vrácení': '30 dní na vrátenie',
    '14 dní na vrácení': '14 dní na vrátenie',
    '24 hodin': '24 hodín',
    '24h': '24h',  # Same
    'do 24h': 'do 24h',
    'Expedice do 24h': 'Expedícia do 24h',

    # Countdown
    'DNY': 'DNI',
    'dny': 'dni',
    'HOD': 'HOD',  # Same
    'hod': 'hod',  # Same
    'MIN': 'MIN',  # Same
    'min': 'min',  # Same
    'SEK': 'SEK',  # Same

    # Trust bar
    'skladem': 'skladom',
    'Skladem': 'Skladom',
    '10 000+ skladem': '10 000+ skladom',
    'Na všechny regály': 'Na všetky regály',
    'Doprava od': 'Doprava od',  # Same
    'Nové a nerozbalené': 'Nové a nerozbalené',  # Same
    '100% kvalita': '100% kvalita',  # Same

    # Kategorie
    'Vyberte si kategorii': 'Vyberte si kategóriu',
    'Máme regál pro každé využití': 'Máme regál pre každé využitie',
    'Regály do domu': 'Regály do domu',  # Same
    'Regály do skladu': 'Regály do skladu',  # Same
    'Regály do garáže': 'Regály do garáže',  # Same
    'Regály do kanceláře': 'Regály do kancelárie',
    'Profesionální regály': 'Profesionálne regály',
    'produktů': 'produktov',
    'Do domu': 'Do domu',  # Same
    'Do skladu': 'Do skladu',  # Same
    'Do garáže': 'Do garáže',  # Same

    # Popis kategorií
    'Obývák, ložnice, spíž, dětský pokoj': 'Obývačka, spálňa, špajza, detská izba',
    'Profesionální regály, vysoká nosnost': 'Profesionálne regály, vysoká nosnosť',
    'Zinkované, odolné proti vlhkosti': 'Zinkované, odolné proti vlhkosti',  # Same
    'Šanony, dokumenty, archiv': 'Šanóny, dokumenty, archív',

    # Produkty
    'TOP prodeje': 'TOP predaje',
    'Nejprodávanější regály': 'Najpredávanejšie regály',
    'Zobrazit všech': 'Zobraziť všetky',
    'Zobrazit dalších': 'Zobraziť ďalšie',
    'produktů': 'produktov',
    'Zinkovaný': 'Zinkovaný',  # Same
    'Lakovaný': 'Lakovaný',  # Same
    'Pozinkovaný': 'Pozinkovaný',  # Same
    'černý': 'čierny',
    'Černý': 'Čierny',
    'Černá': 'Čierna',
    'bílý': 'biely',
    'Bílý': 'Biely',
    'Bílá': 'Biela',
    'červený': 'červený',  # Same
    'Červený': 'Červený',  # Same
    'Červená': 'Červená',  # Same
    'modrý': 'modrý',  # Same
    'Modrý': 'Modrý',  # Same
    'Modrá': 'Modrá',  # Same
    '-policový': '-policový',  # Same
    'nosnost': 'nosnosť',
    'Nosnost': 'Nosnosť',
    'kg': 'kg',  # Same
    'cm': 'cm',  # Same
    'mm': 'mm',  # Same

    # Proč nakoupit u nás
    'Proč nakoupit u nás?': 'Prečo nakúpiť u nás?',
    'Tisíce spokojených zákazníků nám důvěřuje': 'Tisíce spokojných zákazníkov nám dôveruje',
    'Garance nejnižší ceny': 'Garancia najnižšej ceny',
    'Najdete levněji? Dorovnáme cenu a dáme slevu 5% navíc.': 'Nájdete lacnejšie? Dorovnáme cenu a dáme zľavu 5% navyše.',
    'Expedice do 24h': 'Expedícia do 24h',
    'Objednáte dnes, zítra odesíláme. Doručení do 2-3 dnů.': 'Objednáte dnes, zajtra odosielame. Doručenie do 2-3 dní.',
    'Montáž za 10 minut': 'Montáž za 10 minút',
    'Bezšroubový systém. Zvládne to i začátečník bez nářadí.': 'Bezskrutkový systém. Zvládne to aj začiatočník bez náradia.',
    '30 dní na vrácení': '30 dní na vrátenie',
    'Nejste spokojeni? Vrátíme vám peníze bez zbytečných otázek.': 'Nie ste spokojní? Vrátime vám peniaze bez zbytočných otázok.',

    # Jak to funguje
    'Jak to funguje?': 'Ako to funguje?',
    '3 jednoduché kroky k vašemu novému regálu': '3 jednoduché kroky k vášmu novému regálu',
    'Vyberte regál': 'Vyberte regál',  # Same
    'Prohlédněte si nabídku a vyberte regál podle vašich potřeb.': 'Prezrite si ponuku a vyberte regál podľa vašich potrieb.',
    'Objednejte online': 'Objednajte online',
    'Přidejte do košíku a dokončete objednávku. Platba kartou nebo dobírkou.': 'Pridajte do košíka a dokončite objednávku. Platba kartou alebo dobierkou.',
    'Doručíme domů': 'Doručíme domov',
    'Do 2-3 dnů máte regál doma. Montáž zvládnete za 10 minut.': 'Do 2-3 dní máte regál doma. Montáž zvládnete za 10 minút.',

    # Recenze
    'z 5 hvězdiček': 'z 5 hviezdičiek',
    'Na základě': 'Na základe',
    'hodnocení od zákazníků': 'hodnotení od zákazníkov',
    'Skvělá kvalita za super cenu!': 'Skvelá kvalita za super cenu!',
    'Ověřený nákup': 'Overený nákup',
    'Přečíst všech': 'Prečítať všetky',
    'recenzí': 'recenzií',

    # SEO sekce
    'Kovové regály za výprodejové ceny': 'Kovové regály za výpredajové ceny',
    'Hledáte kvalitní kovové regály za nejlepší ceny?': 'Hľadáte kvalitné kovové regály za najlepšie ceny?',
    'Právě probíhá': 'Práve prebieha',
    'likvidace skladu': 'likvidácia skladu',
    'všechny regály musí pryč': 'všetky regály musia preč',
    'Nabízíme pouze': 'Ponúkame iba',
    'nové a nerozbalené': 'nové a nerozbalené',  # Same
    'regály s': 'regály so',
    'zárukou': 'zárukou',  # Same
    'Díky tomu, že likvidujeme zásoby': 'Vďaka tomu, že likvidujeme zásoby',
    'můžeme nabídnout slevy až 40% oproti běžným cenám': 'môžeme ponúknuť zľavy až 40% oproti bežným cenám',
    'V nabídce najdete regály pro domácnost i profesionální využití': 'V ponuke nájdete regály pre domácnosť aj profesionálne využitie',
    'Lakované regály': 'Lakované regály',  # Same
    'jsou ideální do interiéru': 'sú ideálne do interiéru',
    'Zinkované regály jsou vhodné do vlhkého prostředí jako garáž nebo sklep': 'Zinkované regály sú vhodné do vlhkého prostredia ako garáž alebo pivnica',
    'splní i ty nejnáročnější požadavky': 'splnia aj tie najnáročnejšie požiadavky',

    # Co nabízíme
    'Co nabízíme:': 'Čo ponúkame:',
    'Regály do domu, garáže, skladu a kanceláře': 'Regály do domu, garáže, skladu a kancelárie',
    'Nosnost od 700 kg do 1200 kg': 'Nosnosť od 700 kg do 1200 kg',
    'Lakované i zinkované povrchy': 'Lakované aj zinkované povrchy',
    'Bezšroubová montáž za 10 minut': 'Bezskrutková montáž za 10 minút',
    'Nastavitelná výška polic': 'Nastaviteľná výška políc',

    # Proč nakoupit u nás
    'Proč nakoupit u nás:': 'Prečo nakúpiť u nás:',
    'Garance nejnižší ceny na trhu': 'Garancia najnižšej ceny na trhu',
    'Expedice do 24 hodin': 'Expedícia do 24 hodín',
    '30 dní na vrácení bez udání důvodu': '30 dní na vrátenie bez udania dôvodu',

    # Urgency
    'Nečekejte, dokud nebudou ty nejlepší kousky pryč': 'Nečakajte, kým nebudú tie najlepšie kúsky preč',
    'Počet kusů je omezený a zásoby se rychle tenčí': 'Počet kusov je obmedzený a zásoby sa rýchlo míňajú',
    'Objednejte ještě dnes a využijte likvidační ceny!': 'Objednajte ešte dnes a využite likvidačné ceny!',

    # Newsletter
    'Získejte slevu 10% navíc!': 'Získajte zľavu 10% navyše!',
    'Přihlaste se k odběru novinek a získejte slevový kód na první objednávku.': 'Prihláste sa na odber noviniek a získajte zľavový kód na prvú objednávku.',
    'Váš e-mail': 'Váš e-mail',  # Same
    'Chci slevu': 'Chcem zľavu',
    'Žádný spam. Odhlásit se můžete kdykoli.': 'Žiadny spam. Odhlásiť sa môžete kedykoľvek.',

    # Footer
    'Kategorie': 'Kategórie',
    'Informace': 'Informácie',
    'Často kladené otázky': 'Často kladené otázky',  # Same
    'Doprava a platba': 'Doprava a platba',  # Same
    'Obchodní podmínky': 'Obchodné podmienky',
    'Ochrana osobních údajů': 'Ochrana osobných údajov',
    'Platební metody:': 'Platobné metódy:',
    'Karta': 'Karta',  # Same
    'Převod': 'Prevod',
    'Dobírka': 'Dobierka',
    'Volejte': 'Volajte',
    'Všechna práva vyhrazena': 'Všetky práva vyhradené',
    'Nákup probíhá na': 'Nákup prebieha na',

    # FAQ
    'Často kladené dotazy': 'Často kladené otázky',
    'MÁME ODPOVĚDI NA VŠECHNY VAŠE OTÁZKY': 'MÁME ODPOVEDE NA VŠETKY VAŠE OTÁZKY',
    'Všechno co potřebujete vědět o nákupu, dopravě, montáži a záruce': 'Všetko čo potrebujete vedieť o nákupe, doprave, montáži a záruke',
    'Jakou máte otázku?': 'Akú máte otázku?',
    'Začněte psát klíčové slovo nebo si vyberte kategorii níže': 'Začnite písať kľúčové slovo alebo si vyberte kategóriu nižšie',
    'Nejčastějších otázek': 'Najčastejších otázok',
    'Odpověď na e-mail': 'Odpoveď na e-mail',
    'Záruka na regály': 'Záruka na regály',  # Same
    'Vrácení zboží': 'Vrátenie tovaru',
    'Vyberte kategorii:': 'Vyberte kategóriu:',
    'Všechny otázky': 'Všetky otázky',
    'Objednávka a platba': 'Objednávka a platba',  # Same
    'Doprava': 'Doprava',  # Same
    'Produkty': 'Produkty',  # Same
    'Montáž': 'Montáž',  # Same
    'Záruka a reklamace': 'Záruka a reklamácie',

    # FAQ - Objednávka
    'Jak objednat?': 'Ako objednať?',
    'Objednávka je velmi jednoduchá:': 'Objednávka je veľmi jednoduchá:',
    'Vyberte si regál na našem webu': 'Vyberte si regál na našom webe',
    'Přidejte regál do košíku': 'Pridajte regál do košíka',
    'Vyplňte doručovací adresu': 'Vyplňte doručovaciu adresu',
    'Zvolte způsob platby': 'Zvoľte spôsob platby',
    'karta, převod, dobírka': 'karta, prevod, dobierka',
    'Potvrďte objednávku': 'Potvrďte objednávku',  # Same
    'Všechny nákupy probíhají na': 'Všetky nákupy prebiehajú na',
    'což je matka firma se stejným systémem a zárukami': 'čo je materská firma s rovnakým systémom a zárukami',

    'Jaké jsou platební možnosti?': 'Aké sú platobné možnosti?',
    'přijímáme následující způsoby platby': 'prijímame nasledujúce spôsoby platby',
    'Platba kartou': 'Platba kartou',  # Same
    'okamžitá platba, nejrychlejší zpracování objednávky': 'okamžitá platba, najrýchlejšie spracovanie objednávky',
    'Převod na účet': 'Prevod na účet',
    'můžete zaplatit převodem z banky': 'môžete zaplatiť prevodom z banky',
    'zaplatíte při doručení zboží, bez poplatku': 'zaplatíte pri doručení tovaru, bez poplatku',
    'Všechny metody jsou bezpečné a ověřené': 'Všetky metódy sú bezpečné a overené',
    'Objednávka je uložena až po potvrzení platby': 'Objednávka je uložená až po potvrdení platby',

    'Můžu objednat na firmu?': 'Môžem objednať na firmu?',
    'Ano, zcela bez problému!': 'Áno, úplne bez problémov!',
    'Při objednávce si můžete vybrat jako zákazník': 'Pri objednávke si môžete vybrať ako zákazník',
    'Fyzickou osobu': 'Fyzickú osobu',
    'jméno a příjmení': 'meno a priezvisko',
    'Právnickou osobu': 'Právnickú osobu',
    'obchodní název a IČO': 'obchodný názov a IČO',
    'Pokud objednáváte na IČO': 'Ak objednávate na IČO',
    'stačí to uvést při objednávce': 'stačí to uviesť pri objednávke',
    'Faktura se vygeneruje automaticky': 'Faktúra sa vygeneruje automaticky',

    'Je možné vyzvednout osobně?': 'Je možné vyzdvihnúť osobne?',
    'Ano, ale pouze v': 'Áno, ale iba v',
    'po předchozí domluvě': 'po predchádzajúcej dohode',
    'Máme skladiště v': 'Máme sklad v',
    'kde si můžete zboží vyzvednout osobně': 'kde si môžete tovar vyzdvihnúť osobne',
    'Tímto způsobem ušetříte na dopravě': 'Týmto spôsobom ušetríte na doprave',
    'Vyzvednutí je bezplatné': 'Vyzdvihnutie je bezplatné',
    'Domluvte se s námi telefonicky': 'Dohodnite sa s nami telefonicky',
    'Vyzvednutí je možné': 'Vyzdvihnutie je možné',
    'Po-Pá 8:00-16:00': 'Po-Pi 8:00-16:00',
    'Po-Pá 8:00 - 16:00': 'Po-Pi 8:00 - 16:00',
    'Po-Pá': 'Po-Pi',
    'So-Ne': 'So-Ne',  # Same
    'Zavřeno': 'Zatvorené',

    # FAQ - Doprava
    'Kolik stojí doprava?': 'Koľko stojí doprava?',
    'Cena dopravy je na základě hmotnosti a vzdálenosti': 'Cena dopravy je na základe hmotnosti a vzdialenosti',
    'Základní sazba': 'Základná sadzba',
    'v tuto cenu máte zahrnuty regály do ~30 kg': 'v túto cenu máte zahrnuté regály do ~30 kg',
    'obvyklý regál': 'obvyklý regál',  # Same
    'Těžší regály': 'Ťažšie regály',
    'cena se vypočte podle hmotnosti při objednávce': 'cena sa vypočíta podľa hmotnosti pri objednávke',
    'pro objednávky nad': 'pre objednávky nad',
    'Nejčastěji vás stojí doprava pouhých': 'Najčastejšie vás stojí doprava iba',
    'A pokud nakupujete více regálů, doprava je obvykle zdarma': 'A ak nakupujete viac regálov, doprava je obvykle zadarmo',

    'Jak dlouho trvá doručení?': 'Ako dlho trvá doručenie?',
    'Naše doručovací časy': 'Naše doručovacie časy',
    'Expediční lhůta': 'Expedičná lehota',
    'Do 24 hodin od potvrzení objednávky': 'Do 24 hodín od potvrdenia objednávky',
    'Doručení': 'Doručenie',
    '2-3 pracovní dny': '2-3 pracovné dni',
    'Sledování': 'Sledovanie',
    'Dostanete SMS s číslem balíku a odhadem doručení': 'Dostanete SMS s číslom balíka a odhadom doručenia',
    'Přesný čas doručení vám potvrdí přepravce 24 hodin před doručením SMS': 'Presný čas doručenia vám potvrdí prepravca 24 hodín pred doručením SMS',
    'Objednáte-li do 14:00, objednávka se expeduje do konce dne!': 'Objednáte-li do 14:00, objednávka sa expeduje do konca dňa!',

    'Kam doručujete?': 'Kam doručujete?',  # Same
    'Doručujeme do celé': 'Doručujeme do celého',
    'výběr konkrétního času': 'výber konkrétneho času',
    'Ostatní části': 'Ostatné časti',
    'doručení v pracovní dny': 'doručenie v pracovné dni',
    'Na adresu domu, kanceláře nebo skladu': 'Na adresu domu, kancelárie alebo skladu',
    'Také do horských oblastí': 'Tiež do horských oblastí',
    'nad 500 m nadmořské výšky': 'nad 500 m nadmorskej výšky',
    'Doručujeme přes ověřené přepravce': 'Doručujeme cez overených prepravcov',
    'které máme dlouhodobě smluvně zajištěny': 'ktoré máme dlhodobo zmluvne zabezpečené',
    'Česká pošta, GLS, PPL': 'Slovenská pošta, GLS, DPD',

    'Doručíte i na Slovensko?': 'Doručíte aj do Česka?',
    'Ano! Máme speciální web pro slovenské zákazníky.': 'Áno! Máme špeciálny web pre českých zákazníkov.',
    'Na Slovensku objednávejte na:': 'V Česku objednávajte na:',
    'Stejné produkty a ceny jako v ČR': 'Rovnaké produkty a ceny ako na Slovensku',
    'Slovenská podpora a fakturace': 'Česká podpora a fakturácia',
    'Doručení po celém Slovensku': 'Doručenie po celom Česku',
    'Záruka 7 let platí i na Slovensku': 'Záruka 7 rokov platí aj v Česku',

    # FAQ - Produkty
    'Jsou regály nové?': 'Sú regály nové?',
    'Ano, 100% nové a nerozbalené!': 'Áno, 100% nové a nerozbalené!',
    'Všechny regály, které prodáváme, jsou': 'Všetky regály, ktoré predávame, sú',
    'Zcela nové, nikdy předtím neprodané': 'Úplne nové, nikdy predtým nepredané',
    'V originálním balení od výrobce': 'V originálnom balení od výrobcu',
    'Bez poškození a defektů': 'Bez poškodenia a defektov',
    'Se všemi součástmi a návodem v češtině': 'So všetkými súčasťami a návodom v slovenčine',
    'Regály pocházejí z likvidace skladu': 'Regály pochádzajú z likvidácie skladu',
    'takže ceny jsou nižší než běžný obchod': 'takže ceny sú nižšie ako bežný obchod',
    'ale kvalita je stejně vysoká': 'ale kvalita je rovnako vysoká',

    'Jaká je nosnost regálů?': 'Aká je nosnosť regálov?',
    'Nosnost se liší podle typu regálu': 'Nosnosť sa líši podľa typu regálu',
    'Regály do domu (4-policové)': 'Regály do domu (4-policové)',  # Same
    '700 kg nosnosti': '700 kg nosnosti',  # Same
    '175 kg na jednu polici': '175 kg na jednu policu',
    'Regály do garáže (4-5 policový)': 'Regály do garáže (4-5 policový)',  # Same
    '700-875 kg nosnosti': '700-875 kg nosnosti',  # Same
    '1000-1200 kg nosnosti': '1000-1200 kg nosnosti',  # Same
    'Přesná nosnost je vždy uvedena v popisu produktu': 'Presná nosnosť je vždy uvedená v popise produktu',
    'Nosnost je stanovena pro rovnoměrně rozloženou váhu': 'Nosnosť je stanovená pre rovnomerne rozloženú váhu',

    'Z čeho jsou regály vyrobené?': 'Z čoho sú regály vyrobené?',
    'Naše regály se vyrábějí ze dvou základních materiálů': 'Naše regály sa vyrábajú z dvoch základných materiálov',
    'Ocelové regály (základní materiál)': 'Oceľové regály (základný materiál)',
    'Všechny regály mají ocelové nosné sloupy': 'Všetky regály majú oceľové nosné stĺpy',
    'čímž jsou extrémně pevné a odolné': 'čím sú extrémne pevné a odolné',
    'Ocelový rám je přepískován a pokryt kvalitní barvou': 'Oceľový rám je prepieskovavaný a pokrytý kvalitnou farbou',
    'v černé, bílé, červené nebo modré barvě': 'v čiernej, bielej, červenej alebo modrej farbe',
    'Vhodné do interiérů': 'Vhodné do interiérov',
    'Ocelový rám je pokryt zinkovou vrstvou metodou horké zinkování': 'Oceľový rám je pokrytý zinkovou vrstvou metódou horúceho zinkovania',
    'Odolává vlhkosti a korozi': 'Odolný voči vlhkosti a korózii',
    'Ideální do garáží a na zahrady': 'Ideálne do garáží a na záhrady',
    'Všechny typy mají stejnou nosnost a životnost': 'Všetky typy majú rovnakú nosnosť a životnosť',
    'Výběr záleží na použití a vzhledu': 'Výber závisí na použití a vzhľade',

    'Lze nastavit výšku polic?': 'Dá sa nastaviť výška políc?',
    'Ano, výška polic je nastavitelná!': 'Áno, výška políc je nastaviteľná!',
    'Krok nastavení': 'Krok nastavenia',
    'Po 3,5 cm': 'Po 3,5 cm',  # Same
    'Nastavení': 'Nastavenie',
    'Jednoduché vyjmutí a přesunutí police': 'Jednoduché vybratie a presunutie police',
    'Bez nářadí': 'Bez náradia',
    'Nemusíte nic rozebírat nebo montovat': 'Nemusíte nič rozoberať alebo montovať',
    'Počet pozic': 'Počet pozícií',
    'Typicky 5-6 pozic na výšku': 'Typicky 5-6 pozícií na výšku',
    'Díky tomu si můžete přizpůsobit regál přesně podle toho, co máte skladovat': 'Vďaka tomu si môžete prispôsobiť regál presne podľa toho, čo máte skladovať',
    'Můžete si vytvořit např. 3 vysoké mezery a 1 nízkou': 'Môžete si vytvoriť napr. 3 vysoké medzery a 1 nízku',

    # FAQ - Montáž
    'Je montáž složitá?': 'Je montáž zložitá?',
    'Ne! Montáž je velmi jednoduchá a trvá jen 10 minut.': 'Nie! Montáž je veľmi jednoduchá a trvá len 10 minút.',
    'Naše regály mají speciální systém bez šroubů': 'Naše regály majú špeciálny systém bez skrutiek',
    'bezšroubový': 'bezskrutkový',
    'Bez vrtání a šroubování': 'Bez vŕtania a skrutkovania',
    'Policie jednoduše vsuňete do sloupů': 'Police jednoducho vsunúte do stĺpov',
    'Bez elektrowerkzeuges': 'Bez elektrického náradia',
    'Nemusíte nic vrtat, elektřiny, vrtačky': 'Nemusíte nič vŕtať, elektriny, vŕtačky',
    'Bez pomoci': 'Bez pomoci',  # Same
    'Zvládnete to sami, není potřeba druhá osoba': 'Zvládnete to sami, nie je potrebná druhá osoba',
    'Čas': 'Čas',  # Same
    'Typicky 10 minut pro 4-policový regál': 'Typicky 10 minút pre 4-policový regál',
    'Skutečně to zvládne i dítě! Tisíce našich zákazníků montáž zvládly bez problému.': 'Skutočne to zvládne aj dieťa! Tisíce našich zákazníkov montáž zvládli bez problému.',

    'Potřebuji nářadí?': 'Potrebujem náradie?',
    'Ne, stačí vám gumová palička!': 'Nie, stačí vám gumová palička!',
    'Na montáž regálu potřebujete': 'Na montáž regálu potrebujete',
    'Gumová palička': 'Gumová palička',  # Same
    'aby ste polou lehčeji zasunuli do sloupů': 'aby ste policu ľahšie zasunuli do stĺpov',
    'Nic víc!': 'Nič viac!',
    'bez vrtačky, bez bitů, bez šroubováku': 'bez vŕtačky, bez bitov, bez skrutkovača',
    'Gumová palička se obvykle nedodává s regálem': 'Gumová palička sa obvykle nedodáva s regálom',
    'ale máte ji jistě doma': 'ale máte ju určite doma',
    'Pokud ne, stojí cca 100 Kč v každém hobbymarkt': 'Ak nie, stojí cca 4 € v každom hobbymarkete',

    'Je k dispozici návod?': 'Je k dispozícii návod?',
    'Ano! Návod je v balení a také online.': 'Áno! Návod je v balení a tiež online.',
    'V balení': 'V balení',  # Same
    'Tiskovný návod v češtině krok za krokem': 'Tlačený návod v slovenčine krok za krokom',
    'Obrázky': 'Obrázky',  # Same
    'Barevné, srozumitelné ilustrace': 'Farebné, zrozumiteľné ilustrácie',
    'Online video': 'Online video',  # Same
    'YouTube návod s postupem montáže': 'YouTube návod s postupom montáže',  # Same
    'Podpora': 'Podpora',  # Same
    'Kdybyste měli otázku, napište nám na': 'Ak by ste mali otázku, napíšte nám na',
    'Návod je tak jednoduchý, že se ani nemusíte koukat na video': 'Návod je tak jednoduchý, že sa ani nemusíte pozerať na video',
    'Ale je tam, pokud ho budete potřebovat!': 'Ale je tam, ak ho budete potrebovať!',

    # FAQ - Záruka
    'Jaká je záruka?': 'Aká je záruka?',
    '7 let záruka na všechny regály!': '7 rokov záruka na všetky regály!',
    'Záruka pokrývá': 'Záruka pokrýva',
    'Rozbitý nebo deformovaný ocelový rám': 'Rozbitý alebo deformovaný oceľový rám',
    'Prasklé nebo zlomené policie': 'Prasknuté alebo zlomené police',
    'Opotřebované nebo rezavé části': 'Opotrebované alebo hrdzavé časti',
    'Jakékoliv výrobní vady': 'Akékoľvek výrobné chyby',
    'Záruka se vztahuje na normální používání': 'Záruka sa vzťahuje na normálne používanie',
    'Pokud regál používáte přetížený': 'Ak regál používate preťažený',
    'víc než je uvedena nosnost': 'viac ako je uvedená nosnosť',
    'záruka se vztahuje na nižší nosnost': 'záruka sa vzťahuje na nižšiu nosnosť',
    '7 let je jednou z nejdelších záruk na trhu!': '7 rokov je jednou z najdlhších záruk na trhu!',

    'Co když mi regál nevyhovuje?': 'Čo ak mi regál nevyhovuje?',
    'Máte 30 dní na vrácení bez udání důvodu!': 'Máte 30 dní na vrátenie bez udania dôvodu!',
    'Pokud se vám regál nelíbí, vrátíte ho do 30 dnů': 'Ak sa vám regál nepáči, vrátite ho do 30 dní',
    'Vrácení je': 'Vrátenie je',
    'bezplatné': 'bezplatné',  # Same
    'my zaplatíme dopravu': 'my zaplatíme dopravu',  # Same
    'Peníze vám vrátíme do 14 dnů': 'Peniaze vám vrátime do 14 dní',
    'Regál se musí vrátit v původním stavu': 'Regál sa musí vrátiť v pôvodnom stave',
    'v krabici, nepoškozený': 'v krabici, nepoškodený',
    'Není potřeba udávat důvod': 'Nie je potrebné udávať dôvod',
    'Pokud se vám nelíbí barva, velikost nebo cokoli jiného - vrátíte to!': 'Ak sa vám nepáči farba, veľkosť alebo čokoľvek iné - vrátite to!',

    'Jak reklamovat?': 'Ako reklamovať?',
    'Máte problém s regálem? Postup reklamace:': 'Máte problém s regálom? Postup reklamácie:',
    'Napište nám e-mail:': 'Napíšte nám e-mail:',
    'Popište problém': 'Popíšte problém',
    'a přiložte fotografie': 'a priložte fotografie',
    'Číslo objednávky': 'Číslo objednávky',  # Same
    'najdete v e-mailu od nás': 'nájdete v e-maile od nás',
    'Čekání na odpověď:': 'Čakanie na odpoveď:',
    'Odpověď do 48 hodin': 'Odpoveď do 48 hodín',
    'Řešení:': 'Riešenie:',
    'Buď náhrada, vrácení peněz, nebo oprava': 'Buď náhrada, vrátenie peňazí, alebo oprava',
    'Kontakt pro reklamace:': 'Kontakt pre reklamácie:',

    # FAQ - O nás
    'O Bazarovyregal': 'O Bazarovyregal',
    'Kdo jste?': 'Kto ste?',
    'je': 'je',  # Same
    'prezentační web': 'prezentačný web',
    'pro nákupní platformu': 'pre nákupnú platformu',
    'Struktura:': 'Štruktúra:',
    'mateřská firma a hlavní e-shop': 'materská firma a hlavný e-shop',
    'prezentační web s lepším UX': 'prezentačný web s lepším UX',
    'verze pro slovenské zákazníky': 'verzia pre českých zákazníkov',
    'Všechny weby jsou spravovány stejným týmem': 'Všetky weby sú spravované rovnakým tímom',
    'Jsou úplně stejné záruky, ceny a služby': 'Sú úplne rovnaké záruky, ceny a služby',

    'Proč jsou ceny tak nízké?': 'Prečo sú ceny tak nízke?',
    'Ceny jsou nízké, protože probíhá likvidace skladu!': 'Ceny sú nízke, pretože prebieha likvidácia skladu!',
    'Důvody nižších cen:': 'Dôvody nižších cien:',
    'Máme': 'Máme',  # Same
    'velké přebytky zásob': 'veľké prebytky zásob',
    'regálů je více než potřeba': 'regálov je viac ako potreba',
    'Nákupy se nám': 'Nákupy sa nám',
    'hromadily v skladě': 'hromadili v sklade',
    'máme na ně místo': 'máme na ne miesto',
    'je nutná': 'je nutná',  # Same
    'musíme zboží co nejrychleji prodat': 'musíme tovar čo najrýchlejšie predať',
    'Marže je': 'Marža je',
    'nižší': 'nižšia',
    'počítáme na objem prodeje, ne na vysoký zisk': 'počítame na objem predaja, nie na vysoký zisk',
    'Nejedná se o levné regály': 'Nejedná sa o lacné regály',
    'Je to stejná kvalita a stejný výrobce jako normálně': 'Je to rovnaká kvalita a rovnaký výrobca ako normálne',
    'ale bez nadhodnocení ze strany běžného obchodu': 'ale bez nadhodnotenia zo strany bežného obchodu',

    'Jsou slevy skutečné?': 'Sú zľavy skutočné?',
    'Ano, všechny slevy jsou 100% skutečné!': 'Áno, všetky zľavy sú 100% skutočné!',
    'Procento slevy je vždy vypočteno': 'Percento zľavy je vždy vypočítané',
    'Oproti': 'Oproti',  # Same
    'originální ceně od výrobce': 'originálnej cene od výrobcu',
    'Nebo oproti': 'Alebo oproti',
    'standardní ceně v běžném obchodě': 'štandardnej cene v bežnom obchode',
    'si nenadzvedáme cenu a pak ji neslevujeme': 'si nenavyšujeme cenu a potom ju nezľavujeme',
    'Slevy jsou skutečné, ale počty kusů jsou omezené': 'Zľavy sú skutočné, ale počty kusov sú obmedzené',
    'Když se skončí, tak se skončí!': 'Keď sa skončia, tak sa skončia!',
    'Máme přes 10 000 ks skladem, ale to není neomezeno': 'Máme cez 10 000 ks skladom, ale to nie je neobmedzené',
    'Objednávejte včas!': 'Objednávajte včas!',

    # CTA sekce
    'Stále máte otázku?': 'Stále máte otázku?',  # Same
    'Neváhejte nás kontaktovat! Náš tým vám odpověď během 24 hodin.': 'Neváhajte nás kontaktovať! Náš tím vám odpovie do 24 hodín.',
    'Zavolat': 'Zavolať',
    'Napsat e-mail': 'Napísať e-mail',

    # Kontakt stránka
    'Kontaktujte nás': 'Kontaktujte nás',  # Same
    'Jsme tu pro vás. Rádi odpovíme na vaše dotazy.': 'Sme tu pre vás. Radi odpovieme na vaše otázky.',
    'Máte otázku k produktu, chcete objednat nebo máte reklamaci?': 'Máte otázku k produktu, chcete objednať alebo máte reklamáciu?',
    'Nechte nám vzkaz a my se vám ozvu co nejdříve.': 'Nechajte nám odkaz a my sa vám ozveme čo najskôr.',
    'Telefon': 'Telefón',
    'Volejte nás přímo': 'Volajte nám priamo',
    'Email': 'Email',  # Same
    'Napište nám email': 'Napíšte nám email',
    'Odpovídáme do 24 hodin': 'Odpovedáme do 24 hodín',
    'v pracovní dny': 'v pracovné dni',
    'Adresa': 'Adresa',  # Same
    'Osobní odběr po domluvě': 'Osobný odber po dohode',
    'Kontaktujte nás pro': 'Kontaktujte nás pre',
    'přesnou adresu': 'presnú adresu',

    # Formulář
    'Napište nám': 'Napíšte nám',
    'Vyplňte formulář a my se vám ozveme co nejdříve.': 'Vyplňte formulár a my sa vám ozveme čo najskôr.',
    'Zpráva odeslána!': 'Správa odoslaná!',
    'Děkujeme za vaši zprávu. Odpovíme vám do 24 hodin.': 'Ďakujeme za vašu správu. Odpovieme vám do 24 hodín.',
    'Jméno a příjmení': 'Meno a priezvisko',
    'Vaše jméno': 'Vaše meno',
    'Telefon (volitelné)': 'Telefón (voliteľné)',
    'Předmět': 'Predmet',
    'Vyberte předmět...': 'Vyberte predmet...',
    'Dotaz k produktu': 'Otázka k produktu',
    'Objednávka': 'Objednávka',  # Same
    'Reklamace': 'Reklamácia',
    'Spolupráce': 'Spolupráca',
    'Jiné': 'Iné',
    'Zpráva': 'Správa',
    'Napište nám vaši zprávu...': 'Napíšte nám vašu správu...',
    'Souhlasím se zpracováním mých osobních údajů': 'Súhlasím so spracovaním mojich osobných údajov',
    'Odeslat zprávu': 'Odoslať správu',
    'Všechna pole označená * jsou povinná': 'Všetky polia označené * sú povinné',
    'Toto pole je povinné': 'Toto pole je povinné',  # Same
    'Zadejte platný email': 'Zadajte platný email',

    # Mapa
    'Kde nás najdete': 'Kde nás nájdete',
    'Máme možnost osobního odběru v': 'Máme možnosť osobného odberu v',
    'Kontaktujte nás pro přesné místo a dobu.': 'Kontaktujte nás pre presné miesto a čas.',
    'Přesné místo po domluvě': 'Presné miesto po dohode',
    'Otevřít v Mapách': 'Otvoriť v Mapách',
    'Poznámka': 'Poznámka',  # Same
    'Osobní odběr je možný po domluvě.': 'Osobný odber je možný po dohode.',
    'Volejte nás nebo napište email a domluvíme si čas a místo.': 'Volajte nám alebo napíšte email a dohodneme si čas a miesto.',

    # FAQ na kontaktní stránce
    'Nenašli jste odpověď? Podívejte se do naší FAQ': 'Nenašli ste odpoveď? Pozrite sa do našich FAQ',
    'Jaká je doba doručení?': 'Aká je doba doručenia?',
    'Expedujeme do 24 hodin. Doručení trvá 2-3 pracovní dny dle vaší lokality.': 'Expedujeme do 24 hodín. Doručenie trvá 2-3 pracovné dni podľa vašej lokality.',
    'Jak funguje záruka?': 'Ako funguje záruka?',
    'Všechny regály mají 7letou záruku. Pokud se cokoliv stane, volejte nás.': 'Všetky regály majú 7-ročnú záruku. Ak sa čokoľvek stane, volajte nám.',
    'Jaké jsou platební možnosti?': 'Aké sú platobné možnosti?',
    'Přijímáme platby kartou, bankovním převodem, dobírkou a Bitcoin.': 'Prijímame platby kartou, bankovým prevodom, dobierkou a Bitcoin.',
    'Mohu vrátit objednávku?': 'Môžem vrátiť objednávku?',
    'Ano, máte 30 dní na vrácení bez udání důvodu. Vrátíme vám celý obnos.': 'Áno, máte 30 dní na vrátenie bez udania dôvodu. Vrátime vám celú sumu.',
    'Zobrazit všechny otázky': 'Zobraziť všetky otázky',

    # Doba odpovědi
    'Doba odpovědi': 'Doba odpovede',
    'Na všechny dotazy odpovídáme do 24 hodin v pracovní dny.': 'Na všetky otázky odpovedáme do 24 hodín v pracovné dni.',
    'Pokud nás kontaktujete přes formulář během pracovní doby, odpovíme vám ještě dnes.': 'Ak nás kontaktujete cez formulár počas pracovnej doby, odpovieme vám ešte dnes.',
    'Pondělí - Pátek 8:00 - 16:00': 'Pondelok - Piatok 8:00 - 16:00',
    'Nákupy online': 'Nákupy online',  # Same
    'Nákupy probíhají přes ověřený e-shop': 'Nákupy prebiehajú cez overený e-shop',
    'Všechny transakce jsou bezpečné a chráněné.': 'Všetky transakcie sú bezpečné a chránené.',
    'Jít na e-shop': 'Ísť na e-shop',

    # O nás stránka
    'Váš spolehlivý partner pro kvalitní kovové regály': 'Váš spoľahlivý partner pre kvalitné kovové regály',
    'NAŠE PŘÍBĚH': 'NÁŠ PRÍBEH',
    'Kdo jsme': 'Kto sme',
    'je prezentační stránka pro likvidaci skladu': 'je prezentačná stránka pre likvidáciu skladu',
    'Jsme projekt zaměřený na to, aby kvalitní kovové regály byly dostupné pro všechny.': 'Sme projekt zameraný na to, aby kvalitné kovové regály boli dostupné pre všetkých.',
    'Naše mateřská společnost': 'Naša materská spoločnosť',
    'provádí likvidaci velkého skladu obsahujícího tisíce': 'vykonáva likvidáciu veľkého skladu obsahujúceho tisíce',
    'nových, nerozbalených regálů vysoké kvality': 'nových, nerozbalených regálov vysokej kvality',
    'Místo aby se regály znehodnotily v skladě, rozhodli jsme se je nabídnout': 'Namiesto toho, aby sa regály znehodnotili v sklade, rozhodli sme sa ich ponúknuť',
    'veřejnosti za výjimečně nízké ceny': 'verejnosti za výnimočne nízke ceny',
    'Každý regál je nový, nerozbalený a pochází z důvěryhodného zdroje.': 'Každý regál je nový, nerozbalený a pochádza z dôveryhodného zdroja.',
    'Všechny produkty jsou chráněny zárukou 7 let': 'Všetky produkty sú chránené zárukou 7 rokov',
    'což dokazuje naši důvěru v kvalitu našeho sortimentu': 'čo dokazuje našu dôveru v kvalitu nášho sortimentu',
    'Produktů skladem': 'Produktov skladom',
    'Spokojených zákazníků': 'Spokojných zákazníkov',
    'Typů produktů': 'Typov produktov',

    # Proč jsme tady
    'Proč jsme tady': 'Prečo sme tu',
    'Naším cílem je udělat prémiové skladování dostupné pro všechny bez zbytečných výdajů.': 'Naším cieľom je urobiť prémiové skladovanie dostupné pre všetkých bez zbytočných výdavkov.',
    'Kvalita dostupná všem': 'Kvalita dostupná všetkým',
    'Věříme, že kvalitní regály by neměly být luxusem.': 'Veríme, že kvalitné regály by nemali byť luxusom.',
    'Díky likvidaci skladu můžeme nabídnout prémiové produkty': 'Vďaka likvidácii skladu môžeme ponúknuť prémiové produkty',
    'za zlomek běžné ceny': 'za zlomok bežnej ceny',
    'Udržitelnější budoucnost': 'Udržateľnejšia budúcnosť',
    'Namísto vyhazování nových produktů je předáváme lidem, kteří je potřebují.': 'Namiesto vyhadzovaniu nových produktov ich odovzdávame ľuďom, ktorí ich potrebujú.',
    'Tímto způsobem redukujeme odpad': 'Týmto spôsobom redukujeme odpad',
    'a minimalizujeme naši ekologickou stopu': 'a minimalizujeme našu ekologickú stopu',
    'Podpora podnikání': 'Podpora podnikania',
    'Podporujeme malé firmy, domácnosti i velké sklady při jejich potřebě kvalitního skladovacího řešení.': 'Podporujeme malé firmy, domácnosti aj veľké sklady pri ich potrebe kvalitného skladovacieho riešenia.',
    'Snižujeme jejich náklady na nákup inventáře.': 'Znižujeme ich náklady na nákup inventára.',
    'Transparentnost': 'Transparentnosť',
    'Všechny naše produkty jsou nové a nerozbalené.': 'Všetky naše produkty sú nové a nerozbalené.',
    'Podrobné informace a fotografie každého regálu jsou vždy': 'Podrobné informácie a fotografie každého regálu sú vždy',
    'dostupné': 'dostupné',  # Same
    'Žádná skrytá vada.': 'Žiadna skrytá chyba.',

    # Naše hodnoty
    'Naše hodnoty': 'Naše hodnoty',  # Same
    'Čtyři pilíře, na nichž se staví naše služba': 'Štyri piliere, na ktorých sa stavia naša služba',
    'Kvalita': 'Kvalita',  # Same
    '7letá záruka na všechny produkty': '7-ročná záruka na všetky produkty',
    'standardní záruka': 'štandardná záruka',
    'Rychlost': 'Rýchlosť',
    'Expediujeme do 24 hodin': 'Expedujeme do 24 hodín',
    'do odeslání': 'do odoslania',
    'Férovost': 'Férovosť',
    '30denní právo na vrácení': '30-dňové právo na vrátenie',
    'bez otázek': 'bez otázok',
    'Jednoduchost': 'Jednoduchosť',
    'Montáž bez nářadí': 'Montáž bez náradia',
    'doba montáže': 'doba montáže',  # Same

    # Statistiky
    'Naší výsledky': 'Naše výsledky',
    'Čísla, která vypovídají o našem úspěchu': 'Čísla, ktoré hovoria o našom úspechu',
    'Nikdy nemáme problém s dostupností': 'Nikdy nemáme problém s dostupnosťou',
    'A jejich počet neustále roste': 'A ich počet neustále rastie',
    'Nejdelší standardní záruka na trhu': 'Najdlhšia štandardná záruka na trhu',
    'Regály pro každý účel a potřebu': 'Regály pre každý účel a potrebu',

    # Tým
    'Náš tým': 'Náš tím',
    'Za projektem stojí tým nadšenců pro kvalitní skladování': 'Za projektom stojí tím nadšencov pre kvalitné skladovanie',
    'Projektový tým': 'Projektový tím',
    'Tým podpory': 'Tím podpory',
    'Tým logistiky': 'Tím logistiky',
    'Dedikovaní profesionálové': 'Dedikovaní profesionáli',
    'Náš tým se skládá z zkušených profesionálů z oblasti skladování, logistiky a zákaznické podpory.': 'Náš tím sa skladá zo skúsených profesionálov z oblasti skladovania, logistiky a zákazníckej podpory.',
    'Každý člen týmu je zaměřen na to, aby vaše nakupování bylo co nejhladší a nejpříjemnější.': 'Každý člen tímu je zameraný na to, aby vaše nakupovanie bolo čo najhladšie a najpríjemnejšie.',
    'Jsme tu pro vás a jsme pyšní na služby, které poskytujeme.': 'Sme tu pre vás a sme hrdí na služby, ktoré poskytujeme.',

    # CTA
    'Připraveni koupit?': 'Pripravení kúpiť?',
    'Prohlédněte si naši kompletní nabídku kvalitních kovových regálů dostupných za likvidační ceny.': 'Prezrite si našu kompletnú ponuku kvalitných kovových regálov dostupných za likvidačné ceny.',
    'Prohlédnout katalog': 'Prezrieť katalóg',

    # Detail produktu
    'VÝPRODEJ': 'VÝPREDAJ',
    'BESTSELLER': 'BESTSELLER',  # Same
    'Profesionální kovový regál do domácnosti i dílny': 'Profesionálny kovový regál do domácnosti aj dielne',
    'Elegantní černý lak': 'Elegantný čierny lak',
    '5 nastavitelných polic s nosností 175 kg každá': '5 nastaviteľných políc s nosnosťou 175 kg každá',
    'Bezšroubová montáž za 10 minut bez nářadí': 'Bezskrutková montáž za 10 minút bez náradia',
    'Ideální pro garáž, spíž, sklep nebo kancelář': 'Ideálne pre garáž, špajzu, pivnicu alebo kanceláriu',
    'Cena bez DPH': 'Cena bez DPH',  # Same
    'Ušetříte': 'Ušetríte',
    'Za posledních 24h koupilo': 'Za posledných 24h kúpilo',
    'lidí': 'ľudí',
    'Rozměry': 'Rozmery',
    'Celk. nosnost': 'Celk. nosnosť',
    'Počet polic': 'Počet políc',
    'Povrch': 'Povrch',  # Same
    'Práškový lak': 'Práškový lak',  # Same
    'Koupit': 'Kúpiť',
    'Doprava od 99 Kč': 'Doprava od 3,99 €',
    'Expedujeme ihned': 'Expedujeme ihneď',
    'Na celý regál': 'Na celý regál',  # Same
    '14 dní na vrácení': '14 dní na vrátenie',
    'Bez udání důvodu': 'Bez udania dôvodu',
    'Snadná montáž': 'Jednoduchá montáž',
    'Za 10 minut bez nářadí': 'Za 10 minút bez náradia',

    # Taby
    'Popis': 'Popis',  # Same
    'Parametry': 'Parametre',
    'Rozměry': 'Rozmery',
    'Montáž': 'Montáž',  # Same
    'Recenze': 'Recenzie',
    'Dotazy': 'Otázky',

    # Popis tab
    'Profesionální kovový regál pro náročné použití': 'Profesionálny kovový regál pre náročné použitie',
    'Hledáte spolehlivé úložné řešení': 'Hľadáte spoľahlivé úložné riešenie',
    'které zvládne i těžší předměty a zároveň bude vypadat elegantně': 'ktoré zvládne aj ťažšie predmety a zároveň bude vyzerať elegantne',
    'je přesně to, co potřebujete': 'je presne to, čo potrebujete',
    'pojme vše od knih přes nářadí až po těžké krabice': 'pojme všetko od kníh cez náradie až po ťažké krabice',
    'Vysoká nosnost 175 kg/polici': 'Vysoká nosnosť 175 kg/policu',
    'Každá z 5 polic unese až 175 kg': 'Každá z 5 políc unesie až 175 kg',
    'Celkem tedy 875 kg na celý regál': 'Celkom teda 875 kg na celý regál',
    'Bezšroubová montáž za 10 minut': 'Bezskrutková montáž za 10 minút',
    'Systém zapadacích spojek nevyžaduje šrouby ani nářadí': 'Systém zapadajúcich spojok nevyžaduje skrutky ani náradie',
    'Odolný práškový lak': 'Odolný práškový lak',  # Same
    'Kvalitní povrchová úprava chrání před korozí a zaručuje dlouhou životnost': 'Kvalitná povrchová úprava chráni pred koróziou a zaručuje dlhú životnosť',
    'Nastavitelná výška polic': 'Nastaviteľná výška políc',
    'Police můžete nastavit po 5 cm podle potřeby': 'Police môžete nastaviť po 5 cm podľa potreby',
    'Pro koho je tento regál vhodný?': 'Pre koho je tento regál vhodný?',
    'Garáž a dílnu': 'Garáž a dielňu',
    'uložte nářadí, barvy, chemii i náhradní díly': 'uložte náradie, farby, chémiu aj náhradné diely',
    'Spíž a sklep': 'Špajzu a pivnicu',
    'konzervace, zavařeniny, víno a potraviny na jednom místě': 'konzervy, zaváraniny, víno a potraviny na jednom mieste',
    'Kancelář a archiv': 'Kanceláriu a archív',
    'šanony, dokumenty a kancelářské potřeby': 'šanóny, dokumenty a kancelárske potreby',
    'Šatnu a komoru': 'Šatňu a komoru',
    'boxy s oblečením, boty, sezónní věci': 'boxy s oblečením, topánky, sezónne veci',
    'Sklad e-shopu': 'Sklad e-shopu',  # Same
    'rychlý přístup ke zboží a přehledná organizace': 'rýchly prístup k tovaru a prehľadná organizácia',
    'Co je v balení': 'Čo je v balení',
    'Sloupky (stojny)': 'Stĺpiky (stojany)',
    'Police': 'Police',  # Same
    'Spojovací příčky': 'Spojovacie priečky',
    'Návod k montáži': 'Návod na montáž',

    # Parametry tab
    'Technické parametry': 'Technické parametre',
    'Vizualizace rozměrů': 'Vizualizácia rozmerov',
    'Výška': 'Výška',  # Same
    'od podlahy po vrch': 'od podlahy po vrch',  # Same
    'Šířka': 'Šírka',
    'mezi stojnami': 'medzi stojanmi',
    'Hloubka': 'Hĺbka',
    'od zdi': 'od steny',
    'Rozměry a konstrukce': 'Rozmery a konštrukcia',
    'Rozteč polic': 'Rozstup políc',
    'Nastavitelná po 50 mm': 'Nastaviteľná po 50 mm',
    'Nosnost jedné police': 'Nosnosť jednej police',
    'Celková nosnost regálu': 'Celková nosnosť regálu',
    'Materiál a povrch': 'Materiál a povrch',  # Same
    'Materiál konstrukce': 'Materiál konštrukcie',
    'Ocelový plech': 'Oceľový plech',
    'Povrchová úprava': 'Povrchová úprava',  # Same
    'Barva': 'Farba',
    'Ostatní údaje': 'Ostatné údaje',
    'Kód produktu': 'Kód produktu',  # Same
    'Hmotnost': 'Hmotnosť',
    'Typ montáže': 'Typ montáže',  # Same
    'Bezšroubová': 'Bezskrutková',
    'Záruka': 'Záruka',  # Same

    # Rozměry tab
    'Rozměrový nákres': 'Rozmerový nákres',
    'Detailní rozměry': 'Detailné rozmery',
    'Celková výška': 'Celková výška',  # Same
    'Od podlahy po horní hranu': 'Od podlahy po hornú hranu',
    'Vnější rozměr mezi stojnami': 'Vonkajší rozmer medzi stojanmi',
    'Využitelná plocha police': 'Využiteľná plocha police',
    'Tip: Změřte si prostor': 'Tip: Zmerajte si priestor',
    'Nechte alespoň 5 cm volného místa okolo regálu': 'Nechajte aspoň 5 cm voľného miesta okolo regálu',

    # Montáž tab
    'Montáž regálu': 'Montáž regálu',  # Same
    'Montáž za 10 minut bez nářadí!': 'Montáž za 10 minút bez náradia!',
    'Díky bezšroubovému systému je sestavení regálu hračka': 'Vďaka bezskrutkovému systému je zostavenie regálu hračka',
    'Video návod k montáži': 'Video návod na montáž',
    'Postup montáže': 'Postup montáže',  # Same
    'Položte 2 stojny na zem': 'Položte 2 stojany na zem',
    'Rovnoběžně vedle sebe': 'Rovnobežne vedľa seba',
    'Nasaďte příčky spodní police': 'Nasaďte priečky spodnej police',
    'Zaklapněte do otvorů': 'Zaklapnite do otvorov',
    'Postavte konstrukci': 'Postavte konštrukciu',
    'Přidejte zbývající stojny': 'Pridajte zvyšné stojany',
    'Vložte police': 'Vložte police',  # Same
    'Položte na příčky': 'Položte na priečky',
    'Hotovo!': 'Hotovo!',  # Same
    'Zkontrolujte stabilitu': 'Skontrolujte stabilitu',
    'Tipy pro montáž': 'Tipy na montáž',
    'Montáž provádějte ve dvou lidech': 'Montáž vykonávajte vo dvoch ľuďoch',
    'Použijte gumovou paličku pro doražení spojů': 'Použite gumovú paličku na dorazenie spojov',
    'Pro stabilitu přikotvěte regál ke zdi': 'Pre stabilitu prikotviť regál k stene',
    'Těžké předměty umísťujte na spodní police': 'Ťažké predmety umiestňujte na spodné police',

    # FAQ tab
    'Časté dotazy': 'Časté otázky',
    'Jaká je skutečná nosnost police?': 'Aká je skutočná nosnosť police?',
    'Nosnost 175 kg na polici platí při rovnoměrném rozložení zátěže': 'Nosnosť 175 kg na policu platí pri rovnomernom rozložení záťaže',
    'Mohu regál použít ve vlhkém prostředí?': 'Môžem regál použiť vo vlhkom prostredí?',
    'Lakovaný regál je vhodný do suchých a mírně vlhkých prostor': 'Lakovaný regál je vhodný do suchých a mierne vlhkých priestorov',
    'Pro vlhké prostředí doporučujeme zinkovanou variantu': 'Pre vlhké prostredie odporúčame zinkovanú variantu',
    'Jak dlouho trvá doručení?': 'Ako dlho trvá doručenie?',
    'Produkt je skladem, expedujeme ihned': 'Produkt je skladom, expedujeme ihneď',
    'Doručení trvá obvykle 2-3 pracovní dny': 'Doručenie trvá obvykle 2-3 pracovné dni',

    # Související produkty
    'Podobné produkty': 'Podobné produkty',  # Same
    'Bílá varianta': 'Biela varianta',
    'Zinkovaná varianta': 'Zinkovaná varianta',  # Same
    'Do vlhka': 'Do vlhka',  # Same
    'Užší varianta': 'Užšia varianta',
    'Menší regál': 'Menší regál',  # Same
    'Varianta': 'Varianta',  # Same

    # Katalog
    'LIKVIDACE PROBÍHÁ PRÁVĚ TEĎ': 'LIKVIDÁCIA PREBIEHA PRÁVE TERAZ',
    'lidí právě nakupuje': 'ľudí práve nakupuje',
    'Dnes prodáno:': 'Dnes predaných:',
    'regálů': 'regálov',
    'Prohlédnout regály': 'Prezrieť regály',
    'Zbývá pouze': 'Zostáva iba',
    'ks': 'ks',  # Same
    'Koupeno': 'Kúpené',
    'za 7 dní': 'za 7 dní',  # Same

    # Filtry
    'Filtry': 'Filtre',
    'Resetovat': 'Resetovať',
    'Barva': 'Farba',
    'Výška': 'Výška',  # Same
    'Šířka': 'Šírka',
    'Povrch': 'Povrch',  # Same
    'Cena': 'Cena',  # Same
    'Nosnost celkem': 'Nosnosť celkom',
    'Ideální do': 'Ideálne do',
    'Garáž': 'Garáž',  # Same
    'Sklep': 'Pivnica',
    'Dílna': 'Dielňa',
    'Kancelář': 'Kancelária',
    'Zink': 'Zink',  # Same

    # Řazení
    'Řadit:': 'Zoradiť:',
    'Nejprodávanější': 'Najpredávanejšie',
    'Cena: od nejnižší': 'Cena: od najnižšej',
    'Cena: od nejvyšší': 'Cena: od najvyššej',
    'Název A-Z': 'Názov A-Z',
    'Nosnost: od nejvyšší': 'Nosnosť: od najvyššej',

    # Stránkování
    'Předchozí': 'Predchádzajúci',
    'Další': 'Ďalší',

    # Popup
    'Počkejte! Máme pro vás dárek': 'Počkajte! Máme pre vás darček',
    'slevu 10%': 'zľavu 10%',
    'na první objednávku': 'na prvú objednávku',
    'Platí pouze dnes při objednávce nad': 'Platí iba dnes pri objednávke nad',
    'Uplatnit slevu': 'Uplatniť zľavu',
    'Ne, děkuji': 'Nie, ďakujem',

    # Shipping bar
    'Přidejte zboží za': 'Pridajte tovar za',
    'a získejte': 'a získajte',
    'dopravu ZDARMA!': 'dopravu ZADARMO!',

    # Chatbot
    'RegálBot': 'RegálBot',  # Same
    'Online': 'Online',  # Same
    'Ahoj!': 'Ahoj!',  # Same
    'Jsem RegálBot a pomohu vám vybrat ideální regál.': 'Som RegálBot a pomôžem vám vybrať ideálny regál.',
    'Na co se chcete zeptat?': 'Na čo sa chcete opýtať?',
    'Napište zprávu...': 'Napíšte správu...',
    'Do garáže': 'Do garáže',  # Same
    'Do vlhka': 'Do vlhka',  # Same
    'Nejlevnější': 'Najlacnejší',
    'Pro garáž doporučuji': 'Pre garáž odporúčam',
    'Mají nosnost 875 kg a jsou odolné': 'Majú nosnosť 875 kg a sú odolné',
    'Do vlhkého prostředí jednoznačně': 'Do vlhkého prostredia jednoznačne',
    'Jsou odolné proti korozi a vlhkosti': 'Sú odolné proti korózii a vlhkosti',
    'Máme je od': 'Máme ich od',
    'Nejlevnější regál máme za': 'Najlacnejší regál máme za',
    'Skvělý poměr cena/výkon!': 'Skvelý pomer cena/výkon!',
    'Všechny naše regály mají vysokou nosnost 175 kg na polici': 'Všetky naše regály majú vysokú nosnosť 175 kg na policu',
    'Celková nosnost až 875 kg!': 'Celková nosnosť až 875 kg!',
    'To unese opravdu hodně': 'To unesie naozaj veľa',
    'Doručujeme do 2-3 pracovních dnů po celé': 'Doručujeme do 2-3 pracovných dní po celom',
    'Doprava od 99 Kč, nad 1000 Kč ZDARMA!': 'Doprava od 3,99 €, nad 39 € ZADARMO!',
    'Na všechny regály poskytujeme záruku 7 let!': 'Na všetky regály poskytujeme záruku 7 rokov!',
    'To je jeden z nejdelších záručních období na trhu': 'To je jedno z najdlhších záručných období na trhu',
    'Montáž je super jednoduchá': 'Montáž je super jednoduchá',  # Same
    'bezšroubový systém, zvládnete to za 10 minut bez nářadí!': 'bezskrutkový systém, zvládnete to za 10 minút bez náradia!',
    'Máme i video návod': 'Máme aj video návod',
    'Děkuji za dotaz!': 'Ďakujem za otázku!',
    'Pomohu vám vybrat ideální regál.': 'Pomôžem vám vybrať ideálny regál.',
    'Můžete mi říct, kam ho chcete umístit': 'Môžete mi povedať, kam ho chcete umiestniť',
    'garáž, sklep, dílna': 'garáž, pivnica, dielňa',
    'nebo jaké máte požadavky na velikost či nosnost?': 'alebo aké máte požiadavky na veľkosť či nosnosť?',

    # Live notifications
    'Přidáno do košíku': 'Pridané do košíka',
    'právě koupil(a)': 'práve kúpil(a)',
    'z města': 'z mesta',
    'před': 'pred',

    # File names in links
    'bazarovyregal-homepage.html': 'index.html',
    'bazarovyregal-katalog.html': 'katalog.html',
    'bazarovyregal-detail-produktu.html': 'detail.html',
    'bazarovyregal-faq.html': 'faq.html',
    'bazarovyregal-kontakt.html': 'kontakt.html',
    'bazarovyregal-o-nas.html': 'o-nas.html',

    # Copyright
    '© 2026 Bazarovyregal.cz': '© 2026 Bazarovyregal.sk',
}

# Přepočet cen z Kč na € (kurz cca 25 Kč = 1 €)
def convert_price(match):
    price_text = match.group(0)
    # Odstraníme všechny mezery a "Kč"
    price_str = price_text.replace(' ', '').replace('Kč', '').replace('\xa0', '')
    try:
        price_czk = int(price_str)
        price_eur = round(price_czk / 25, 2)
        # Formátování s desetinnou čárkou
        return f"{price_eur:.2f} €".replace('.', ',')
    except:
        return price_text

def localize_file(content):
    """Lokalizuje obsah souboru z češtiny do slovenštiny"""

    # Nejprve nahradíme všechny statické překlady
    for czech, slovak in TRANSLATIONS.items():
        content = content.replace(czech, slovak)

    # Pak převedeme ceny pomocí regex
    # Pattern pro ceny typu "489 Kč", "1 149 Kč", "2 949 Kč"
    content = re.sub(r'(\d[\d\s]*)\s*Kč', convert_price, content)

    # Ujistíme se, že lang je "sk"
    content = content.replace('lang="cs"', 'lang="sk"')

    return content

def main():
    # Zdrojové a cílové adresáře
    source_github = '/sessions/exciting-serene-rubin/mnt/Downloads/bazarovyregal-github'
    source_deploy = '/sessions/exciting-serene-rubin/mnt/Downloads/bazarovyregal-deploy'
    target_dir = '/sessions/exciting-serene-rubin/mnt/Bazarovyregalsk'

    # Vyčistíme cílový adresář
    if os.path.exists(target_dir):
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            if os.path.isfile(item_path) and item.endswith('.py'):
                continue  # Necháme Python skripty
            elif os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)

    # Seznam souborů k lokalizaci z github složky
    github_files = [
        ('index.html', 'index.html'),
        ('katalog.html', 'katalog.html'),
        ('detail.html', 'detail.html'),
        ('faq.html', 'faq.html'),
        ('kontakt.html', 'kontakt.html'),
        ('o-nas.html', 'o-nas.html'),
        ('quiz.html', 'quiz.html'),
        ('srovnavac.html', 'srovnavac.html'),
        ('lokalni-seo.html', 'lokalni-seo.html'),
    ]

    processed = 0

    # Zpracování hlavních souborů z github
    for source_name, target_name in github_files:
        source_path = os.path.join(source_github, source_name)
        target_path = os.path.join(target_dir, target_name)

        if os.path.exists(source_path):
            with open(source_path, 'r', encoding='utf-8') as f:
                content = f.read()

            localized = localize_file(content)

            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(localized)

            processed += 1
            print(f"✓ Lokalizován: {source_name} -> {target_name}")

    print(f"\n✅ Lokalizováno {processed} hlavních souborů")

    # Zpracování SEO stránek z deploy složky
    seo_processed = 0
    seo_dir = os.path.join(target_dir, 'seo')
    os.makedirs(seo_dir, exist_ok=True)

    if os.path.exists(source_deploy):
        for filename in os.listdir(source_deploy):
            if filename.endswith('.html') and not filename.startswith('.'):
                source_path = os.path.join(source_deploy, filename)
                target_path = os.path.join(seo_dir, filename)

                try:
                    with open(source_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    localized = localize_file(content)

                    with open(target_path, 'w', encoding='utf-8') as f:
                        f.write(localized)

                    seo_processed += 1

                    if seo_processed % 100 == 0:
                        print(f"  Zpracováno {seo_processed} SEO stránek...")
                except Exception as e:
                    print(f"⚠ Chyba při zpracování {filename}: {e}")

    print(f"✅ Lokalizováno {seo_processed} SEO stránek")
    print(f"\n🎉 Celkem lokalizováno {processed + seo_processed} souborů")
    print(f"📁 Výstup uložen do: {target_dir}")

if __name__ == '__main__':
    main()
