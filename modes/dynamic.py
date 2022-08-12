import pyautogui
from PIL import Image
from mss import mss

from asuslighting.modes.transition import Transition

mss = mss()


def processor_dominant_color(image: Image):
    paletted = image.convert('P', palette=Image.ADAPTIVE, colors=16)

    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)

    additions = (0, 0, 0)

    for color in color_counts:
        palette_index = color[1]
        dominant_color = palette[palette_index * 3:palette_index * 3 + 3]

        addition = 255 - max(dominant_color)
        additions = tuple(i + addition for i in dominant_color)

        if sum(additions) < 625:
            return additions

    return additions


def processor_mouse_position_color(image: Image):
    colors = image.getpixel(pyautogui.position())

    addition = 255 - max(colors)
    return [i + addition for i in colors]


def dynamic(processor):
    while True:
        sct_img = mss.grab(mss.monitors[1])
        image = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        yield processor(image)


def dynamic_dominant_mode():
    return Transition(dynamic(processor_dominant_color))


def dynamic_mouse_position_mode():
    return Transition(dynamic(processor_mouse_position_color))
