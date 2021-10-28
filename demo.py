#!/usr/bin/env python3

import itertools
import math
import time

import bpgfx


class MyAnimatedDrawable:
    """
    Example user-defined class implementing the drawable interface.
    """

    SIDE_LENGTH = 5

    def __init__(self, x: int, y: int, dx: int = +1, dy: int = +1) -> None:
        self.x = x
        self.y = y
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
                self.textures[0].set(x, y, x % 2 == y % 2 or None)
                self.textures[1].set(x, y, x % 2 != y % 2 or None)
                self.textures[2].set(x, y, abs(x - y) > 1 or None)
                self.textures[3].set(x, y, edge(x) or edge(y) or None)

    def update(self, canvas: bpgfx.Canvas, frame: int):
        self.x += self.dx
        self.y += self.dy

        if self.x <= 1:
            self.dx = +1
        elif self.x + self.SIDE_LENGTH >= canvas.width - 1:
            self.dx = -1

        if self.y <= 1:
            self.dy = +1
        elif self.y + self.SIDE_LENGTH >= canvas.height - 1:
            self.dy = -1

        if frame % 15 == 0:
            self.index = (self.index + 1) % len(self.textures)

    def draw(self, canvas: bpgfx.Canvas):
        sprite = bpgfx.Sprite(self.x, self.y, self.textures[self.index])
        canvas.draw(sprite)


def main() -> None:
    canvas = bpgfx.Canvas(160, 120)

    animated = MyAnimatedDrawable(3, 3)
    boarder = bpgfx.Rectangle(0, 0, canvas.width, canvas.height)
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
            canvas.width // 2,
            canvas.height // 2,
            animated.x + animated.SIDE_LENGTH // 2,
            animated.y + animated.SIDE_LENGTH // 2,
        )
        canvas.draw(follower)
        canvas.draw(animated)
        animated.update(canvas, t)

        # Clear the screen and render the canvas onto the terminal.
        print(f"{bpgfx.CLEAR}{canvas}", end="")
        time.sleep(1 / 30)


if __name__ == "__main__":
    main()
