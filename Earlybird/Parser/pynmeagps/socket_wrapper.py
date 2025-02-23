"""
Dummy-Klasse für SocketWrapper, um MicroPython-Kompatibilität zu gewährleisten.
"""

class SocketWrapper:
    """Leere Klasse, da MicroPython kein `socket`-Modul benötigt."""
    def __init__(self, *args, **kwargs):
        pass
