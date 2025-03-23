from pynmeagps.nmeareader import NMEAReader
from pynmeagps.exceptions import NMEAParseError
from mgrs import LLtoMGRS

# Analyse-Zähler
total_sentences = 0
valid_coord_sentences = 0

def parse_nmea_analysis_step(uart):
    global total_sentences, valid_coord_sentences

    if uart.any():
        raw_data = uart.readline()
        if not raw_data:
            return

        try:
            lines = raw_data.decode("utf-8").split("\r\n")
            for line in lines:
                line = line.strip()
                if not line or not line.startswith("$"):
                    continue

                total_sentences += 1

                try:
                    parsed = NMEAReader.parse(line.encode("utf-8"))
                    if parsed:
                        msg_type = parsed.msgID
                        if msg_type == "GGA":
                            lat = parsed.payload[1]
                            lon = parsed.payload[3]
                        elif msg_type == "GLL":
                            lat = parsed.payload[0]
                            lon = parsed.payload[2]
                        else:
                            continue

                        if lat and lon:
                            try:
                                # Versuch MGRS-Umwandlung → zählt als gültig
                                lat_dir = parsed.payload[2] if msg_type == "GGA" else parsed.payload[1]
                                lon_dir = parsed.payload[4] if msg_type == "GGA" else parsed.payload[3]
                                lat_f = float(lat[:2]) + float(lat[2:]) / 60
                                lon_f = float(lon[:3]) + float(lon[3:]) / 60
                                if lat_dir == "S":
                                    lat_f *= -1
                                if lon_dir == "W":
                                    lon_f *= -1
                                mgrs = LLtoMGRS(lat_f, lon_f)
                                valid_coord_sentences += 1
                                print(f"✅ {msg_type} gültig → {mgrs}")
                            except:
                                print(f"⚠️ {msg_type}: Umwandlung fehlgeschlagen")
                except NMEAParseError:
                    pass
        except Exception as e:
            print("❌ Fehler beim Dekodieren:", e)

    if total_sentences > 0 and total_sentences % 10 == 0:
        ratio = 100 * valid_coord_sentences / total_sentences
        print(f"\n📊 Statistik: {valid_coord_sentences}/{total_sentences} gültig ({ratio:.1f}%)\n")
