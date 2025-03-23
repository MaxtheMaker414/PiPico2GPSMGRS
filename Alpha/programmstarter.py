import parser  # dein GPS-Parser mit parse_nmea_step(uart) Funktion
import display  # dein Display mit display.run_display_step()
import config
import machine
import utime

# UART-Initialisierung wie im parser
uart1 = machine.UART(1, baudrate=115200, tx=machine.Pin(4), rx=machine.Pin(5))

def main_loop():
    display.init_display()  # Display vorbereiten (Setup aus display.py)
    
    while True:
        # 1. GPS-Daten verarbeiten
        parser.parse_nmea_step(uart1)

        # 2. Display aktualisieren
        display.run_display_step()

        # 3. Kurze Pause für gleichmäßiges Timing
        utime.sleep_ms(100)

if __name__ == "__main__":
    main_loop()
