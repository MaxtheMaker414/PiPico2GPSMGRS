from machine import Pin
import time

# Beispiel: Falls die Pins bekannt sind (ersetze durch echte Pin-Nummern!)
pins = {
    "A": Pin(12, Pin.IN, Pin.PULL_UP),
    "B": Pin(13, Pin.IN, Pin.PULL_UP),
    "C": Pin(14, Pin.IN, Pin.PULL_UP),
    "D": Pin(15, Pin.IN, Pin.PULL_UP),
    "E": Pin(22, Pin.IN, Pin.PULL_UP),
}

while True:
    raw_gpio_values = {key: pin.value() for key, pin in pins.items()}
    print(f"Direkte GPIO-Werte: {raw_gpio_values}")
    time.sleep(0.5)
