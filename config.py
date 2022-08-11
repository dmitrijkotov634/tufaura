from asuslighting.modes.adaptive_mode import AdaptiveMode, AdaptiveMouseMode
from asuslighting.modes.standard_modes import Breathing, Strobe, Static, ColorCycle
from asuslighting.modes.transition_mode import TransitionMode
from asuslighting.tufaura import TUFSpeed

modes = (
    Breathing(),
    Strobe(),
    Static(),
    ColorCycle(),

    TransitionMode(
        (
            (250, 68, 140),
            (254, 200, 89),
            (67, 181, 160),
            (73, 29, 136),
        )
    ),

    TransitionMode(
        (
            (103, 197, 10),
            (255, 217, 0),
            (124, 215, 194),
            (5, 78, 111),
        )
    ),

    TransitionMode(
        (
            (255, 163, 0),
            (207, 0, 96),
            (255, 0, 255),
            (19, 168, 254),
        )
    ),

    TransitionMode(
        (
            (78, 135, 164),
            (176, 213, 206),
            (255, 241, 228),
            (250, 134, 171),
            (238, 40, 137)
        )
    ),
    AdaptiveMouseMode(),
    AdaptiveMode(),
)

COLOR = (204, 41, 95)
SPEED = TUFSpeed.MEDIUM
