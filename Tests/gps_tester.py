"""
Author: Nathan Rogers
Date: 2020
"""

from serial import Serial, SerialException
from serial.tools import list_ports
from serial.tools.list_ports_common import ListPortInfo
import time
import adafruit_gps

cont = True

uart = Serial("COM3", baudrate=9600, timeout=10)

print("uart.name:", uart.name)
print("type:", type(uart))
print("uart:", uart)
x = list_ports.comports()
for port in x:
    print("port:", port)
    print("port.name:", port.name)
    print("port.pid:", port.pid)
    print("port.vid:", port.vid)


gps = adafruit_gps.GPS(uart, debug=False)

# turn on basic GGA and RMC info
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

# set update rate to 1hz
gps.send_command(b"PMTK220,1000")

last_print = time.monotonic()
while cont:
    gps.update()
    current = time.monotonic()
    if current - last_print >= 1.0:
        last_print = current
        if not gps.has_fix:
            print("waiting for fix...")
            continue
        print("=" * 150)
        print(gps.nmea_sentence)
        print(
            "Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}".format(
                gps.timestamp_utc.tm_mon,
                gps.timestamp_utc.tm_mday,
                gps.timestamp_utc.tm_year,
                gps.timestamp_utc.tm_hour,
                gps.timestamp_utc.tm_min,
                gps.timestamp_utc.tm_sec,
            )
        )
        print("Latitude: {0:.6f} degrees".format(gps.latitude))
        print("Longitude: {0:.6f} degrees".format(gps.longitude))
        print("Fix quality: {}".format(gps.fix_quality))

        if gps.satellites is not None:
            print("# satellites: {}".format(gps.satellites))
        if gps.altitude_m is not None:
            print("Altitude: {} meters".format(gps.altitude_m))
        if gps.speed_knots is not None:
            print("Speed: {} knots".format(gps.speed_knots))
        if gps.track_angle_deg is not None:
            print("Track angle: {} degrees".format(gps.track_angle_deg))
        if gps.horizontal_dilution is not None:
            print("Horizontal dilution: {}".format(gps.horizontal_dilution))
        if gps.height_geoid is not None:
            print("Height geo ID: {} meters".format(gps.height_geoid))
        ans = str(input("continue? (y or n): "))
        if ans == "y":
            cont = True
        if ans == "n":
            cont = False
