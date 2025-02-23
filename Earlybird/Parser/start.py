import machine
import utime
from pynmeagps.nmeareader import NMEAReader
from pynmeagps.exceptions import NMEAParseError

# UART Initialisierung für RS485
uart1 = machine.UART(1, baudrate=115200, tx=machine.Pin(4), rx=machine.Pin(5))

def read_nmea():
    """Liest und parst NMEA-Daten von der GPS-UART-Schnittstelle."""
    reader = NMEAReader(uart1)

    while True:
        try:
            raw_data, parsed_data = reader.read()
            if parsed_data:
                print("Empfangene NMEA-Nachricht:", parsed_data)
                
                # GGA-Nachricht auswerten
                if parsed_data.msgID == "GGA":
                    print(f"Zeit: {parsed_data.time}")
                    print(f"Breitengrad: {parsed_data.lat} {parsed_data.NS}")
                    print(f"Längengrad: {parsed_data.lon} {parsed_data.EW}")
                    print(f"Höhe: {parsed_data.alt} {parsed_data.altUnit}")
                    print(f"Anzahl Satelliten: {parsed_data.numSV}")
                    print(f"HDOP: {parsed_data.HDOP}")
            
            utime.sleep(1)  # Wartezeit für neue Daten
        except NMEAParseError as e:
            print("Fehler beim Parsen der NMEA-Daten:", e)
        except KeyboardInterrupt:
            print("Beende GPS-Reader.")
            break

if __name__ == "__main__":
    read_nmea()
