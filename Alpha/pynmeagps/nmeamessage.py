"""
NMEA Nachrichtendekodierung für MicroPython
"""

from pynmeagps.nmeahelpers import get_parts

class NMEAMessage:
    """Verarbeitet und speichert eine NMEA-Nachricht."""

    def __init__(self, talker, msgID, payload):
        """Initialisiert die NMEA-Nachricht."""
        self.talker = talker
        self.msgID = msgID
        self.payload = payload

    @classmethod
    def from_string(cls, message):
        """
        Erstellt eine NMEAMessage aus einer Roh-NMEA-Zeile.

        :param message: NMEA-Nachricht als String
        :return: NMEAMessage-Objekt
        """
        try:
            content, talker, msgID, payload, checksum = get_parts(message)
            return cls(talker, msgID, payload)
        except Exception as e:
            raise ValueError(f"Ungültige NMEA-Zeile: {message} – Fehler: {e}")

    def __str__(self):
        """Gibt eine lesbare Form der NMEA-Nachricht zurück."""
        return f"<NMEAMessage {self.talker}{self.msgID}: {self.payload}>"
