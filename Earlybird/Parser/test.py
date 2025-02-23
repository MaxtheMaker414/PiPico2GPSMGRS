import machine
import utime
from pynmeagps.nmeareader import NMEAReader
from pynmeagps.exceptions import NMEAParseError

# UART Initialisierung für RS485 (Pin 4 = TX, Pin 5 = RX)
uart1 = machine.UART(1, baudrate=115200, tx=machine.Pin(4), rx=machine.Pin(5))

def parse_nmea_message(parsed_data):
    """Verarbeitet eine NMEA-Nachricht und zeigt nur gültige Werte."""
    msg_type = parsed_data.msgID

    print(f"\n✅ Geparste Nachricht: {msg_type}")

    if not parsed_data.payload or all(v in ["", None] for v in parsed_data.payload):
        print("⚠ Die Nachricht enthält keine gültigen Werte.")
        return

    # Falls GPS noch keinen Fix hat, die Daten ignorieren
    if msg_type == "GGA":
        fix_status = parsed_data.payload[5] if len(parsed_data.payload) > 5 else '0'
        if fix_status == '0':
            print("⚠ Kein GPS-Fix! Warte auf gültige Positionsdaten...")
            return
    
    # Ausgabe aller gültigen Werte
    print("📜 Nachrichtendaten:")
    for i, value in enumerate(parsed_data.payload):
        if value not in ["", None]:  # Nur gültige Werte anzeigen
            print(f"  🔹 Feld {i + 1}: {value}")

def read_nmea():
    """Liest und verarbeitet NMEA-Daten von der GPS-UART-Schnittstelle mit Debugging."""
    reader = NMEAReader(uart1)

    while True:
        try:
            print("🔄 Warte auf GPS-Daten...")

            # Überprüfen, ob Daten empfangen werden
            if uart1.any() > 0:
                raw_data = uart1.readline()  # Liest eine Zeile von UART
                if raw_data:
                    print(f"🔍 Rohdaten empfangen: {raw_data}")  # Debugging: Zeigt ungefilterte GPS-Daten
                    try:
                        parsed_data = NMEAReader.parse(raw_data)
                        if parsed_data:
                            parse_nmea_message(parsed_data)  # Nachricht parsen & ausgeben
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
