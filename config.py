from asuslighting.modes.custom import transition
from asuslighting.modes.default import DefaultMode
from asuslighting.modes.dynamic import dynamic_dominant_mode, dynamic_mouse_position_mode
from asuslighting.modes.ripple import Ripple
from asuslighting.modes.transition import Transition
from asuslighting.tufaura import TUFSpeed, TUFMode

COLOR = (204, 41, 95)
SPEED = TUFSpeed.MEDIUM

modes = [
    ("Breathing", DefaultMode(TUFMode.BREATHING, COLOR, SPEED)),
    ("Strobe", DefaultMode(TUFMode.STROBE, COLOR, SPEED)),
    ("Static", DefaultMode(TUFMode.STATIC, COLOR)),
    ("Color cycle", DefaultMode(TUFMode.COLOR_CYCLE, speed=SPEED)),

    ("Colors 1", transition(
        [
            (250, 68, 140),
            (254, 200, 89),
            (67, 181, 160),
            (73, 29, 136),
        ]
    )),

    ("Colors 2", transition(
        [
            (103, 197, 10),
            (255, 217, 0),
            (124, 215, 194),
            (5, 78, 111),
        ]
    )),

    ("Colors 3", transition(
        [
            (255, 163, 0),
            (207, 0, 96),
            (255, 0, 255),
            (19, 168, 254),
        ]
    )),

    ("Colors 4", transition(
        [
            (78, 135, 164),
            (176, 213, 206),
            (255, 241, 228),
            (250, 134, 171),
            (238, 40, 137)
        ]
    )),

    ("Dynamic (dominant)", dynamic_dominant_mode()),
    ("Dynamic (mouse position)", dynamic_mouse_position_mode()),

    ("Ripple", Ripple(
        key_up=lambda: DefaultMode(
            TUFMode.STATIC,
            (90, 90, 0)
        ),
        key_down=lambda: Transition(
            iter([
                (90, 90, 0),
                (255, 255, 0)
            ]),
            steps=10
        )
    ))
]
