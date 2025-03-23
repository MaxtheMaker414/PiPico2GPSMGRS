# 🛰️ RS485 GPS Logger mit MGRS-Anzeige auf Pico 2 + GFX Pack

Dieses Projekt verbindet ein NMEA-kompatibles GPS-Modul über RS485 mit einem **Raspberry Pi Pico 2**, nutzt die **Pimoroni GFX LCD-Anzeige** und zeigt live **MGRS-Koordinaten, Kurs, Uhrzeit und Systemstatus** an. Die Daten werden über einen Parser interpretiert und als Seiten auf dem Display dargestellt.

---

## 📦 Verwendete Hardware

- 🧭 **NMEA-GPS-Modul** (uBlox)
- 🔌 **RS485-Konverter** (UART-basiert)
- 🧠 **Raspberry Pi Pico 2**
- 🖼️ **Pimoroni GFX Pack LCD (128x64)**
- 🔋 **2x Stromversorgung**

---

## 📡 Signalweg & Datenfluss

```text
+-------------+      UART/RS485      +-----------+      I2C/GPIO       +------------------+
| NMEA-GPS    |  →  RS485-Treiber →  | Raspberry |  →  Pimoroni GFX   | LCD Display       |
| Modul       |                      | Pi Pico 2 |                     | (Koordinatenanzeige)
+-------------+                      +-----------+                     +------------------+
        ↑                                ↑
   NMEA-Daten:                         Python-Skripte
   $GGA, $GLL, etc.                    parser.py, display.py
```

---

## 💾 Firmware & Setup

1. **Firmware flashen**  
   Lade die passende Firmware von Pimoroni:

   🔗 [pico2-v0.0.12-pimoroni-micropython.uf2](https://github.com/pimoroni/pimoroni-pico/releases)

2. **Installationsschritte**

   - Drücke `BOOTSEL` auf dem Pico 2
   - Schließe über USB an → erscheint als Laufwerk
   - Kopiere die `.uf2` Datei auf den Pico
   - Nach dem Reboot: Pimoroni Bibliotheken sind aktiv

3. **REPL Zugriff (z. B. über Thonny)**  
   IDE verbinden und Skripte hochladen

---

## 🗂️ Python-Dateien & Aufgaben

| Datei             | Aufgabe                                         |
|------------------|--------------------------------------------------|
| `main.py`         | Hauptloop: verbindet Parser und Display         |
| `parser.py`       | NMEA-Daten lesen, analysieren, Koordinaten parsen |
| `display.py`      | Seitenlogik, Buttons, Layout auf dem GFX-Pack   |
| `config.py`       | Zentrale Variablen, Statuswerte, Farben         |
| `icons.py`        | Symbole, Kompasspfeile, Batteriegrafik          |
| `gfx_pack`        | Hardware-Ansteuerung (Bibliothek von Pimoroni)  |

---

## 🧠 NMEA-Datensätze, die der Parser unterstützt

| Typ   | Beschreibung                                |
|-------|---------------------------------------------|
| `$GGA` | Position, Satellitenanzahl, Fixqualität     |
| `$GLL` | Geografische Position                       |
| `$RMC` | Kurs, Geschwindigkeit, Zeit & Datum         |

➡️ Daraus werden folgende Daten extrahiert:

- 🛰️ Satellitenanzahl
- 📍 Latitude / Longitude
- 🔁 MGRS-Koordinaten
- 🧭 Kurs (° und Symbol)
- ⏰ UTC-Zeit & Datum
- 🚀 Geschwindigkeit in km/h

---

## 📺 Displayseiten

| Seite     | Inhalt                                 | Besonderheiten                            |
|-----------|----------------------------------------|--------------------------------------------|
| 1 – Start | **MGRS-Zone + Grid + Easting + Northing** | MGRS ist aufgeteilt & groß dargestellt     |
| 2 – GPS   | Satellitenanzahl & Fix-Status          | oben in der Statusleiste                   |
| 3 – Course| Richtung (°) + **Kompasspfeil**         | Richtungsanzeige mit großem Pfeil          |
| 4 – Zeit  | UTC-Zeit + Datum (aus RMC/GGA)         | zweizeilig, synchronisiert                 |
| 5 – Akku  | Batteriesymbol + Spannung               | visuell mit Balken                         |

---

## 🎮 Tastenbelegung

| Taste | Funktion                     |
|-------|------------------------------|
| `A`   | nächste Seite                |
| `B`   | vorherige Seite              |

---

## 🌈 Displayhelligkeit & Hintergrundfarbe

Die Helligkeit und Hintergrundfarbe werden über `config.py` gesteuert:

```python
# config.py

DISPLAY_BRIGHTNESS = 0.5  # Skala 0.0 – 1.0
BACKLIGHT_COLOR = (255, 0, 0)  # RGB (rot)

def init_backlight(board, display):
    board.set_backlight(*BACKLIGHT_COLOR)
    display.set_backlight(int(DISPLAY_BRIGHTNESS * 255))
```

➡️ Passe die Farbe an z. B. für Nachtbetrieb:  
```python
BACKLIGHT_COLOR = (0, 0, 50)  # gedimmtes Blau
```

---

## 🧪 Erweiterungen möglich

- 🔄 Logging auf SD-Karte
- 💡 Helligkeit steuerbar per Tasten
- 📈 Anzeige von DOP-Werten (PDOP/HDOP/VDOP)
- 📍 Zielnavigation / Richtungsführung
