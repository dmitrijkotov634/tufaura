import json
from contextlib import suppress
from typing import Any

import keyboard
from win10toast import ToastNotifier

from asuslighting import config
from asuslighting.controller import Controller
from asuslighting.private.agent import AuraAgent
from asuslighting.tufaura import ASUSTUFAura

toaster = ToastNotifier()


class JSONConfig:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._data = {}

        try:
            with open(self.file_path, "r") as file:
                self._data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self._data = {}

    def save(self):
        with open(self.file_path, "w") as file:
            json.dump(self._data, file, indent=4)

    def __getitem__(self, key: str) -> Any:
        return self._data.get(key)

    def __setitem__(self, key: str, value: Any):
        self._data[key] = value
        self.save()

    def __delitem__(self, key: str):
        if key in self._data:
            del self._data[key]
            self.save()

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def as_dict(self):
        return self._data


latest_state = JSONConfig("state.json")


def main():
    aura = AuraAgent(ASUSTUFAura())

    if config.ENABLE_CUSTOM_RGB_DEVICE_SYNC:
        aura.start()

    if latest_state["modes_count"] != len(config.modes):
        latest_state["modes_count"] = len(config.modes)
        latest_state["current_mode"] = 0
        latest_state.save()

    mode_index = latest_state["current_mode"] or 0

    controller = Controller(aura, config.modes, config.modes[mode_index][1])

    def change(func):
        def wrapped():
            mode = func()

            latest_state["current_mode"] = config.modes.index(mode)
            latest_state.save()

            toaster.show_toast("ASUS Lighting",
                               mode[0],
                               duration=0.1,
                               threaded=True)

        return wrapped

    keyboard.add_hotkey('right ctrl+left', change(controller.next))
    keyboard.add_hotkey('right ctrl+right', change(controller.prev))

    try:
        with suppress(Exception):
            while True:
                controller.on_key_event(keyboard.read_event())
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        controller.stop()
        aura.stop()
