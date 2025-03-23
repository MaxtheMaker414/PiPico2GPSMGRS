# config.py

# ------------------------------------------------------
# 💡 Display-Helligkeit (Wert: 0.0 – 1.0)
# ------------------------------------------------------
# Diese Einstellung beeinflusst die eigentliche Display-Hintergrundhelligkeit,
# nicht die RGB-Hintergrundbeleuchtung des Boards.
# Wert 0 = dunkel, 1 = maximale Helligkeit
DISPLAY_BRIGHTNESS = 0.5  # Empfehlung: 0.3–0.6 für angenehmes Ablesen

# ------------------------------------------------------
# 🌈 RGB-Backlight Farbe (nur für Pimoroni GFX Pack)
# ------------------------------------------------------
# Diese RGB-Werte steuern die separate Hintergrund-LED des GFX-Packs.
# Wertebereich pro Kanal: 0–255
# Beispiel:
# - (255, 0, 0)   → Rot
# - (0, 255, 0)   → Grün
# - (0, 0, 255)   → Blau
# - (0, 0, 0)     → Aus
# - (0, 0, 50)    → Dunkelblau für Nachtmodus
BACKLIGHT_COLOR = (0, 0, 255)

# ------------------------------------------------------
# 🎨 Farben für Text und Hintergrund auf dem Display
# ------------------------------------------------------
# FOREGROUND_COLOR → Farbe für Text und Symbole
# BACKGROUND_COLOR → Farbe für leeren Hintergrund (Clear-Screen)
# Farbbereiche hängen vom Displaytyp ab – meist 0–15 (4 Bit)
BACKGROUND_COLOR = 0    # 0 = Schwarz
FOREGROUND_COLOR = 15   # 15 = Weiß

# ------------------------------------------------------
# 🛠 Initialisierung der Hintergrundbeleuchtung
# ------------------------------------------------------
# Diese Funktion wird beim Start ausgeführt und steuert:
# - RGB-Farbe
# - Display-Helligkeit separat
def init_backlight(board, display):
    """
    Setzt die Hintergrundbeleuchtung (RGB-Farbe) und Display-Helligkeit.
    """
    board.set_backlight(*BACKLIGHT_COLOR)
    display.set_backlight(DISPLAY_BRIGHTNESS)


# ------------------------------------------------------
# 📄 Seiten-Management (optional bei mehrseitigem System)
# ------------------------------------------------------
PAGES = {
    1: True,
    2: True,
    3: True,
    4: True,
    5: True,
    6: True
}

START_PAGE = 1  # Startseite beim Start (Index basiert auf 0 → Seite 1 = Index 0)

# ------------------------------------------------------
# 📡 Live-Daten vom GPS-Parser (werden dynamisch gesetzt)
# ------------------------------------------------------
CURRENT_MGRS = ""
NUM_SATS = 0
FIX_TYPE = "No Fix"
SPEED_KMH = "0.0"
COURSE = "0"
DATE_UTC = "------"
TIME_UTC = "--:--:--"

# ------------------------------------------------------
# 🔁 Anzeige-Aktualisierung vom Parser auslösen
# ------------------------------------------------------
SHOULD_REFRESH_DISPLAY = False

# ------------------------------------------------------
# 🔋 Batterieanzeige – Dummywert (kann später aus ADC kommen)
# ------------------------------------------------------
DUMMY_BATTERY_VOLTAGE = 3.7

