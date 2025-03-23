from pynmeagps.nmeareader import NMEAReader
from pynmeagps.exceptions import NMEAParseError
from mgrs import LLtoMGRS
import config

# Debug-Modus aktivieren/deaktivieren
DEBUG = True

reader = None

def parse_nmea_step(uart):
    global reader
    if reader is None:
        reader = NMEAReader(uart)

    if uart.any():
        raw_data = uart.readline()
        if raw_data:
            try:
                lines = raw_data.decode("utf-8").split("$")
                for line in lines:
                    if not line.strip():
                        continue
                    try:
                        msg = "$" + line.strip()
                        parsed = NMEAReader.parse(msg.encode("utf-8"))
                        if parsed:
                            parse_nmea_message(parsed)
                    except NMEAParseError:
                        if DEBUG:
                            print("❌ NMEA-Parsing fehlgeschlagen.")
            except Exception as e:
                if DEBUG:
                    print("❌ Fehler beim Lesen des UART-Datenstroms:", e)

def parse_nmea_message(parsed_data):
    msg_type = parsed_data.msgID
    updated = False

    try:
        if msg_type == "GGA":
            raw_time = parsed_data.payload[0]
            if raw_time and len(raw_time) >= 6:
                new_time = f"{raw_time[:2]}:{raw_time[2:4]}:{raw_time[4:6]}"
                if config.TIME_UTC != new_time:
                    config.TIME_UTC = new_time
                    updated = True
                    if DEBUG:
                        print(f"🕒 Zeit (GGA): {config.TIME_UTC}")

            lat_raw, lat_dir = parsed_data.payload[1], parsed_data.payload[2]
            lon_raw, lon_dir = parsed_data.payload[3], parsed_data.payload[4]
            num_sats = int(parsed_data.payload[6])
            fix_type = {
                "0": "No Fix", "1": "GPS", "2": "DGPS", "4": "RTK"
            }.get(parsed_data.payload[5], "Unknown")

            if config.NUM_SATS != num_sats:
                config.NUM_SATS = num_sats
                updated = True
                if DEBUG:
                    print(f"🛰 Satelliten: {config.NUM_SATS}")

            if config.FIX_TYPE != fix_type:
                config.FIX_TYPE = fix_type
                updated = True
                if DEBUG:
                    print(f"🔧 Fix-Typ: {config.FIX_TYPE}")

            if _set_coords(lat_raw, lat_dir, lon_raw, lon_dir):
                updated = True

        elif msg_type == "GLL":
            lat_raw, lat_dir = parsed_data.payload[0], parsed_data.payload[1]
            lon_raw, lon_dir = parsed_data.payload[2], parsed_data.payload[3]
            if _set_coords(lat_raw, lat_dir, lon_raw, lon_dir):
                updated = True

        elif msg_type == "RMC":
            raw_time = parsed_data.payload[0]
            raw_date = parsed_data.payload[8]
            new_speed = str(round(float(parsed_data.payload[6]) * 1.852, 1))  # knots → km/h
            new_course = parsed_data.payload[7]

            if raw_time and len(raw_time) >= 6:
                new_time = f"{raw_time[:2]}:{raw_time[2:4]}:{raw_time[4:6]}"
                if config.TIME_UTC != new_time:
                    config.TIME_UTC = new_time
                    updated = True
                    if DEBUG:
                        print(f"🕒 Zeit (RMC): {config.TIME_UTC}")

            if config.DATE_UTC != raw_date:
                config.DATE_UTC = raw_date
                updated = True
                if DEBUG:
                    print(f"📆 Datum: {config.DATE_UTC}")

            if config.SPEED_KMH != new_speed:
                config.SPEED_KMH = new_speed
                updated = True
                if DEBUG:
                    print(f"🚀 Geschwindigkeit: {config.SPEED_KMH} km/h")

            if config.COURSE != new_course:
                config.COURSE = new_course
                updated = True
                if DEBUG:
                    print(f"🧭 Kurs: {config.COURSE}°")

    except Exception as e:
        if DEBUG:
            print("❌ Parser-Fehler:", e)

    if updated:
        config.SHOULD_REFRESH_DISPLAY = True

def _set_coords(lat_raw, lat_dir, lon_raw, lon_dir):
    try:
        lat = float(lat_raw[:2]) + float(lat_raw[2:]) / 60
        lon = float(lon_raw[:3]) + float(lon_raw[3:]) / 60
        if lat_dir == "S":
            lat *= -1
        if lon_dir == "W":
            lon *= -1
        new_mgrs = LLtoMGRS(lat, lon)
        if config.CURRENT_MGRS != new_mgrs:
            config.CURRENT_MGRS = new_mgrs
            if DEBUG:
                print(f"📍 MGRS: {config.CURRENT_MGRS}")
                print(f"   Lat: {lat:.8f}°, Lon: {lon:.8f}°")
            return True
    except Exception as e:
        if DEBUG:
            print("❌ Fehler bei Koordinatenumwandlung:", e)
    return False
