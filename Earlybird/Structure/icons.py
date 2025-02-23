# icons.py
# Enthält Funktionen zum Zeichnen von Icons

def draw_gps_icon(display, x, y, scale=1):
    """
    Zeichnet einen Kreis, der als GPS-Satellitensymbol dient.
    Das Symbol ist 6 Pixel breit und 6 Pixel hoch.
    Dabei wird die aktuell gesetzte Pen-Farbe verwendet.
    """
    diameter = 6
    r = diameter // 2  # Radius = 3
    cx = x + r
    cy = y + r
    for j in range(y, y + diameter):
        for i in range(x, x + diameter):
            if (i - cx) ** 2 + (j - cy) ** 2 <= r * r:
                display.pixel(i, j)

# Dictionary, in dem die Icon-Zeichenfunktionen gespeichert werden.
ICON_FUNCTIONS = {
    'gps': draw_gps_icon,
}

def draw_icon(icon_name, display, x, y, scale=1):
    """
    Zeichnet ein Icon anhand des Namens.
    
    icon_name: z.B. "gps".
    display:   Display-Objekt.
    x, y:      Position zum Zeichnen.
    scale:     Skalierungsfaktor (optional).
    """
    icon_func = ICON_FUNCTIONS.get(icon_name)
    if icon_func:
        icon_func(display, x, y, scale)
