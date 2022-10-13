import typing

import keyboard

from asuslighting import ASUSTUFAura
from asuslighting.modes.mode import Mode


class RippleSwitch(Mode):
    aura: ASUSTUFAura

    key_up: Mode
    key_down: Mode

    last_state: bool
    keyboard_state: set

    def __init__(self, key_down: typing.Callable, key_up: typing.Callable):
        self.factory_key_down = key_down
        self.factory_key_up = key_up

    def enable(self, aura: ASUSTUFAura):
        self.aura = aura
        self.key_down = self.factory_key_down()
        self.key_down.enable(self.aura)

        self.keyboard_state = set()
        self.last_state = True

    def disable(self, aura: ASUSTUFAura):
        if self.last_state:
            self.key_down.disable(aura)
        else:
            self.key_up.disable(aura)

    def on_key_event(self, event: keyboard.KeyboardEvent):
        if event.event_type == keyboard.KEY_DOWN:
            self.keyboard_state.add(event.scan_code)

        if event.event_type == keyboard.KEY_UP and event.scan_code in self.keyboard_state:
            self.keyboard_state.remove(event.scan_code)

        current = len(self.keyboard_state) > 0

        if self.last_state == current:
            return

        self.last_state = current

        if self.last_state:
            self.key_up.disable(self.aura)
            self.key_down = self.factory_key_down()
            self.key_down.enable(self.aura)
        else:
            self.key_down.disable(self.aura)
            self.key_up = self.factory_key_up()
            self.key_up.enable(self.aura)
