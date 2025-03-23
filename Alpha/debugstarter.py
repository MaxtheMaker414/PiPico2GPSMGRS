import machine
import debug  # dieser Script hier
import utime

uart1 = machine.UART(1, baudrate=115200, tx=machine.Pin(4), rx=machine.Pin(5))

while True:
    debug.parse_nmea_analysis_step(uart1)
    utime.sleep_ms(100)
