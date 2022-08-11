from abc import ABCMeta, abstractmethod

from asuslighting.tufaura import ASUSTUFAura


class Mode(metaclass=ABCMeta):
    def get_name(self):
        return self.__class__.__name__

    @abstractmethod
    def enable(self, aura: ASUSTUFAura):
        pass

    def disable(self, aura: ASUSTUFAura):
        pass
