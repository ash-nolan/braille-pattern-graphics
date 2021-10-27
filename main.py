#!/usr/bin/env python3

from typing import List
import itertools
import math
import time

import bpgfx


class MyAnimatedDrawable:
    SIDE_LENGTH = 5

    def __init__(self, position: bpgfx.Point) -> None:
        self.position = position
        self.textures = [
            bpgfx.Texture(self.SIDE_LENGTH, self.SIDE_LENGTH),
            bpgfx.Texture(self.SIDE_LENGTH, self.SIDE_LENGTH),
            bpgfx.Texture(self.SIDE_LENGTH, self.SIDE_LENGTH),
            bpgfx.Texture(self.SIDE_LENGTH, self.SIDE_LENGTH),
        ]
        self.index = 0

        def edge(n) -> bool:
            return n == 0 or n == self.SIDE_LENGTH - 1

        for x in range(self.SIDE_LENGTH):
            for y in range(self.SIDE_LENGTH):
                self.textures[0].set_dot(x, y, x % 2 == y % 2 or None)
                self.textures[1].set_dot(x, y, x % 2 != y % 2 or None)
                self.textures[2].set_dot(x, y, abs(x - y) > 1 or None)
                self.textures[3].set_dot(x, y, edge(x) or edge(y) or None)

    def advance(self):
        self.index = (self.index + 1) % len(self.textures)

    def draw(self, canvas: bpgfx.Canvas):
        sprite = bpgfx.Sprite(self.position, self.textures[self.index])
        canvas.draw(sprite)


def main() -> None:
    canvas = bpgfx.Canvas(160, 120)

    def wave(t: int) -> int:
        radians = math.radians(t)
        scale = (canvas.height * 0.75) / 2
        return int(canvas.height / 2 - math.sin(radians) * scale)

    animated = MyAnimatedDrawable(bpgfx.Point(3, 3))
    boarder = bpgfx.Rectangle(bpgfx.Point(0, 0), canvas.width, canvas.height)

    FPS = 30
    for i in itertools.count(start=1):
        canvas.clear()

        canvas.draw(boarder)

        for x in range(canvas.width):
            y = wave((i + x) * 2)
            canvas.draw(bpgfx.Point(x, canvas.height // 2))
            canvas.draw(bpgfx.Point(x, y))

        canvas.draw(animated)
        if i % 15 == 0:
            animated.advance()

        print(f"{bpgfx.CLEAR}{canvas}", end="")
        time.sleep(1 / FPS)


if __name__ == "__main__":
    main()
