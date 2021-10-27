#!/usr/bin/env python3

from typing import List
import itertools
import math
import time

import bpgfx


class MyAnimatedDrawable:
    SIDE_LENGTH = 5

    def __init__(self, position: bpgfx.Point, dx=+1, dy=+1) -> None:
        self.position = position
        self.dx = dx
        self.dy = dy
        self.textures = [
            bpgfx.Texture(self.SIDE_LENGTH, self.SIDE_LENGTH),
            bpgfx.Texture(self.SIDE_LENGTH, self.SIDE_LENGTH),
            bpgfx.Texture(self.SIDE_LENGTH, self.SIDE_LENGTH),
            bpgfx.Texture(self.SIDE_LENGTH, self.SIDE_LENGTH),
        ]
        self.counter = 0
        self.index = 0

        def edge(n) -> bool:
            return n == 0 or n == self.SIDE_LENGTH - 1

        for x in range(self.SIDE_LENGTH):
            for y in range(self.SIDE_LENGTH):
                self.textures[0].set_dot(x, y, x % 2 == y % 2 or None)
                self.textures[1].set_dot(x, y, x % 2 != y % 2 or None)
                self.textures[2].set_dot(x, y, abs(x - y) > 1 or None)
                self.textures[3].set_dot(x, y, edge(x) or edge(y) or None)

    def update(self, canvas: bpgfx.Canvas, frame: int):
        self.position.x += self.dx
        self.position.y += self.dy

        if self.position.x <= 1:
            self.dx = +1
        elif self.position.x + self.SIDE_LENGTH >= canvas.width - 1:
            self.dx = -1

        if self.position.y <= 1:
            self.dy = +1
        elif self.position.y + self.SIDE_LENGTH >= canvas.height - 1:
            self.dy = -1

        if frame % 15 == 0:
            self.index = (self.index + 1) % len(self.textures)

    def draw(self, canvas: bpgfx.Canvas):
        sprite = bpgfx.Sprite(self.position, self.textures[self.index])
        canvas.draw(sprite)


def main() -> None:
    canvas = bpgfx.Canvas(160, 120)

    animated = MyAnimatedDrawable(bpgfx.Point(3, 3))
    boarder = bpgfx.Rectangle(bpgfx.Point(0, 0), canvas.width, canvas.height)
    for t in itertools.count(start=1):
        canvas.clear()

        # Draw the rectangular boarder around the canvas.
        canvas.draw(boarder)

        # Draw the points of the sine wave for all on-canvas (x, y) pairs.
        def wave(k: int) -> int:
            radians = math.radians(k * 2)
            scale = (canvas.height * 0.75) / 2
            return int(canvas.height / 2 - math.sin(radians) * scale)

        for x in range(canvas.width):
            canvas.draw(bpgfx.Point(x, canvas.height // 2))  # x-axis
            canvas.draw(bpgfx.Point(x, wave(t + x)))

        # Draw the animated square as well as the line that follows the
        # animated square around the canvas.
        follower = bpgfx.Line(
            bpgfx.Point(canvas.width // 2, canvas.height // 2),
            bpgfx.Point(
                animated.position.x + animated.SIDE_LENGTH // 2,
                animated.position.y + animated.SIDE_LENGTH // 2,
            ),
        )
        canvas.draw(follower)
        canvas.draw(animated)
        animated.update(canvas, t)

        print(f"{bpgfx.CLEAR}{canvas}", end="")
        time.sleep(1 / 30)


if __name__ == "__main__":
    main()
