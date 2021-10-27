#!/usr/bin/env python3

from typing import List
import itertools
import math
import time

import bpgfx


class AnimatedSprite:
    def __init__(
        self, position: bpgfx.Point, textures: List[bpgfx.Texture]
    ) -> None:
        assert len(textures) != 0
        self.position = position
        self.textures = textures
        self.index = 0

    def advance_texture(self):
        self.index = (self.index + 1) % len(self.textures)

    def draw(self, canvas: bpgfx.Canvas):
        sprite = bpgfx.Sprite(self.position, self.textures[self.index])
        canvas.draw(sprite)


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

    TEXTURE_SIDE_LENGTH = 5
    textures = [
        bpgfx.Texture(TEXTURE_SIDE_LENGTH, TEXTURE_SIDE_LENGTH),
        bpgfx.Texture(TEXTURE_SIDE_LENGTH, TEXTURE_SIDE_LENGTH),
        bpgfx.Texture(TEXTURE_SIDE_LENGTH, TEXTURE_SIDE_LENGTH),
        bpgfx.Texture(TEXTURE_SIDE_LENGTH, TEXTURE_SIDE_LENGTH),
    ]
    for x in range(5):
        for y in range(5):

            def edge(n):
                return n == 0 or n == TEXTURE_SIDE_LENGTH - 1

            textures[0].set_dot(x, y, x % 2 == y % 2)
            textures[1].set_dot(x, y, x % 2 != y % 2)
            textures[2].set_dot(x, y, abs(x - y) > 1)
            textures[3].set_dot(x, y, edge(x) or edge(y))
    animated_sprite = AnimatedSprite(bpgfx.Point(3, 3), textures)

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
        canvas.draw(animated_sprite)
        if i % 15 == 0:
            animated_sprite.advance_texture()

        TERM_CLEAR = f"\N{ESCAPE}[H\N{ESCAPE}[2J"  # HOME; CLEAR SCREEN
        print(f"{TERM_CLEAR}{canvas}", end="")
        time.sleep(1 / 30)


if __name__ == "__main__":
    main()
