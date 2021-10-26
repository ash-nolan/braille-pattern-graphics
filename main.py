#!/usr/bin/env python3

import itertools
import math
import time

import bpgfx


def main() -> None:
    # 640x480 dots
    # v
    # scale down by 4x
    # v
    # 160x120 dots
    # v
    # with 2x4 dots per monospace character
    # v
    # 80x30 characters total
    canvas = bpgfx.Canvas(160, 120)

    for i in itertools.count(start=1):
        canvas.clear()

        # Draw boarder box.
        upper = bpgfx.Line(bpgfx.Point(0, 0), bpgfx.Point(canvas.width - 1, 0))
        lower = bpgfx.Line(
            bpgfx.Point(0, canvas.height - 1),
            bpgfx.Point(canvas.width - 1, canvas.height - 1),
        )
        lhs = bpgfx.Line(bpgfx.Point(0, 0), bpgfx.Point(0, canvas.height - 1))
        rhs = bpgfx.Line(
            bpgfx.Point(canvas.width - 1, 0),
            bpgfx.Point(canvas.width - 1, canvas.height - 1),
        )
        canvas.draw(upper)
        canvas.draw(lower)
        canvas.draw(lhs)
        canvas.draw(rhs)

        # Draw the sine wave.
        for x in range(canvas.width):
            canvas.draw(bpgfx.Point(x, canvas.height // 2))

            degrees = (x + i) * 2
            radians = math.radians(degrees)
            scale = (canvas.height * 0.75) / 2
            y = int(canvas.height / 2 - math.sin(radians) * scale)
            canvas.draw(bpgfx.Point(x, y))

        TERM_CLEAR = f"\N{ESCAPE}[H\N{ESCAPE}[2J"  # HOME; CLEAR SCREEN
        print(f"{TERM_CLEAR}{canvas}", end="")
        time.sleep(1 / 30)


if __name__ == "__main__":
    main()
