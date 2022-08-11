from asuslighting import config
from asuslighting.modes.mode import Mode
from asuslighting.tufaura import ASUSTUFAura, TUFMode


class StandardMode(Mode):
    mode: TUFMode

    def enable(self, aura: ASUSTUFAura):
        aura.set_color(config.COLOR[0], config.COLOR[1], config.COLOR[2], speed=config.SPEED, mode=self.mode)


class Strobe(StandardMode):
    mode = TUFMode.STROBE


class Breathing(StandardMode):
    mode = TUFMode.BREATHING


class ColorCycle(StandardMode):
    mode = TUFMode.COLOR_CYCLE


class Static(StandardMode):
    mode = TUFMode.STATIC
