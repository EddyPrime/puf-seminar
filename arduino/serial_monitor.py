import serial
import time

BAUD_RATE = 115200
with open("port.txt") as f:
    SERIAL_PORT = f.read().strip()

sleep_seconds = 1

ser = None
while not ser:
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=None)
    except serial.SerialException:
        print(
            f"Serial port '{SERIAL_PORT}' not available. New attempt in {sleep_seconds} seconds..."
        )
        time.sleep(sleep_seconds)

filename = "data.txt"
f = open(filename, "a")
bytes_to_read = 4

while True:
    try:
        # line = ser.readline().strip()
        line = ser.read(bytes_to_read).strip()
        print(f"[{len(line)}] {line}")
        bin_repr = "".join([bin(byte)[2:].zfill(8) for byte in line])
        print(f"[{len(bin_repr)}] {bin_repr}")
        if len(line) > 0:
            f.write(bin_repr + "\n")
    except serial.SerialException:
        print("Serial port disconnected")
        while True:
            try:
                ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=None)
                print(f"Reconnection completed on serial port '{SERIAL_PORT}'")
                break
            except serial.SerialException:
                print(
                    f"Serial port '{SERIAL_PORT}' not available. New attempt in {sleep_seconds} seconds...",
                    end="\r",
                )
                time.sleep(sleep_seconds)
        continue
    except KeyboardInterrupt:
        f.close()
        ser.close()
        break
