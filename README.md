# WebScrap
O co jde v projektu?
Tento skript umožnuje získat výsledky z parlamentních voleb 2017 pro okrez z této stránky : https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ a uložit je do csv souboru

Jak na to ?
Před spuštěním je potřeba zkontrolovat jestli máte potřebné knihovny které jsou uvedeny v souboru requirements.txt. Skript se pak spustí pomocí příkazového řádku pomocí následujícího příkazu 
python WebScrap.py <odkaz_uzemniho_celku> <odkaz_kde_jsou_uvedené_strany> <vystupni_soubor>
výstupem pak bude soubor csv s výsledky voleb

Příklad v praxi pro okres Jablonec nad Nisou 
python WebScrap.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=7&xnumnuts=5102" "https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=7&xobec=563528&xvyber=5102" vysledky-okrsek_Jablonec_nad_Nisou.csv

Výsledek : 
Kod oblasti;Nazev oblasti;Registrovany volici;Obalky;Platn� hlasy;Ob�ansk� demokratick� strana;��d n�roda - Vlasteneck� unie;CESTA ODPOV�DN� SPOLE�NOSTI;�esk� str.soci�ln� demokrat.;STAROSTOV� A NEZ�VISL�;Komunistick� str.�ech a Moravy;Strana zelen�ch;ROZUMN�-stop migraci,dikt�t.EU;Strana svobodn�ch ob�an�;Blok proti islam.-Obran.domova;Ob�ansk� demokratick� aliance;�esk� pir�tsk� strana;Referendum o Evropsk� unii;TOP 09;ANO 2011;Dobr� volba 2016;SPR-Republ.str.�sl. M.Sl�dka;K�es�.demokr.unie-�s.str.lid.;�esk� strana n�rodn� soci�ln�;REALIST�;SPORTOVCI;D�lnic.str.soci�ln� spravedl.;Svob.a p�.dem.-T.Okamura (SPD);Strana Pr�v Ob�an�
563528;Albrechtice v Jizersk�ch hor�ch;277;211;210;37;0;0;9;12;11;9;1;0;0;0;40;0;16;45;0;0;6;0;1;1;0;21;1
563536;Bed�ichov;304;237;233;66;0;0;4;32;8;4;0;3;0;2;38;0;17;42;0;0;5;0;2;1;0;9;0
530425;Dale�ice;147;107;107;10;0;1;9;11;5;2;0;2;1;0;13;0;7;27;0;0;3;0;1;0;0;14;1
