import socket
import time
from threading import Thread, Event

from asuslighting.tufaura import ASUSTUFAura
from asuslighting.tufaura import TUFSpeed, TUFMode

DEFAULT_PORT = 55663
SCAN_RANGE = range(220, 230)
SCAN_RETRIES = 5
SCAN_SLEEP = 5
RETRY_DELAY = 120


def scan_network(prefix: str, port: int, scan_range=SCAN_RANGE) -> socket.socket | None:
    for device in scan_range:
        ip = f"{prefix}.{device}"
        print(f"Trying {ip}...")
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.3)
            s.connect((ip, port))
            s.send("p".encode())
            s.recv(1)
            print(f"Connected to {ip}")
            return s
        except (TimeoutError, ConnectionRefusedError):
            continue
    return None


def get_local_ip_prefix() -> str:
    local_ip = socket.gethostbyname(socket.gethostname())
    ip_parts = local_ip.split(".")
    return ".".join(ip_parts[:3])


class AuraAgent(Thread, ASUSTUFAura):
    def __init__(self, aura: ASUSTUFAura):
        super().__init__()
        self.aura = aura

        self.red = 255
        self.green = 255
        self.blue = 255

        self.stop_event = Event()
        self.stop_event.clear()

    def set_color(self, red=255, green=255, blue=255,
                  mode=TUFMode.STATIC, speed=TUFSpeed.LOW):
        self.aura.set_color(red, green, blue, mode, speed)
        if mode == TUFMode.STATIC:
            self.red, self.green, self.blue = red, green, blue
        else:
            self.red, self.green, self.blue = 255, 255, 255

    def run(self):
        while not self.stop_event.is_set():
            sock = None
            prefix = get_local_ip_prefix()

            for _ in range(SCAN_RETRIES):
                sock = scan_network(prefix, DEFAULT_PORT)
                if sock:
                    break
                time.sleep(SCAN_SLEEP)

            if not sock:
                print("No devices found. Retrying after delay.")
                time.sleep(RETRY_DELAY)
                continue

            try:
                sock.settimeout(5)
                sock.send("p".encode())
                sock.recv(1)
                while not self.stop_event.is_set():
                    color = ((self.red & 0xFF) << 16) | ((self.green & 0xFF) << 8) | (self.blue & 0xFF)
                    if not sock or sock.fileno() == -1:
                        print("Socket is invalid. Breaking loop for reconnect.")
                        break
                    sock.send(f"s{color};".encode())
                    sock.recv(1)
                    time.sleep(0.01)
            except Exception as e:
                print(f"Connection error: {e}. Reconnecting...")
            finally:
                if sock:
                    sock.close()
                time.sleep(10)

    def stop(self):
        self.stop_event.set()
