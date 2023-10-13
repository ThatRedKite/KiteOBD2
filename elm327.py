import serial


def send_command(port: serial.Serial, command: str, *args):
    try:
        port.write(b"AT" + bytes(command) + bytes(args) + b"\r")

    except serial.SerialException as e:
        raise e


def z(serial: serial.Serial):
    send_command(serial, "z")


def at1(serial: serial.Serial):
    send_command(serial, "@1")

