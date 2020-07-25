from serial import Serial
from serial.serialutil import SerialException
from serial.tools.list_ports import comports
from serial.tools.list_ports_common import ListPortInfo
from time import sleep


""" A basic serial scanner working in the same way as rs_device_com_scanner.py for testing purposes. """


known_ports = list()


def scan_ports() -> None:
    while True:
        ports = comports()
        print("Plugged in COMs")
        for port in ports:
            print(port, port.pid, port.vid)
        print()
        if len(ports) > len(known_ports):
            check_for_new_devices(ports)
        elif len(ports) < len(known_ports):
            check_for_disconnects(ports)
        sleep(1)


def check_for_new_devices(ports: [ListPortInfo]) -> None:
    for port in ports:
        if port not in known_ports:
            known_ports.append(port)
            print("Found port:", port, "Trying to connect...")
            ret_val, connection = try_open_port(port)
            if ret_val:
                print("Connected to port:", port, "Connection is:", connection)
            else:
                print("Failed to connect to port:", port)
            print()


def check_for_disconnects(ports: [ListPortInfo]) -> None:
    for known_port in known_ports:
        if known_port not in ports:
            known_ports.remove(known_port)
            print("Lost one:", known_port, "\n")


def try_open_port(port) -> (bool, Serial):
    new_connection = Serial()
    new_connection.port = port.device
    i = 0
    while not new_connection.is_open and i < 5:  # Make multiple attempts in case device is busy
        i += 1
        try:
            new_connection.open()
        except SerialException as e:
            sleep(1)
    if not new_connection.is_open:  # Failed to connect
        return False, None
    return True, new_connection


def main():
    scan_ports()


if __name__ == '__main__':
    main()
