"""
NMEAReader für MicroPython – Liest GPS-Daten von UART.
"""

import machine
import utime
from pynmeagps.nmeamessage import NMEAMessage
from pynmeagps.exceptions import NMEAParseError

class NMEAReader:
    """
    NMEAReader liest und verarbeitet NMEA-Daten von einer seriellen Schnittstelle.
    """

    def __init__(self, uart):
        """
        Initialisiert den NMEAReader.
        
        :param uart: UART-Objekt von machine.UART
        """
        self._uart = uart

    def read(self):
        """
        Liest eine Zeile aus der UART-Schnittstelle und parst sie als NMEA-Nachricht.

        :return: (rohe Daten, NMEAMessage-Objekt)
        """
        raw_data = self._read_uart_line()
        if raw_data:
            parsed_data = self.parse(raw_data)
            return raw_data, parsed_data
        return None, None

    def _read_uart_line(self):
        """Liest eine NMEA-Zeile von der UART-Schnittstelle."""
        line = b""
        while True:
            char = self._uart.read(1)  # Lese 1 Byte
            if char:
                line += char
                if char == b"\n":  # Endet Zeile mit LF?
                    break
            else:
                utime.sleep(0.01)  # Warte auf neue Daten
        return line

    @staticmethod
    def parse(message):
        """
        Parsed eine NMEA-Byte-Zeile in eine NMEAMessage.

        :param message: NMEA-Nachricht als Bytes
        :return: NMEAMessage-Objekt
        :raises: NMEAParseError bei ungültigen Daten
        """
        try:
            return NMEAMessage.from_string(message.decode("utf-8"))
        except Exception as e:
            raise NMEAParseError(f"Fehler beim Parsen der Nachricht: {e}")

