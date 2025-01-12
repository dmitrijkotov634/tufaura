import itertools

from asuslighting.modes.default import RGBColor
from asuslighting.modes.transition import Transition


def transition(colors: list[RGBColor], steps: int = 100):
    return Transition(itertools.cycle(colors), steps)


def make_single_transition(colors: list[RGBColor], steps: int = 100):
    return lambda: Transition(iter(colors), steps)
