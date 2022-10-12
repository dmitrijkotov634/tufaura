import typing

import keyboard

from asuslighting import ASUSTUFAura
from asuslighting.modes.mode import Mode


class Ripple(Mode):
    aura: ASUSTUFAura

    key_up: Mode
    key_down: Mode

    def __init__(self, key_down: typing.Callable, key_up: typing.Callable):
        self.factory_key_down = key_down
        self.factory_key_up = key_up
        self.current_event = keyboard.KEY_UP

    def enable(self, aura: ASUSTUFAura):
        self.aura = aura
        self.key_up = self.factory_key_up()
        self.key_up.enable(self.aura)

    def disable(self, aura: ASUSTUFAura):
        if self.current_event == keyboard.KEY_DOWN:
            self.key_down.disable(aura)
        else:
            self.key_up.disable(aura)

    def on_key_event(self, event: keyboard.KeyboardEvent):
        if event.event_type == self.current_event:
            return

        if event.event_type == keyboard.KEY_DOWN:
            self.key_up.disable(self.aura)
            self.key_down = self.factory_key_down()
            self.key_down.enable(self.aura)
        else:
            self.key_down.disable(self.aura)
            self.key_up = self.factory_key_up()
            self.key_up.enable(self.aura)

        self.current_event = event.event_type
