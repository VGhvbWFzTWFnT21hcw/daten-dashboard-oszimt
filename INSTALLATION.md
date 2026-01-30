# Installationsanleitung

Diese Anleitung beschreibt die Installation und Einrichtung des Daten-Dashboards Schritt für Schritt.

## Voraussetzungen

### Systemanforderungen

- **Betriebssystem**: Windows 10/11, macOS oder Linux
- **RAM**: Mindestens 4 GB (8 GB empfohlen)
- **Festplattenspeicher**: Mindestens 500 MB freier Speicherplatz

### Software-Voraussetzungen

1. **Python 3.8 oder höher**
   - Download: [python.org/downloads](https://www.python.org/downloads/)
   - Bei der Installation auf Windows: "Add Python to PATH" aktivieren

2. **Git** (optional, für das Klonen des Repositories)
   - Download: [git-scm.com](https://git-scm.com/)

3. **pip** (Python-Paketmanager)
   - Wird normalerweise mit Python installiert
   - Aktualisieren mit: `python -m pip install --upgrade pip`

## Installation

### Schritt 1: Repository herunterladen

**Option A: Mit Git (empfohlen)**
```bash
git clone https://github.com/VGhvbWFzTWFnT21hcw/daten-dashboard-oszimt.git
cd daten-dashboard-oszimt
```

**Option B: Als ZIP-Datei**
1. Gehe zu https://github.com/VGhvbWFzTWFnT21hcw/daten-dashboard-oszimt
2. Klicke auf "Code" > "Download ZIP"
3. Entpacke die ZIP-Datei
4. Öffne ein Terminal im entpackten Ordner

### Schritt 2: Virtuelle Umgebung erstellen

Eine virtuelle Umgebung isoliert die Projektabhängigkeiten vom System-Python.

```bash
# Virtuelle Umgebung erstellen
python -m venv venv
```

### Schritt 3: Virtuelle Umgebung aktivieren

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

> Falls ein Fehler auftritt, führe zuerst aus:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

**macOS/Linux:**
```bash
source venv/bin/activate
```

Nach der Aktivierung sollte `(venv)` am Anfang der Kommandozeile erscheinen.

### Schritt 4: Abhängigkeiten installieren

```bash
pip install -r dashboard-app/dashboard/requirements.txt
```

Dies installiert folgende Pakete:
- `faicons` - Font Awesome Icons
- `ipyleaflet` - Interaktive Karten
- `pandas` - Datenverarbeitung
- `plotly` - Interaktive Diagramme
- `shiny` - Web-Framework
- `shinylive` - Shiny-Erweiterungen
- `shinywidgets` - Widget-Bibliothek

### Schritt 5: Anwendung starten

```bash
cd dashboard-app/dashboard
shiny run app.py
```

### Schritt 6: Dashboard öffnen

Öffne einen Webbrowser und navigiere zu:
```
http://127.0.0.1:8000
```

## Fehlerbehebung

### Problem: "python" wird nicht erkannt

**Lösung:** Python ist nicht im PATH. Entweder:
- Python neu installieren und "Add to PATH" aktivieren
- Oder den vollständigen Pfad verwenden (z.B. `C:\Python311\python.exe`)

### Problem: pip-Installation schlägt fehl

**Lösung:** pip aktualisieren:
```bash
python -m pip install --upgrade pip
```

### Problem: PowerShell-Skriptausführung blockiert

**Lösung:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Problem: Port 8000 bereits belegt

**Lösung:** Anderen Port verwenden:
```bash
shiny run app.py --port 8080
```

### Problem: Karte lädt sehr langsam

**Lösung:**
- Chrome statt Safari verwenden (bessere Performance)
- Seite auf 80% zoomen für bessere Übersicht
- Ersten Start abwarten (Dateien werden gecached)

### Problem: Module nicht gefunden

**Lösung:** Sicherstellen, dass die virtuelle Umgebung aktiviert ist:
- `(venv)` sollte am Anfang der Kommandozeile erscheinen
- Falls nicht: virtuelle Umgebung erneut aktivieren

## Deinstallation

```bash
# Virtuelle Umgebung deaktivieren
deactivate

# Projektordner löschen
# Windows:
rmdir /s /q daten-dashboard-oszimt

# macOS/Linux:
rm -rf daten-dashboard-oszimt
```

## Entwicklungsumgebung

### Empfohlene IDEs

- **PyCharm** (Community oder Professional)
- **Visual Studio Code** mit Python-Erweiterung
- **JetBrains DataSpell** für Data Science

### Nützliche VS Code Erweiterungen

- Python (Microsoft)
- Pylance
- Python Debugger

## Weiterführende Links

- [Python Shiny Dokumentation](https://shiny.posit.co/py/)
- [Plotly Python Dokumentation](https://plotly.com/python/)
- [ipyleaflet Dokumentation](https://ipyleaflet.readthedocs.io/)
- [Pandas Dokumentation](https://pandas.pydata.org/docs/)
