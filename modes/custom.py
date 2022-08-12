import itertools

from asuslighting.modes.transition import Transition


def transition(colors: list[tuple[int, int, int]], steps: int = 100):
    return Transition(itertools.cycle(colors), steps)
