import time
from machine import Pin
import config
import gfx_pack
import icons

# Initialisierung des Pimoroni GFX Pack
board = gfx_pack.GfxPack()
display = board.display

# Definition der Tasten mit Pull-Up-Widerständen
BUTTONS = {
    "A": Pin(12, Pin.IN, Pin.PULL_UP),  # Nächste Seite
    "B": Pin(13, Pin.IN, Pin.PULL_UP),  # Vorherige Seite
}

# Helligkeit und Hintergrundfarbe setzen
config.init_backlight(board, display)

# Schriftart für das Display
display.set_font("bitmap8")

# Globale Variable für aktuelle Seite
current_page = 0

# 🔋 Kleines Batteriesymbol (wird in Statusleiste gezeichnet)
def draw_small_battery_icon(voltage, x, y):
    width = 12
    height = 6
    tip_width = 2
    tip_height = 4
    display.set_pen(config.FOREGROUND_COLOR)
    display.rectangle(x, y, width, height)
    display.rectangle(x + width, y + 1, tip_width, tip_height)

    # Innerer Bereich zuerst leer
    display.set_pen(config.BACKGROUND_COLOR)
    display.rectangle(x + 1, y + 1, width - 2, height - 2)

    # Füllstand berechnen (4 Blöcke → 0–100%)
    level = min(max(int((voltage - 3.3) / 0.6 * 4), 1), 4)
    fill_width = ((width - 2) // 4) * level

    display.set_pen(config.FOREGROUND_COLOR)
    display.rectangle(x + 1, y + 1, fill_width, height - 2)

# 🔧 Statuszeile oben auf dem Display (Satelliten, Fix, Akku)
def draw_status_bar():
    x, y = 2, 2
    display.set_pen(config.FOREGROUND_COLOR)

    # GPS-Symbol (kleines Icon)
    icons.draw_icon("gps", display, x, y, scale=1)

    # Sat-Anzahl + Fix-Status
    sat_text = f"({config.NUM_SATS})"
    fix_text = config.FIX_TYPE
    display.text(sat_text, x + 8, y, 128, 1)
    display.text(fix_text, x + 30, y, 128, 1)

    # Akkuanzeige
    draw_small_battery_icon(config.DUMMY_BATTERY_VOLTAGE, 114, y)

# 🔢 Seitenzahl unten rechts anzeigen
def draw_page_number(page):
    display.set_pen(config.FOREGROUND_COLOR)
    display.text(str(page), 120, 56, 128, 1)

# 🧭 Berechnung der Richtung (Text) anhand Gradzahl
def get_compass_direction(degrees):
    try:
        deg = float(degrees)
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        index = int((deg + 22.5) % 360 // 45)
        return directions[index]
    except:
        return 'N'

# 📄 Alle Seiteninhalte: Titel, Daten, Anzeigeoption
def get_live_pages_content():
    return [
        {"title": "", "subtitle": "", "data": config.CURRENT_MGRS, "show_status_bar": True},
        {"title": "GPS-Daten", "subtitle": None, "data": f"Sat: {config.NUM_SATS}, Fix: {config.FIX_TYPE}", "show_status_bar": True},
        {"title": "", "subtitle": None, "data": f"{config.SPEED_KMH} km/h  {config.COURSE}°", "show_status_bar": True},
        {"title": "Uhrzeit", "subtitle": None, "data": f"{config.TIME_UTC} UTC\n{config.DATE_UTC}", "show_status_bar": True},
        {"title": "Akkuspannung", "subtitle": None, "data": f"{config.DUMMY_BATTERY_VOLTAGE:.2f} V", "show_status_bar": True},
    ]

# 🖼️ Zentrale Funktion zum Zeichnen einer Seite
def draw_page_generic(page_num):
    display.set_pen(config.BACKGROUND_COLOR)
    display.clear()
    page_info = get_live_pages_content()[page_num]

    # Statuszeile oben, falls aktiv
    if page_info["show_status_bar"]:
        draw_status_bar()

    display.set_pen(config.FOREGROUND_COLOR)

    # Seitentitel
    if page_info["title"]:
        display.text(page_info["title"], 5, 14, 128, 2)

    # Untertitel (z. B. "MGRS:")
    if page_info["subtitle"]:
        display.text(page_info["subtitle"], 5, 34, 128, 1)

    # Datendarstellung
    if page_info["data"]:
        # 👁️ Spezialfall: Seite 0 – MGRS-Formatierung
        if page_num == 0 and isinstance(page_info["data"], str) and len(page_info["data"]) >= 15:
            mgrs = page_info["data"]
            part1 = mgrs[0:3]     # Zone
            part2 = mgrs[3:5]     # Grid
            part3 = mgrs[5:10]    # Easting
            part4 = mgrs[10:15]   # Northing

            display.text(part1, 5, 16, 128, 1)        # links oben
            display.text(part2, 5, 28, 128, 2)        # VS groß
            display.text("MGRS", 108, 18, 128, 1)     # rechts oben

            display.text(part3, 28, 17, 128, 3)       # Easting groß
            display.text(part4, 28, 40, 128, 3)       # Northing groß

        # 🎯 Mehrzeilige Anzeige
        elif "\n" in str(page_info["data"]):
            for i, line in enumerate(str(page_info["data"]).split("\n")):
                display.text(line, 5, 44 + i*10, 128, 1)

        # 🔤 Einzeilige Anzeige
        else:
            display.text(str(page_info["data"]), 5, 44, 128, 1)

    # 🧭 Spezialfall Seite 2: Kompasspfeil
    if page_num == 2:
        direction = get_compass_direction(config.COURSE)
        display.set_pen(config.FOREGROUND_COLOR)
        display.text(direction, 60, 6, 128, 1)  # Richtungstext (z. B. "SW")
        icons.draw_compass_arrow(display, 56, 18, direction)  # Symbol darunter

    # Seitenzähler unten rechts
    draw_page_number(page_num + 1)

    display.update()

# 🟢 Startanzeige bei Systemstart
def init_display():
    global current_page
    current_page = 0
    draw_page_generic(current_page)

# 🔁 Zyklischer Aufruf im Hauptprogramm (Buttonsteuerung + Refresh)
def run_display_step():
    global current_page
    pressed = [name for name, pin in BUTTONS.items() if not pin.value()]

    if "A" in pressed:
        current_page = (current_page + 1) % len(get_live_pages_content())
        draw_page_generic(current_page)
        time.sleep(0.2)

    elif "B" in pressed:
        current_page = (current_page - 1) % len(get_live_pages_content())
        draw_page_generic(current_page)
        time.sleep(0.2)

    elif config.SHOULD_REFRESH_DISPLAY:
        draw_page_generic(current_page)
        config.SHOULD_REFRESH_DISPLAY = False
