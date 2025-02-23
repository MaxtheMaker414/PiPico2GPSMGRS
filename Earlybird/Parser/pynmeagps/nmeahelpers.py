"""
Hilfsfunktionen für NMEA-Daten in MicroPython
"""

def get_parts(message):
    """
    Zerlegt eine NMEA-Nachricht in ihre Bestandteile.

    :param message: Roh-NMEA-String
    :return: (content, talker, msgID, payload, checksum)
    """
    try:
        content, checksum = message.strip("$\r\n").split("*", 1)
        hdr, payload = content.split(",", 1)
        payload = payload.split(",")
        talker = hdr[:2]
        msgID = hdr[2:]
        return content, talker, msgID, payload, checksum
    except Exception as e:
        raise ValueError(f"Fehler beim Zerlegen der Nachricht: {message}, Fehler: {e}")
