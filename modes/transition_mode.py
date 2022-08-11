import itertools
import time
from threading import Thread

from asuslighting import ASUSTUFAura
from asuslighting.modes.mode import Mode
from asuslighting.modes.utils import color_transition


class TransitionLighting(Thread):
    def __init__(self, aura: ASUSTUFAura, colors: tuple[tuple[int, int, int], ...], steps: int):
        super().__init__()

        self.aura = aura
        self.colors = colors
        self.steps = steps

        self.is_stopped = False

    def stop(self):
        self.is_stopped = True

    def run(self):
        last_colors = self.colors[-1]
        for colors in itertools.cycle(self.colors):
            for r, g, b in color_transition(colors, last_colors, self.steps):
                self.aura.set_color(r, g, b)
                time.sleep(0.01)
                if self.is_stopped:
                    return
            last_colors = colors


class TransitionMode(Mode):
    lighting: TransitionLighting

    def __init__(self, colors: tuple[tuple[int, int, int], ...], steps: int = 100):
        self.colors = colors
        self.steps = steps

    def enable(self, aura: ASUSTUFAura):
        self.lighting = TransitionLighting(aura, self.colors, self.steps)
        self.lighting.start()

    def disable(self, aura: ASUSTUFAura):
        self.lighting.stop()
        self.lighting.join()

    def get_name(self):
        return f"Transition: {len(self.colors)} states, {self.steps} steps"
