# config.py

# Display-Helligkeit
DISPLAY_BRIGHTNESS = 0.5

# Backlight-Farbe als RGB-Tupel
BACKLIGHT_COLOR = (255, 0, 0)

# Hintergrund- und Vordergrundfarbe
BACKGROUND_COLOR = 0    # Schwarz
FOREGROUND_COLOR = 15   # Weiß

def init_backlight(board, display):
    """
    Setzt die Hintergrundbeleuchtung (RGB-Farbe) und dunkelt das Display selbst ab (0).
    """
    # Erst Farbhintergrund der LED(s) setzen
    board.set_backlight(*BACKLIGHT_COLOR)

    # Zusätzlich Display-Helligkeit auf 0 setzen
    display.set_backlight(0)

# Die restlichen Einstellungen, Dummy-Daten usw. bleiben unverändert
PAGES = {
    1: True,
    2: True,
    3: True,
    4: True,
    5: True,
    6: True
}

START_PAGE = 1
# Live-Daten vom Parser
CURRENT_MGRS = ""
NUM_SATS = 0
FIX_TYPE = "No Fix"
SPEED_KMH = "0.0"
COURSE = "0"
DATE_UTC = "------"
TIME_UTC = "--:--:--"

# Steuerflag für Display-Update
SHOULD_REFRESH_DISPLAY = False

# Dummy nur für Batterie
DUMMY_BATTERY_VOLTAGE = 3.7


#DUMMY_SATELLITES = 5
#DUMMY_FIX = True
