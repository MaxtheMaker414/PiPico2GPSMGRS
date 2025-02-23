import machine
import utime
from pynmeagps.nmeareader import NMEAReader
from pynmeagps.exceptions import NMEAParseError

# UART Initialisierung für RS485 (Pin 4 = TX, Pin 5 = RX)
uart1 = machine.UART(1, baudrate=115200, tx=machine.Pin(4), rx=machine.Pin(5))

def read_nmea():
    """Liest und verarbeitet NMEA-Daten von der GPS-UART-Schnittstelle mit Debugging."""
    reader = NMEAReader(uart1)

    while True:
        try:
            print("🔄 Warte auf GPS-Daten...")  # Debugging: zeigt, dass die Schleife läuft

            # Überprüfe, ob überhaupt Daten empfangen werden
            if uart1.any() > 0:
                raw_data = uart1.readline()  # Liest eine Zeile von UART
                if raw_data:
                    print(f"🔍 Rohdaten empfangen: {raw_data}")  # Debugging: zeigt rohe GPS-Daten
                    try:
                        parsed_data = NMEAReader.parse(raw_data)
                        if parsed_data:
                            print(f"✅ Geparste Nachricht: {parsed_data.msgID}")
                            print(parsed_data)
                        else:
                            print("⚠ Konnte Nachricht nicht parsen.")
                    except NMEAParseError as e:
                        print(f"❌ Fehler beim Parsen: {e}")
                else:
                    print("⚠ Keine vollständige NMEA-Nachricht empfangen.")
            else:
                print("⚠ Keine Daten auf UART empfangen.")

            utime.sleep(1)  # Wartezeit für neue Daten
        except Exception as e:  # Fängt alle unerwarteten Fehler ab
            print(f"🚨 Unerwarteter Fehler: {e}")
        except KeyboardInterrupt:
            print("🚨 Beende GPS-Reader (Strg+C erkannt).")
            break

if __name__ == "__main__":
    read_nmea()


