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




Die eigene Software nutzt pynmeagps von Semuconsulting.
Diese Software unterliegt der folgenden Lizenz:

BSD 3-Clause License ("BSD License 2.0", "Revised BSD License", "New BSD License", or "Modified BSD License")

Copyright (c) 2021, SEMU Consulting
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the <organization> nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
