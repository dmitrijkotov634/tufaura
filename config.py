from asuslighting.modes.custom import transition, make_single_transition
from asuslighting.modes.default import DefaultMode, RGBColor
from asuslighting.modes.dynamic import dynamic_dominant_mode, dynamic_mouse_position_mode
from asuslighting.modes.mode import Mode
from asuslighting.modes.ripple import RippleSwitch
from asuslighting.tufaura import TUFSpeed, TUFMode

COLOR: RGBColor = (255, 0, 0)
SPEED: TUFSpeed = TUFSpeed.MEDIUM

"""
WARNING!!! Set to False if you do not have a custom-built device on port 55663 that accepts colors for synchronization with the keyboard.
"""
ENABLE_CUSTOM_RGB_DEVICE_SYNC = True  # Set to False if not applicable

modes: list[tuple[str, Mode]] = [
    ("Breathing", DefaultMode(mode=TUFMode.BREATHING, color=COLOR, speed=SPEED)),
    ("Strobe", DefaultMode(mode=TUFMode.STROBE, color=COLOR, speed=SPEED)),
    ("Static", DefaultMode(mode=TUFMode.STATIC, color=COLOR)),
    ("Color cycle", DefaultMode(mode=TUFMode.COLOR_CYCLE, speed=SPEED)),

    ("Colors 1", transition(
        colors=[
            (250, 68, 140),
            (254, 200, 89),
            (67, 181, 160),
            (73, 29, 136),
        ]
    )),

    ("Colors 2", transition(
        colors=[
            (103, 197, 10),
            (255, 217, 0),
            (124, 215, 194),
            (5, 78, 111),
        ]
    )),

    ("Colors 3", transition(
        colors=[
            (255, 163, 0),
            (207, 0, 96),
            (255, 0, 255),
            (19, 168, 254),
        ]
    )),

    ("Colors 4", transition(
        colors=[
            (33, 137, 126),
            (59, 169, 156),
            (105, 209, 197),
            (126, 188, 230),
            (137, 128, 245)
        ],
        steps=90
    )),

    ("Dynamic (dominant)", dynamic_dominant_mode()),
    ("Dynamic (mouse position)", dynamic_mouse_position_mode()),

    ("Ripple", RippleSwitch(
        key_up=make_single_transition(
            colors=[
                (189, 122, 252),
                (81, 57, 102)
            ],
            steps=5
        ),
        key_down=make_single_transition(
            colors=[
                (81, 57, 102),
                (189, 122, 252)
            ],
            steps=7
        )
    ))
]
