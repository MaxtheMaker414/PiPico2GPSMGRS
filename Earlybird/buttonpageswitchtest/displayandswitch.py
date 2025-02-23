import time
from machine import Pin
import config
import gfx_pack
import icons

# Initialisierung von Board und Display
board = gfx_pack.GfxPack()
display = board.display

# GPIO-Pin-Definitionen für die Schalter
BUTTONS = {
    "A": Pin(12, Pin.IN, Pin.PULL_UP),
    "B": Pin(13, Pin.IN, Pin.PULL_UP),
    "C": Pin(14, Pin.IN, Pin.PULL_UP),
    "D": Pin(15, Pin.IN, Pin.PULL_UP),
    "E": Pin(22, Pin.IN, Pin.PULL_UP),
}

# Hintergrundbeleuchtung zentral über config steuern
config.init_backlight(board, display)

# Schriftart setzen
display.set_font("bitmap8")

def draw_small_battery_icon(voltage, x, y):
    """
    Zeichnet ein kleineres Batteriesymbol (12x6 Pixel).
    """
    width = 12
    height = 6
    tip_width = 2
    tip_height = 4
    display.set_pen(config.FOREGROUND_COLOR)
    display.rectangle(x, y, width, height)
    display.rectangle(x + width, y + 1, tip_width, tip_height)
    display.set_pen(config.BACKGROUND_COLOR)
    display.rectangle(x + 1, y + 1, width - 2, height - 2)
    level = min(max(int((voltage - 3.3) / 0.6 * 4), 1), 4)
    fill_width = ((width - 2) // 4) * level
    display.set_pen(config.FOREGROUND_COLOR)
    display.rectangle(x + 1, y + 1, fill_width, height - 2)

def draw_status_bar():
    """
    Zeichnet die gemeinsame Statuszeile oben auf den Seiten.
    """
    x, y = 2, 2
    display.set_pen(config.FOREGROUND_COLOR)
    icons.draw_icon("gps", display, x, y, scale=1)
    sat_text = f"({config.DUMMY_SATELLITES})"
    display.text(sat_text, x + 8, y, 128, 1)
    fix_text = "Fix" if config.DUMMY_FIX else "No Fix"
    display.text(fix_text, x + 30, y, 128, 1)
    draw_small_battery_icon(config.DUMMY_BATTERY_VOLTAGE, 114, y)

def draw_page_number(page):
    display.set_pen(config.FOREGROUND_COLOR)
    display.text(str(page), 120, 56, 128, 1)

PAGES_CONTENT = [
    {"title": "Startseite", "subtitle": "Koordinaten:", "data": config.DUMMY_COORDINATES, "show_status_bar": True},
    {"title": "GPS-Daten", "subtitle": None, "data": config.DUMMY_GPS_DATA, "show_status_bar": True},
    {"title": "Akkuspannung", "subtitle": None, "data": f"Spannung: {config.DUMMY_BATTERY_VOLTAGE} V", "show_status_bar": True},
    {"title": "Einstellungen", "subtitle": None, "data": None, "show_status_bar": False},
]

def draw_page_generic(page_num):
    display.set_pen(config.BACKGROUND_COLOR)
    display.clear()
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
    draw_page_number(page_num + 1)
    display.update()

total_pages = len(PAGES_CONTENT)
current_page = 0
draw_page_generic(current_page)

while True:
    pressed_buttons = [name for name, pin in BUTTONS.items() if not pin.value()]
    if "A" in pressed_buttons:
        current_page = (current_page + 1) % total_pages
        draw_page_generic(current_page)
        time.sleep(0.2)
    if "B" in pressed_buttons:
        current_page = (current_page - 1) % total_pages
        draw_page_generic(current_page)
        time.sleep(0.2)
    if "C" in pressed_buttons:
        board.set_backlight(255, 255, 0, 0)
        time.sleep(0.2)
    if "D" in pressed_buttons:
        board.set_backlight(*config.BACKLIGHT_COLOR)
        time.sleep(0.2)
    if "E" in pressed_buttons:
        display.set_pen(config.BACKGROUND_COLOR)
        display.clear()
        display.set_pen(config.FOREGROUND_COLOR)
        display.text("Debug-Modus!", 10, 20, 128, 2)
        display.update()
        time.sleep(0.2)
    time.sleep(0.1)

