import time
from threading import Thread

import pyautogui
from PIL import Image
from mss import mss

from asuslighting.modes.mode import Mode
from asuslighting.modes.utils import color_transition
from asuslighting.tufaura import ASUSTUFAura


def get_color(image, palette_size=16):
    paletted = image.convert('P', palette=Image.ADAPTIVE, colors=palette_size)

    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)

    additions = (0, 0, 0)

    for color in color_counts:
        palette_index = color[1]
        dominant_color = palette[palette_index * 3:palette_index * 3 + 3]

        addition = 255 - max(dominant_color)
        additions = [i + addition for i in dominant_color]

        if sum(additions) < 625:
            return additions

    return additions


class AdaptiveLighting(Thread):
    def __init__(self, aura: ASUSTUFAura):
        super().__init__()

        self.aura = aura
        self.is_stopped = False

    def stop(self):
        self.is_stopped = True

    def run(self):
        with mss() as sct:
            last_colors = [255, 255, 255]

            while True:
                sct_img = sct.grab(sct.monitors[1])

                img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

                colors = get_color(img)
                for r, g, b in color_transition(colors, last_colors):
                    self.aura.set_color(r, g, b)
                    time.sleep(0.01)

                last_colors = colors

                if self.is_stopped:
                    break


class AdaptiveMouseLighting(Thread):
    def __init__(self, aura: ASUSTUFAura):
        super().__init__()

        self.aura = aura
        self.is_stopped = False

    def stop(self):
        self.is_stopped = True

    def run(self):
        with mss() as sct:
            last_colors = [255, 255, 255]

            while True:
                sct_img = sct.grab(sct.monitors[1])

                img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

                colors = img.getpixel(pyautogui.position())

                addition = 255 - max(colors)
                colors = [i + addition for i in colors]

                for r, g, b in color_transition(colors, last_colors):
                    self.aura.set_color(r, g, b)
                    time.sleep(0.01)

                last_colors = colors

                if self.is_stopped:
                    break


class AdaptiveMode(Mode):
    lighting: AdaptiveLighting

    def enable(self, aura: ASUSTUFAura):
        self.lighting = AdaptiveLighting(aura)
        self.lighting.start()

    def disable(self, aura: ASUSTUFAura):
        self.lighting.stop()
        self.lighting.join()


class AdaptiveMouseMode(Mode):
    lighting: AdaptiveMouseLighting

    def enable(self, aura: ASUSTUFAura):
        self.lighting = AdaptiveMouseLighting(aura)
        self.lighting.start()

    def disable(self, aura: ASUSTUFAura):
        self.lighting.stop()
        self.lighting.join()
