import os
import sys

import keyboard

from asuslighting import config
from asuslighting.controller import Controller
from asuslighting.tufaura import ASUSTUFAura

sys.path.append(os.getcwd() + r"\Lib\site-packages\win32\lib")
sys.path.append(os.getcwd() + r"\Lib\site-packages\win32")

from win10toast import ToastNotifier

toaster = ToastNotifier()


def restore():
    try:
        with open("mode.txt", "r") as r:
            return int(r.read())
    except FileNotFoundError:
        return 0


def save(mode):
    with open("mode.txt", "w") as w:
        w.write(str(config.modes.index(mode)))


def main():
    aura = ASUSTUFAura()

    controller = Controller(aura, config.modes, config.modes[restore()][1])

    def change(func):
        def wrapped():
            mode = func()
            save(mode)
            toaster.show_toast("ASUS Lighting",
                               mode[0],
                               duration=1,
                               threaded=True)

        return wrapped

    keyboard.add_hotkey('right ctrl+left', change(controller.next))
    keyboard.add_hotkey('right ctrl+right', change(controller.prev))

    while True:
        controller.on_key_event(keyboard.read_event())
