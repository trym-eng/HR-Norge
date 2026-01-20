# 👥 HR Analytics Dashboard

Et interaktivt HR-dashboard bygget med Streamlit som demonstrerer kraften i GenAI/vibe coding for HR-profesjonelle.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-Demo-green.svg)

## 🚀 Hurtigstart

### Installasjon

```bash
# 1. Naviger til prosjektmappen
cd hr-analytics-dashboard

# 2. Installer avhengigheter
pip install -r requirements.txt

# 3. Start dashboardet
streamlit run app.py
```

Dashboardet åpnes automatisk i nettleseren på `http://localhost:8501`

## 📊 Funksjoner

### 1. Executive Summary
- Nøkkeltall på et øyeblikk
- Automatisk beregning av KPIer basert på filtre

### 2. KPI-kort
- **Headcount** - Total arbeidsstyrke
- **Turnover Rate** - Med benchmark-sammenligning
- **Engagement Score** - 1-10 skala
- **Time to Hire** - Gjennomsnittlig rekrutteringstid
- **Sykefravær** - Prosentvis rate

### 3. 🚩 Red Flags & Varsler
Automatisk deteksjon av avvik:
- Høy turnover (>15%)
- Lavt engasjement (<6.5)
- Lang rekrutteringstid (>50 dager)
- Høyt sykefravær (>5%)
- Lønnsavvik (compa-ratio utenfor 0.9-1.1)
- Diversity gap i ledelsen (<30% kvinner)

Hver varsel har en **"Forklar hvorfor"-knapp** som gir:
- Detaljert analyse av årsaker
- Korrelasjon med andre metrics
- Anbefalte tiltak

### 4. 🎛️ Interaktive Filtre
- Land (Norge, Sverige, Danmark, Finland, Tyskland)
- Avdeling (Engineering, Sales, HR, etc.)
- Senioritetsnivå (Junior → C-Level)
- Rollefamilie
- Tidsperiode

### 5. 📈 Analyse-tabs

| Tab | Innhold |
|-----|---------|
| **Overview** | Headcount-fordeling, engasjement per avdeling |
| **Turnover** | Turnover-rate, flight risk, kostnad av attrition |
| **Workforce** | Alder, kjønn, ansiennitet, intern mobilitet |
| **Compensation** | Compa-ratio, pay equity, lønnsfordeling |
| **Recruitment** | Time-to-fill, kilder, rekrutteringstrakt |

### 6. 🔮 What-If Simulator
Simuler effekten av HR-tiltak:
- Juster **lønnsøkning** (0-20%)
- Øk **opplæringstimer**
- Aktiver **engasjementsprogram**

Se umiddelbart:
- Estimert risikoreduksjon
- Kostnad for tiltak
- Netto gevinst / ROI

### 7. 💬 Chat med Data
Still spørsmål på **norsk** og få:
- Tekstlige svar med innsikt
- Relevante grafer
- Peker til hvilke tabs som har mer info

**Eksempel-spørsmål:**
- "Hvor har vi størst lønnsavvik?"
- "Hvilken avdeling har høyest turnover?"
- "Hvordan er kjønnsfordelingen i ledelsen?"

## 📁 Filstruktur

```
hr-analytics-dashboard/
├── app.py                 # Hovedapplikasjon
├── generate_data.py       # Datagenerator (syntetisk data)
├── requirements.txt       # Python-avhengigheter
├── DATA_MODEL.md          # Dokumentasjon av datamodell
├── STORYLINES.md          # 10 storylines for ledergruppen
├── README.md              # Denne filen
└── data/
    ├── employees.csv      # 5,200 ansatte
    ├── sick_leave.csv     # Sykefraværsdata
    ├── recruitment.csv    # Rekrutteringsdata
    └── terminations.csv   # Avgangsdata
```

## 📋 Datamodell

### Hovedtabeller

1. **employees.csv** - All ansattinformasjon
   - Demografi, rolle, lønn, performance, engagement, flight risk

2. **sick_leave.csv** - Månedlig sykefravær per ansatt

3. **recruitment.csv** - Rekrutteringsprosjekter med time-to-fill

4. **terminations.csv** - Avgangsdetaljer og kostnader

### KPI-er som beregnes
- Headcount & vekst
- Turnover rate (total, frivillig, regretted)
- Time-to-hire
- Sykefraværsrate
- Engagement score
- Compa-ratio (lønnsposisjon)
- Span of control
- Intern mobilitet
- Cost of attrition

Se `DATA_MODEL.md` for komplett dokumentasjon.

## 🎯 Workshop-bruk

### Demo-flow (15-20 min)

1. **Åpne dashboardet** - vis Executive Summary
2. **Red Flags** - demonstrer automatisk anomali-deteksjon
3. **"Forklar hvorfor"** - klikk på en flag, vis AI-forklaringen
4. **Filtre** - filtrer på Tyskland → vis engasjementsproblemet
5. **What-If Simulator** - simuler effekt av lønnsøkning
6. **Chat med Data** - la publikum stille spørsmål

### Wow-momenter
- Sanntids KPI-beregning ved filterendring
- AI-genererte forklaringer på varsler
- ROI-kalkulator for HR-tiltak
- Naturlig språk-interaksjon med data

## 🔧 Tilpasning

### Bruk egne data
1. Erstatt CSV-filene i `data/`-mappen
2. Sørg for at kolonnenavnene matcher datamodellen
3. Restart Streamlit

### Regenerer syntetisk data
```bash
python generate_data.py
```

## 📄 Lisens

Dette er et demonstrasjonsprosjekt bygget for workshop-formål.
Syntetiske data - ingen ekte personopplysninger.

---

**Bygget med ❤️ for HR-profesjonelle som vil forstå kraften i GenAI**
