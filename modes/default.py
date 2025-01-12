from asuslighting.modes.mode import Mode
from asuslighting.tufaura import ASUSTUFAura, TUFMode, TUFSpeed

RGBColor = tuple[int, int, int]


class DefaultMode(Mode):
    mode: TUFMode

    def __init__(self, mode: TUFMode, color: RGBColor = (0, 0, 0), speed: TUFSpeed = TUFSpeed.LOW):
        self.mode = mode
        self.color = color
        self.speed = speed

    def enable(self, aura: ASUSTUFAura):
        aura.set_color(self.color[0], self.color[1], self.color[2], speed=self.speed, mode=self.mode)
