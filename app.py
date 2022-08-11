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


def main():
    aura = ASUSTUFAura()

    controller = Controller(aura, config.modes, config.modes[0])

    def change(func):
        def wrapped():
            toaster.show_toast("ASUS Lighting",
                               func().get_name(),
                               duration=1,
                               threaded=True)

        return wrapped

    keyboard.add_hotkey('right ctrl+left', change(controller.next))
    keyboard.add_hotkey('right ctrl+right', change(controller.prev))

    keyboard.wait()
