from collections import deque

from asuslighting.modes.mode import Mode
from asuslighting.tufaura import ASUSTUFAura


class Controller:
    def __init__(self, aura: ASUSTUFAura, modes: tuple[Mode, ...], current_mode: Mode):
        self.aura = aura

        self.modes = deque(modes)

        self.current_mode = current_mode
        self.current_mode.enable(self.aura)

    def change_mode(self, mode: Mode):
        print("Disable", type(self.current_mode).__name__,
              "Enable", type(mode).__name__)

        self.current_mode.disable(self.aura)
        mode.enable(self.aura)
        self.current_mode = mode

    def next(self):
        self.modes.rotate(1)
        self.change_mode(self.modes[0])
        return self.current_mode

    def prev(self):
        self.modes.rotate(-1)
        self.change_mode(self.modes[0])
        return self.current_mode
