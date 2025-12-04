## Opis projekta

Meme Generator je spletna aplikacija, ki omogoča uporabnikom, da:
- Naložijo svojo sliko preko preprostega spletnega vmesnika
- Dodajo zgornji in spodnji tekst v klasičnem meme formatu
- Generirajo profesionalen meme z belim tekstom in črno obrobo
- Prenesejo generirani meme na svoj računalnik

## Uporabljene tehnologije

- **Jezik**: Python 3.12
- **Web Framework**: Flask 3.1.2
- **Obdelava slik**: Pillow 12.0.0
- **Kontejnerizacija**: Docker

##  Struktura projekta

```
meme-generator/
│
├── app.py                    # Glavna Flask aplikacija
├── requirements.txt          # Python odvisnosti
├── Dockerfile               # Docker konfiguracija
├── .gitignore              # Git ignore pravila
│
├── templates/
│   └── index.html          # HTML template
│
├── static/
│   └── uploads/            # Začasna mapa za naložene slike
│
└── fonts/                  # Mapa za fontе 
```

## Kako deluje aplikacija

1. **Nalaganje slike**: Uporabnik naloži sliko preko HTML obrazca
2. **Vnos teksta**: Uporabnik vnese zgornji in spodnji tekst
3. **Obdelava**: Flask sprejme podatke, Pillow knjižnica obdela sliko in doda tekst
4. **Vrnitev**: Generirani meme se prikaže v brskalniku in ga je možno prenesti

##  Zagon z Dockerjem

### Predpogoji

- Nameščen [Docker](https://www.docker.com/get-started)


### Docker Build & Run

```bash
# 1. Zgradite Docker sliko
docker build -t meme-generator .

# 2. Zaženite kontejner
docker run -p 5000:5000 meme-generator

# 3. Odprite v brskalniku
http://localhost:5000
```


## Kako uporabljati aplikacijo

1. Odprite http://localhost:5000 v brskalniku
2. Kliknite na "Naloži sliko" in izberite sliko (PNG, JPG, GIF)
3. Vnesite zgornji tekst (npr. "Ko programiraš ob 3h zjutraj...")
4. Vnesite spodnji tekst (npr. "...ampak koda deluje ")
5. Kliknite "Generiraj Meme!"
6. Počakajte nekaj sekund - vaš meme bo prikazan
7. Kliknite "Prenesi Meme" za prenos

##  Avtor

Matija Dukarić

```



