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

    sprite1 = bpgfx.Sprite(bpgfx.Point(3, 3), 5, 5)
    sprite2 = bpgfx.Sprite(bpgfx.Point(3, 3), 5, 5)
    for x in range(5):
        for y in range(5):
            sprite1.set_dot(x, y, x % 2 == y % 2)
            sprite2.set_dot(x, y, x % 2 != y % 2)

    for i in itertools.count(start=1):
        canvas.clear()

        # Draw boarder box.
        canvas.draw(
            bpgfx.Rectangle(bpgfx.Point(0, 0), canvas.width, canvas.height)
        )

        # Draw the sine wave.
        for x in range(canvas.width):
            canvas.draw(bpgfx.Point(x, canvas.height // 2))

            degrees = (x + i) * 2
            radians = math.radians(degrees)
            scale = (canvas.height * 0.75) / 2
            y = int(canvas.height / 2 - math.sin(radians) * scale)
            canvas.draw(bpgfx.Point(x, y))

        # Draw sprite.
        if i % 15 == 0:
            sprite1, sprite2 = sprite2, sprite1
        canvas.draw(sprite1)

        TERM_CLEAR = f"\N{ESCAPE}[H\N{ESCAPE}[2J"  # HOME; CLEAR SCREEN
        print(f"{TERM_CLEAR}{canvas}", end="")
        time.sleep(1 / 30)


if __name__ == "__main__":
    main()
