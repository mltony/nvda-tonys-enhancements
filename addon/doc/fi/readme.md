# Tonyn laajennukset #

Tämä lisäosa sisältää useita pieniä NVDA-ruudunlukijan parannuksia, jotka
ovat liian pieniä ansaitakseen erillisen lisäosan.

Tämä lisäosa on yhteensopiva NVDA 2022.4:n ja 2024.1:n kanssa.

## Lataukset

Asenna uusin versio NVDA:n lisäosakaupasta.

## Laajennetut taulukkonavigointikomennot
* NVDA+Ctrl+numero: Siirrä taulukon
  ensimmäiseen/toiseen/kolmanteen/... kymmenenteen sarakkeeseen.
* NVDA+Alt+numero: Siirrä taulukon
  ensimmäiselle/toiselle/kolmannelle/... kymmenennelle riville.

## Taulukoiden kopiointi leikepöydälle

Seuraavilla pikanäppäimillä voit kopioida muotoiltuna joko koko taulukon tai
nykyisen rivin/sarakkeen, jotta voit liittää sen taulukkona
rikastekstieditoreihin, kuten Microsoft Word tai WordPad.

* NVDA+Alt+T: Näyttää ponnahdusvalikon, jossa on vaihtoehdot taulukon tai
  sen osan kopioimiseen.

There are also separate scripts for copying tables, rows, columns and cells,
but they don't have keyboard shortcuts assigned by default, custom keyboard
shortcuts cfor them can be assigned in InputGestures dialog of NVDA.

## Automaattinen kielen vaihtaminen
Mahdollistaa puhesyntetisaattorin kielen vaihtamisen automaattisesti
merkistön perusteella. Kielten säännölliset lausekkeet voidaan määrittää
tämän lisäosan asetuksista. Varmista, että käyttämäsi syntetisaattori tukee
kaikkia niitä kieliä, joista olet kiinnostunut. Kahden latinalaista tai
samankaltaista merkistöä käyttävän kielen välillä vaihtaminen ei ole
toistaiseksi mahdollista.

## Pikahakukomennot

Pikahakukomennot on siirretty versiosta 1.18 alkaen
[Sisennysnavigointi-lisäosaan](https://github.com/mltony/nvda-indent-nav).

## Estä häiritsevät NVDA:n "ei valittu" -ilmoitukset

Oletetaan, että sinulla on tekstiä valittuna tekstieditorissa, ja painat
sitten näppäintä, kuten Home tai Nuoli ylös, joka siirtää toiseen kohtaan
asiakirjassa. NVDA sanoo tällöin "ei valittu" ja sen jälkeen valittuna
olleen tekstin, mikä voi olla häiritsevää. Tämä toiminto estää NVDA:ta
puhumasta tällaisissa tilanteissa valittuna ollutta tekstiä.

## Dynaamiset näppäinkomennot

Voit määrittää tietyt näppäinpainallukset dynaamisiksi. Tällaisen
näppäinpainalluksen jälkeen NVDA tarkistaa aktiivisena olevan ikkunan
mahdollisten päivitysten varalta, ja jos rivi päivittyy, NVDA puhuu sen
automaattisesti. Esimerkiksi tietyt tekstieditorien näppäinpainallukset
tulee merkitä dynaamisiksi, kuten "siirry kirjanmerkkiin", "siirry toiselle
riville" ja virheenkorjausnäppäimet, kuten siirrä kohdalle/siirrä ohi.

Dynaamisten näppäinpainallusten taulukon muoto on yksinkertainen. Kukin rivi
sisältää säännön seuraavassa muodossa:
```
sovellus näppäinpainallus
```
jossa `sovellus` on sen sovelluksen nimi, jonka näppäinpainallus merkitään
dynaamiseksi (tai `*`, jolloin se merkitään dynaamiseksi kaikissa
sovelluksissa), ja `näppäinpainallus` on näppäinpainallus NVDA:n
ymmärtämässä muodossa, esim. `control+alt+shift+pagedown`.

Selvitä sovelluksen nimi seuraavasti:

1. Siirry sovellukseen.
2. Avaa NVDA:n Python-konsoli painamalla NVDA+Vaihto+Z.
3. Kirjoita `focus.appModule.appName` ja paina Enter.
4. Siirry tulostusruutuun painamalla F6 ja etsi viimeiseltä riviltä appNamen
   arvo.

## Ikkunoiden näyttäminen ja piilottaminen

As of version v1.18 show/hide commands have been moved to [Task Switcher
add-on](https://github.com/mltony/nvda-task-switcher).

## Anna äänimerkki, kun NVDA on varattu

Valitse tämä vaihtoehto, jos haluat NVDA:n antavan äänipalautteen, kun se on
varattu. NVDA:n varattuna oleminen ei välttämättä tarkoita ongelmaa, vaan se
on merkki käyttäjälle siitä, että NVDA-komentoja ei käsitellä heti.

## Sovellusten äänenvoimakkuuden muuttaminen

Tämä toiminnallisuus on sulautettu NVDA:n ytimeen, ja on käytettävissä
versiossa 2024.3 tai sitä uudemmassa.

## Äänenjako

Tämä toiminnallisuus on sulautettu NVDA:n ytimeen, ja on käytettävissä
versiossa 2024.2 tai sitä uudemmassa.

## Laajennetut hiiritoiminnot

* Alt+Laskinnäppäimistön jakomerkki: Osoita hiirikohdistin nykyiseen
  objektiin ja napsauta sitä.
* Alt+Laskinnäppäimistön kertomerkki: Osoita hiirikohdistin nykyiseen
  objektiin ja napsauta siinä hiiren oikeaa näppäintä.
* Alt+Laskinnäppäimistön plus/Laskinnäppäimistön miinus: Osoita
  hiirikohdistin nykyiseen objektiin ja vieritä alas/ylös. Tästä on hyötyä
  jatkuvan vierityksen verkkosivuilla sekä sellaisissa, jotka lataavat lisää
  sisältöä vieritettäessä.
* Alt+Laskinnäppäimistön Del: Siirrä hiirikohdistin näytön vasempaan
  yläkulmaan. Tästä voi olla hyötyä, kun halutaan estää hiiren jääminen
  ikkunoiden päälle tietyissä sovelluksissa.


## Lisäystilan havaitseminen tekstieditoreissa

Jos tämä asetus on käytössä, NVDA antaa äänimerkin, kun se havaitsee
lisäystilan tekstieditoreissa.

## Estä kaksinkertainen Insert-näppäimen painallus

NVDA:ssa Insert-näppäimen painaminen kahdesti peräkkäin ottaa sovelluksissa
käyttöön lisäystilan. Joskus se kuitenkin tapahtuu vahingossa. Koska tämä on
erityinen näppäinpainallus, sitä ei voi poistaa käytöstä asetuksissa. Tämä
lisäosa tarjoaa tavan tämän pikanäppäimen estämiseen. Kun kaksinkertainen
Insertin painallus on estetty, lisäystila voidaan ottaa käyttöön painamalla
NVDA+F2 ja sitten Insert.

Tämä asetus ei ole oletusarvoisesti käytössä, ja se on otettava käyttöön
asetuksissa.

## NVDA-prosessin järjestelmäprioriteetti

Tämä mahdollistaa NVDA-prosessin järjestelmäprioriteetin lisäämisen, mikä
saattaa parantaa NVDA:n reagointia erityisesti suoritinta paljon
kuormitettaessa.

## Kohdistuksen jääminen jumiin tehtäväpalkkiin painettaessa Win+numero-pikanäppäintä

Tämä ominaisuus on poistettu versiosta 1.18 alkaen. Mikäli tarvitset
luotettavampaa tehtävänvaihtotoiminnallisuutta, harkitse [Task Switcher
-lisäosan](https://github.com/mltony/nvda-task-switcher) käyttöä.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=tonysEnhancements
