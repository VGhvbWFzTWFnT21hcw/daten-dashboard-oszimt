# Daten-Dashboard OSZ IMT

**Dashboardgestützte Analyse und Prognose von Energiedaten**

Ein interaktives Dashboard zur Visualisierung und Analyse von Energiedaten, entwickelt als Schulprojekt am OSZ Informationstechnik und Medizintechnik (OSZ IMT).

## Projektübersicht

Das Dashboard visualisiert Energiedaten (15-Minuten-Lastgänge) und Sonnenscheindaten über einen Zeitraum von 360 Tagen. Es ermöglicht:

- Strukturierte Darstellung von Erzeugung und Verbrauch
- Analyse des Energiemixes (erneuerbar vs. konventionell)
- Korrelation zwischen Sonnenschein und PV-Erzeugung
- Kurzfristige Verbrauchsprognose

## Funktionen

### Tab: Übersicht
- **KPIs**: Durchschnittliche Erzeugung, erneuerbarer Anteil, Verbrauch, Sonnenstunden
- **Energiemix-Diagramm**: Pie-Chart erneuerbar vs. konventionell
- **Erzeugung nach Quelle**: Balkendiagramm aller Energieträger
- **Monatliche Entwicklung**: Gestapeltes Balkendiagramm mit Verbrauchslinie

### Tab: Zeitreihen
- **Erzeugung und Verbrauch**: Tägliche Entwicklung über den gesamten Zeitraum
- **Erneuerbare Erzeugung**: Gestapelte Darstellung von Wind und Solar

### Tab: Tagesprofile
- **Durchschnittliches Tagesprofil**: Verbrauch und Erzeugung nach Stunde
- **Wochentag-Profil**: Verbrauch nach Wochentag
- **PV-Sonnenschein-Korrelation**: Zusammenhang zwischen Sonnenschein und PV-Erzeugung

### Tab: Prognose
- **7-Tage Prognose**: Basierend auf gleitendem Durchschnitt
- **Prognose-Kennzahlen**: Durchschnitt, Standardabweichung, Trend

## Datenbasis

| Datensatz | Beschreibung | Auflösung |
|-----------|--------------|-----------|
| Energiedaten | Erzeugung (Wind, Solar, Kohle, etc.) und Verbrauch | 15 Minuten |
| Sonnenscheindauer | Minuten Sonnenschein pro Intervall | 15 Minuten |

**Zeitraum**: 360 Tage (Januar - Dezember 2025)

## Technologie-Stack

| Technologie | Version | Beschreibung |
|-------------|---------|--------------|
| Python | >= 3.8 | Programmiersprache |
| Shiny | 0.10.1 | Web-Framework für interaktive Dashboards |
| Plotly | 5.22.0 | Interaktive Diagramme |
| Pandas | 2.2.2 | Datenverarbeitung |
| NumPy | - | Numerische Berechnungen |

## Schnellstart

```bash
# Repository klonen
git clone https://github.com/VGhvbWFzTWFnT21hcw/daten-dashboard-oszimt.git
cd daten-dashboard-oszimt

# Virtuelle Umgebung erstellen und aktivieren
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS

# Abhängigkeiten installieren
pip install -r dashboard-app/dashboard/requirements.txt

# Dashboard starten
cd dashboard-app/dashboard
shiny run app.py
```

Das Dashboard ist dann unter `http://127.0.0.1:8000` erreichbar.

## Dokumentation

- [Installationsanleitung](INSTALLATION.md) - Detaillierte Anweisungen zur Installation

## Projektstruktur

```
daten-dashboard-oszimt/
├── README.md                    # Diese Datei
├── INSTALLATION.md              # Installationsanleitung
├── LICENSE                      # MIT-Lizenz
└── dashboard-app/               # Dashboard-Anwendung
    └── dashboard/
        ├── app.py               # Hauptanwendung
        ├── requirements.txt     # Python-Abhängigkeiten
        ├── data/
        │   ├── energiedaten.csv     # Energiedaten (15-Min)
        │   └── sonnenschein.csv     # Sonnenscheindaten
        └── static/              # Statische Assets
```

## Features

- **Interaktive Filter**: Datumsbereich frei wählbar
- **Dark/Light Mode**: Umschaltbares Farbschema
- **Responsive Design**: Anpassung an verschiedene Bildschirmgrößen
- **Vollbild-Modus**: Diagramme im Vollbild anzeigbar

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz - siehe [LICENSE](LICENSE) für Details.

---

*Entwickelt als Schulprojekt am OSZ IMT Berlin*
