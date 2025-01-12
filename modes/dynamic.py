import time

import pyautogui
from PIL import Image
from mss import mss

from asuslighting.modes.transition import Transition

mss = mss()


def get_monitor_for_cursor():
    cursor_x, cursor_y = pyautogui.position()

    for monitor in mss.monitors:
        if (monitor["left"] <= cursor_x < monitor["left"] + monitor["width"] and monitor["top"] <= cursor_y < monitor[
            "top"] + monitor["height"]):
            return monitor

    return None


def process_dominant_color(image: Image, _):
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


def process_mouse_position_color(image, mouse_pos):
    colors = image.getpixel(mouse_pos)
    addition = 255 - max(colors)
    return [i + addition for i in colors]


def dynamic(processor):
    with mss as sct:
        while True:
            monitor = get_monitor_for_cursor()

            if not monitor:
                print("Cursor is outside of available monitors.")
                time.sleep(0.1)
                continue

            mouse_pos = pyautogui.position()
            mouse_pos_relative = (
                mouse_pos[0] - monitor["left"],
                mouse_pos[1] - monitor["top"],
            )

            sct_img = sct.grab(monitor)
            image = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

            yield processor(image, mouse_pos_relative)
            time.sleep(0.05)


def dynamic_dominant_mode():
    return Transition(dynamic(process_dominant_color))


def dynamic_mouse_position_mode():
    return Transition(dynamic(process_mouse_position_color))
