from ctypes import cdll
from enum import Enum


class TUFMode(Enum):
    DIRECT = 4
    STATIC = 0
    BREATHING = 1
    COLOR_CYCLE = 2
    STROBE = 10


class TUFSpeed(Enum):
    LOW = 0xE1
    MEDIUM = 0xEB
    HIGH = 0xF5


class ASUSTUFAura:
    def __init__(self, dll_path: str = "ACPIWMI.dll"):
        self.dll = cdll.LoadLibrary(dll_path)
        self.dll.AsWMI_Open()

    def set_color(self,
                  red: int = 255,
                  green: int = 255,
                  blue: int = 255,
                  mode: TUFMode = TUFMode.STATIC,
                  speed: TUFSpeed = TUFSpeed.LOW):
        # print("r =", red, "g =", green, "b =", blue, "mode =", mode.name, "speed =", speed.name)
        high = ((mode.value | ((red | (green << 8)) << 8)) << 8) | 0xB3
        low = blue | (speed.value << 8)
        self.dll.AsWMI_NB_DeviceControl_2arg(0x100056, high, low)
