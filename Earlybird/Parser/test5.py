import machine
import utime
from pynmeagps.nmeareader import NMEAReader
from pynmeagps.exceptions import NMEAParseError

# UART Initialisierung für RS485 (Pin 4 = TX, Pin 5 = RX)
uart1 = machine.UART(1, baudrate=115200, tx=machine.Pin(4), rx=machine.Pin(5))

# Zuordnung der Talker-IDs zu GNSS-Systemen
TALKER_ID_MAPPING = {
    "GP": "GPS",
    "GN": "GNSS (Kombiniert)",
    "GL": "GLONASS",
    "GA": "Galileo",
    "GB": "BeiDou",
    "GI": "NavIC",
    "IN": "INS"
}

def parse_nmea_message(parsed_data):
    """Verarbeitet eine NMEA-Nachricht und zeigt nur gültige Werte mit den korrekten Bezeichnungen an."""
    talker_id = parsed_data.talker
    msg_type = parsed_data.msgID
    gnss_system = TALKER_ID_MAPPING.get(talker_id, "Unbekanntes System")

    print(f"\n✅ Geparste Nachricht: {msg_type} (Talker ID: {talker_id} - {gnss_system})")

    if not parsed_data.payload or all(v in ["", None] for v in parsed_data.payload):
        print("⚠ Die Nachricht enthält keine gültigen Werte.")
        return

    if msg_type == "GGA":
        fix_quality = parsed_data.payload[5] if len(parsed_data.payload) > 5 else 'N/A'
        num_sats = parsed_data.payload[7] if len(parsed_data.payload) > 7 else 'N/A'
        altitude = parsed_data.payload[9] if len(parsed_data.payload) > 9 else 'N/A'
        altitude_unit = parsed_data.payload[10] if len(parsed_data.payload) > 10 else 'N/A'

        print(f"📍 Latitude: {parsed_data.payload[1]} {parsed_data.payload[2]}")
        print(f"📍 Longitude: {parsed_data.payload[3]} {parsed_data.payload[4]}")
        print(f"🏔 Altitude: {altitude} {altitude_unit}")
        print(f"🛰 Satelliten in Nutzung: {num_sats}")
        print(f"🔧 Fix Quality: {fix_quality}")

    elif msg_type == "GSA":
        fix_mode = parsed_data.payload[1] if len(parsed_data.payload) > 1 else 'N/A'  # 1=kein Fix, 2=2D, 3=3D
        fix_text = {"1": "Kein Fix", "2": "2D-Fix", "3": "3D-Fix"}.get(fix_mode, "Unbekannt")
        pdop = parsed_data.payload[14] if len(parsed_data.payload) > 14 else 'N/A'
        hdop = parsed_data.payload[15] if len(parsed_data.payload) > 15 else 'N/A'
        vdop = parsed_data.payload[16] if len(parsed_data.payload) > 16 else 'N/A'

        active_sats = []
        for i in range(2, 14):  # Die aktiven Satelliten sind in den Feldern 2-13
            if len(parsed_data.payload) > i and parsed_data.payload[i] not in ["", None]:
                active_sats.append(parsed_data.payload[i])

        print(f"📡 Fix: {fix_text}")
        print(f"🛰 Aktive Satelliten ({len(active_sats)}): {', '.join(active_sats) if active_sats else 'N/A'}")
        print(f"📏 PDOP: {pdop}, HDOP: {hdop}, VDOP: {vdop}")

    elif msg_type == "GLL":
        latitude = parsed_data.payload[1] if len(parsed_data.payload) > 1 else 'N/A'
        lat_dir = parsed_data.payload[2] if len(parsed_data.payload) > 2 else 'N/A'
        longitude = parsed_data.payload[3] if len(parsed_data.payload) > 3 else 'N/A'
        lon_dir = parsed_data.payload[4] if len(parsed_data.payload) > 4 else 'N/A'
        time_utc = parsed_data.payload[5] if len(parsed_data.payload) > 5 else 'N/A'  # ✅ UTC-Zeitfeld korrekt gesetzt
        status = parsed_data.payload[6] if len(parsed_data.payload) > 6 else 'N/A'

        print(f"⏰ Zeit UTC: {time_utc}")
        print(f"📍 Latitude: {latitude} {lat_dir}")
        print(f"📍 Longitude: {longitude} {lon_dir}")
        print(f"🔄 Status: {'Valid' if status == 'A' else 'Invalid'}")

def read_nmea():
    """Liest und verarbeitet NMEA-Daten von der GPS-UART-Schnittstelle mit Debugging."""
    reader = NMEAReader(uart1)

    while True:
        try:
            print("🔄 Warte auf GPS-Daten...")

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
