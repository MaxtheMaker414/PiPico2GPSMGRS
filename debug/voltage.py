import time
from machine import ADC, Pin

# Definition der Pins für VSYS und VBUS
VSYS_PIN = ADC(29)  # VSYS misst die Eingangsspannung
VBUS_DETECT_PIN = Pin(24, Pin.IN)  # VBUS erkennt, ob USB angeschlossen ist

REFERENCE_VOLTAGE = 3.3  # Referenzspannung des ADC
RESISTOR_RATIO = 2  # Falls ein Spannungsteiler verwendet wird

def read_voltage(adc_pin):
    """Liest die Spannung am angegebenen ADC-Pin aus."""
    raw_value = adc_pin.read_u16()
    voltage = (raw_value / 65535.0) * REFERENCE_VOLTAGE * RESISTOR_RATIO
    return round(voltage, 2)

while True:
    vsys_voltage = read_voltage(VSYS_PIN)
    usb_connected = VBUS_DETECT_PIN.value()  # 1 = USB angeschlossen, 0 = nicht angeschlossen
    
    if usb_connected:
        print("USB angeschlossen")
    else:
        print(f"{vsys_voltage}V")
    
    time.sleep(1)

