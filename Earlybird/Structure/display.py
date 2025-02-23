# display.py
# Hauptprogramm zur Darstellung der Seiten (generisch) auf dem Pico GFX Pack

import time
import config
import gfx_pack
import icons

# Initialisierung von Board und Display
board = gfx_pack.GfxPack()
display = board.display

# Hintergrundbeleuchtung zentral über config steuern
config.init_backlight(board, display)

# Schriftart setzen
display.set_font("bitmap8")

def draw_small_battery_icon(voltage, x, y):
    """
    Zeichnet ein kleineres Batteriesymbol (12x6 Pixel).
    Füllstand ermittelt sich aus der Spannung.
    """
    width = 12
    height = 6
    tip_width = 2
    tip_height = 4

    # Rahmen
    display.set_pen(config.FOREGROUND_COLOR)
    display.rectangle(x, y, width, height)
    display.rectangle(x + width, y + 1, tip_width, tip_height)

    # Innenfläche leeren
    display.set_pen(config.BACKGROUND_COLOR)
    display.rectangle(x + 1, y + 1, width - 2, height - 2)

    # Batterie-Level bestimmen
    if voltage < 3.5:
        level = 1
    elif voltage < 3.7:
        level = 2
    elif voltage < 3.9:
        level = 3
    else:
        level = 4

    fill_width = ((width - 2) // 4) * level

    # Gefüllter Teil
    display.set_pen(config.FOREGROUND_COLOR)
    display.rectangle(x + 1, y + 1, fill_width, height - 2)

def draw_status_bar():
    """
    Zeichnet die gemeinsame Statuszeile oben auf den Seiten.
    Links: GPS-Icon (Kreis),
    Mitte: Satellitenanzahl und Fix-Status,
    Rechts: Batteriesymbol.
    """
    x = 2
    y = 2
    display.set_pen(config.FOREGROUND_COLOR)

    # GPS-Icon
    icons.draw_icon("gps", display, x, y, scale=1)

    # Satellitenanzahl
    sat_text = f"({config.DUMMY_SATELLITES})"
    display.text(sat_text, x + 8, y, 128, 1)

    # Fix-Status
    fix_text = "Fix" if config.DUMMY_FIX else "No Fix"
    display.text(fix_text, x + 30, y, 128, 1)

    # Battery-Symbol rechts
    draw_small_battery_icon(config.DUMMY_BATTERY_VOLTAGE, 114, y)

def draw_page_number(page):
    """
    Zeichnet die Seitenzahl in der unteren rechten Ecke.
    """
    display.set_pen(config.FOREGROUND_COLOR)
    display.text(str(page), 120, 56, 128, 1)

# Definiere den Inhalt aller Seiten in einer Datenstruktur
# show_status_bar = True/False steuert, ob oben die Statuszeile gezeichnet wird
PAGES_CONTENT = [
    {
        "title": "Startseite",
        "subtitle": "Koordinaten:",
        "data": config.DUMMY_COORDINATES,
        "show_status_bar": True
    },
    {
        "title": "GPS-Daten",
        "subtitle": None,
        "data": config.DUMMY_GPS_DATA,
        "show_status_bar": True
    },
    {
        "title": "Akkuspannung",
        "subtitle": None,
        "data": f"Spannung: {config.DUMMY_BATTERY_VOLTAGE} V",
        "show_status_bar": True
    },
    {
        "title": "Parameter A: Dummy",
        "subtitle": None,
        "data": None,
        "show_status_bar": True
    },
    {
        "title": "Parameter B: Dummy",
        "subtitle": None,
        "data": None,
        "show_status_bar": True
    },
    {
        "title": "Einstellungen",
        "subtitle": None,
        "data": None,
        "show_status_bar": False
    },
]

def draw_page_generic(page_num):
    """
    Zeichnet eine Seite anhand der Daten in PAGES_CONTENT.
    page_num: Index in der PAGES_CONTENT-Liste (0-basiert).
    """
    display.set_pen(config.BACKGROUND_COLOR)
    display.clear()
    display.update()

    page_info = PAGES_CONTENT[page_num]

    if page_info["show_status_bar"]:
        draw_status_bar()

    display.set_pen(config.FOREGROUND_COLOR)

    if page_info["title"]:
        display.text(page_info["title"], 5, 14, 128, 2)

    if page_info["subtitle"]:
        display.text(page_info["subtitle"], 5, 34, 128, 1)

    if page_info["data"]:
        display.text(str(page_info["data"]), 5, 44, 128, 1)

    # Seitenzahl
    draw_page_number(page_num + 1)
    display.update()

# Endlosschleife: Blättert alle aktivierten Seiten durch
current_page = config.START_PAGE - 1
total_pages = len(PAGES_CONTENT)

while True:
    # Überspringe Seiten, die in config.PAGES als False markiert sind
    if config.PAGES.get(current_page + 1, False):
        draw_page_generic(current_page)
        time.sleep(3)
    current_page = (current_page + 1) % total_pages
