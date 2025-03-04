import socket
import struct
from salsa20 import Salsa20_xor
import time

PS5_IP = "192.168.100.27"
SendPort = 33739
ReceivePort = 33740
PC_IP = "192.168.100.3"

def salsa20_dec(dat):
    KEY = b'Simulator Interface Packet GT7 ver 0.0'
    oiv = dat[0x40:0x44]
    iv1 = int.from_bytes(oiv, byteorder='little')
    iv2 = iv1 ^ 0xDEADBEAF
    IV = bytearray()
    IV.extend(iv2.to_bytes(4, 'little'))
    IV.extend(iv1.to_bytes(4, 'little'))
    ddata = Salsa20_xor(dat, bytes(IV), KEY[0:32])
    magic = int.from_bytes(ddata[0:4], byteorder='little')
    return ddata if magic == 0x47375330 else bytearray(b'')

def send_hb(s):
    s.sendto(b'A', (PS5_IP, SendPort))

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Socket created")
    s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
    try:
        s.bind((PC_IP, ReceivePort))
        print(f"Bound to {PC_IP}:{ReceivePort}")
    except OSError as e:
        print(f"Bind failed: {e}")
        return
    s.setblocking(False)
    print(f"Listening for GT7 telemetry from {PS5_IP}...")
    last_hb = time.time()
    last_display = time.time()
    packet_count = 0
    latest_data = None

    try:
        while True:
            now = time.time()
            if now - last_hb >= 0.005:  # Heartbeat every 5ms
                send_hb(s)
                last_hb = now
            try:
                data, addr = s.recvfrom(4096)
                packet_count += 1
                ddata = salsa20_dec(data)
                if len(ddata) > 0:
                    pktid = struct.unpack('i', ddata[0x70:0x70+4])[0]
                    speed = struct.unpack('f', ddata[0x4C:0x4C+4])[0] * 3.6
                    gear = struct.unpack('B', ddata[0x90:0x90+1])[0] & 0b00001111
                    gear = 'R' if gear < 1 else str(gear)
                    rpm = struct.unpack('f', ddata[0x3C:0x3C+4])[0]
                    latest_data = f"Packet #{packet_count} | ID: {pktid} | Speed: {speed:.1f} kph | Gear: {gear} | RPM: {rpm:.0f}"
            except BlockingIOError:
                pass
            if latest_data and now - last_display >= 0.5:  # Display every 0.5s
                print(latest_data)
                last_display = now
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        s.close()

if __name__ == "__main__":
    main()