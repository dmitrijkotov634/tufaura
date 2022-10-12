from collections import deque

from keyboard import KeyboardEvent

from asuslighting.modes.mode import Mode
from asuslighting.tufaura import ASUSTUFAura


class Controller:
    def __init__(self, aura: ASUSTUFAura, modes: dict, current_mode: Mode):
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
        self.change_mode(self.modes[0][1])
        return self.modes[0]

    def prev(self):
        self.modes.rotate(-1)
        self.change_mode(self.modes[0][1])
        return self.modes[0]

    def on_key_event(self, event: KeyboardEvent):
        self.current_mode.on_key_event(event)
