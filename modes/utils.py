def color_transition(old_colors, new_colors, steps=15):
    for step in range(steps):
        yield (int(last_color + ((color - last_color) * step / steps)) for color, last_color in
               zip(old_colors, new_colors))
