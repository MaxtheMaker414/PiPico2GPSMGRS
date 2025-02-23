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

DUMMY_COORDINATES = "Lat: 51.1234, Lon: 7.5678"
DUMMY_GPS_DATA = "Sat: 5, Fix: 3D"
DUMMY_BATTERY_VOLTAGE = 3.7

DUMMY_SATELLITES = 5
DUMMY_FIX = True
