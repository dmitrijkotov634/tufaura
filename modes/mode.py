from abc import ABCMeta, abstractmethod

from keyboard import KeyboardEvent

from asuslighting.tufaura import ASUSTUFAura


class Mode(metaclass=ABCMeta):
    @abstractmethod
    def enable(self, aura: ASUSTUFAura):
        pass

    def disable(self, aura: ASUSTUFAura):
        pass

    def on_key_event(self, event: KeyboardEvent):
        pass
