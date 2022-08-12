import time
from threading import Thread
from typing import Tuple, Iterator

from asuslighting import ASUSTUFAura
from asuslighting.modes.mode import Mode
from asuslighting.modes.utils import color_transition


class Worker(Thread):
    def __init__(self, aura: ASUSTUFAura, iterator: Iterator[Tuple[int, int, int]], steps: int):
        super().__init__()

        self.aura = aura
        self.iterator = iterator
        self.steps = steps
        self.stopped = False

    def stop(self):
        self.stopped = True

    def run(self):
        last_colors = next(self.iterator)
        for colors in self.iterator:
            for r, g, b in color_transition(colors, last_colors, self.steps):
                self.aura.set_color(r, g, b)
                time.sleep(0.01)
                if self.stopped:
                    return
            last_colors = colors


class Transition(Mode):
    lighting: Worker

    def __init__(self, iterator: Iterator[Tuple[int, int, int]], steps: int = 15):
        self.iterator = iterator
        self.steps = steps

    def enable(self, aura: ASUSTUFAura):
        self.lighting = Worker(aura, self.iterator, self.steps)
        self.lighting.start()

    def disable(self, aura: ASUSTUFAura):
        self.lighting.stop()
        self.lighting.join()
