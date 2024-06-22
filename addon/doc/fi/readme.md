# Tonyn laajennukset #

Tämä lisäosa sisältää useita pieniä NVDA-ruudunlukijan parannuksia, jotka
ovat liian pieniä ansaitakseen erillisen lisäosan.

Tämä lisäosa on yhteensopiva NVDA 2024.2:n tai sitä uudempien kanssa

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

Taulukoiden, rivien, sarakkeiden ja solujen kopiointia varten on myös
erilliset skriptit, mutta niille ei ole oletuksena määritetty
pikanäppäimiä. Ne on mahdollista määrittää NVDA:n
Näppäinkomennot-valintaikkunassa.

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

Näytä/Piilota-komennot on siirretty versiosta 1.18 alkaen [Task Switcher
-lisäosaan](https://github.com/mltony/nvda-task-switcher).

## Anna äänimerkki, kun NVDA on varattu

Valitse tämä vaihtoehto, jos haluat NVDA:n antavan äänipalautteen, kun se on
varattu. NVDA:n varattuna oleminen ei välttämättä tarkoita ongelmaa, vaan se
on merkki käyttäjälle siitä, että NVDA-komentoja ei käsitellä heti.

## Sovellusten äänenvoimakkuuden muuttaminen

Tämä toiminnallisuus on sulautettu NVDA:n ytimeen, ja on käytettävissä
versiossa 2024.3 tai sitä uudemmassa.

## Mykistä mikrofoni

Tämä lisäosa tarjoaa komennon mikrofonin mykistämiseen ja mykistyksen
poistamiseen. Sille ei ole oletusarvoisesti määritetty näppäinkomentoa,
mutta voit tarvittaessa määrittää sellaisen NVDA:n
"Näppäinkomennot"-valintaikkunassa.

## Äänenjako

Tämä toiminnallisuus on sulautettu NVDA:n ytimeen, ja on käytettävissä
versiossa 2024.2 tai sitä uudemmassa.

## Laajennetut hiiritoiminnot

* Alt+Laskinnäppäimistön jakomerkki: Osoita hiirikohdistin nykyiseen
  objektiin ja napsauta sitä.
* Alt+Laskinnäppäimistön kertomerkki: Osoita hiirikohdistin nykyiseen
  objektiin ja napsauta siinä hiiren oikeaa näppäintä.
* Alt+Laskinnäppäimistön Del: Siirrä hiirikohdistin näytön vasempaan
  yläkulmaan. Tästä voi olla hyötyä, kun halutaan estää hiiren jääminen
  ikkunoiden päälle tietyissä sovelluksissa.

Hiiren rullan vieritystoiminnallisuus on sulautettu NVDA:n ytimeen, ja on
käytettävissä versiossa 2024.3 tai sitä uudemmassa.

## Lisäystilan havaitseminen tekstieditoreissa

Jos tämä asetus on käytössä, NVDA antaa äänimerkin, kun se havaitsee
lisäystilan tekstieditoreissa.

## Estä Insert-näppäimen kaksoispainallus

NVDA:ssa Insert-näppäimen painaminen kahdesti peräkkäin ottaa sovelluksissa
käyttöön lisäystilan. Joskus se kuitenkin tapahtuu vahingossa. Koska tämä on
erityinen näppäinpainallus, sitä ei voi poistaa käytöstä asetuksissa. Tämä
lisäosa tarjoaa tavan tämän pikanäppäimen estämiseen. Kun Insertin
kaksoispainallus on estetty, lisäystila voidaan ottaa käyttöön painamalla
NVDA+F2 ja sitten Insert.

Tämä asetus ei ole oletusarvoisesti käytössä, ja se on otettava käyttöön
asetuksissa.

## Estä Caps Lock -näppäimen kaksoispainallus

Kun Caps Lock on määritetty NVDA-näppäimeksi, sen painaminen kahdesti
peräkkäin vaihtaa isojen ja pienten kirjainten välillä. Toisinaan se saattaa
kuitenkin tapahtua vahingossa. Koska kyseessä on erikoisnäppäin eikä sitä
voi poistaa käytöstä asetuksissa, tämä lisäosa tarjoaa menetelmän kyseisen
näppäinpainalluksen estämiseen. Kun Caps Lockin kaksoispainallus on estetty,
voit silti vaihtaa isojen ja pienten kirjainten välillä painamalla NVDA+F2
ja sitten Caps Lock.

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
