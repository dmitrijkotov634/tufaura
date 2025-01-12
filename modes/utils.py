from typing import Iterator

from asuslighting.modes.default import RGBColor


def color_transition(old_colors: RGBColor, new_colors: RGBColor, steps: int = 15) -> Iterator[RGBColor]:
    for step in range(steps):
        yield (int(last_color + ((color - last_color) * step / steps)) for color, last_color in
               zip(old_colors, new_colors))
