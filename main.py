#!/usr/bin/env python3

import itertools
import math
import time

import bpgfx


def main() -> None:
    canvas = bpgfx.Canvas((5, 5))
    canvas.set_dot((0, 0), True)
    canvas.set_dot((1, 1), True)
    canvas.set_dot((2, 2), True)
    canvas.set_dot((3, 3), True)
    canvas.set_dot((4, 4), True)
    print(canvas)
    print(repr(canvas))
    time.sleep(2)

    # 640x480 dots
    # v
    # scale down by 4x
    # v
    # 160x120 dots
    # v
    # with 2x4 dots per monospace character
    # v
    # 80x30 characters total
    canvas = bpgfx.Canvas((160, 120))

    for i in itertools.count(start=1):
        canvas.clear()
        # Draw boarder box.
        for x in range(canvas.width):
            canvas.set_dot((x, 0), True)
            canvas.set_dot((x, canvas.height - 1), True)
        for y in range(canvas.height):
            canvas.set_dot((0, y), True)
            canvas.set_dot((canvas.width - 1, y), True)
        # Draw sin wave.
        for x in range(canvas.width):
            canvas.set_dot((x, canvas.height // 2), True)
            degrees = (x + i) * 2
            radians = math.radians(degrees)
            scale = (canvas.height * 0.75) / 2
            y = int(canvas.height / 2 - math.sin(radians) * scale)
            canvas.set_dot((x, y), True)

        TERM_CLEAR = f"\N{ESCAPE}[H\N{ESCAPE}[2J"  # HOME; CLEAR SCREEN
        print(f"{TERM_CLEAR}{canvas}", end="")
        time.sleep(1 / 30)


if __name__ == "__main__":
    main()
