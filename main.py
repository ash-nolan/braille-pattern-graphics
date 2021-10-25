#!/usr/bin/env python3

from typing import List, NewType, Tuple
import itertools
import math
import time

# Braille Dot Numbering
# ---------------------
#   1 4
#   2 3
#   3 6
#   7 8
#
# Unicode Braille Patterns Block
# ------------------------------
# https://en.wikipedia.org/wiki/Braille_Patterns
# https://www.unicode.org/charts/PDF/U2800.pdf
#
#        | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | A | B | C | D | E | F
# U+280x | ⠀ | ⠁ | ⠂ | ⠃ | ⠄ | ⠅ | ⠆ | ⠇ | ⠈ | ⠉ | ⠊ | ⠋ | ⠌ | ⠍ | ⠎ | ⠏
# U+281x | ⠐ | ⠑ | ⠒ | ⠓ | ⠔ | ⠕ | ⠖ | ⠗ | ⠘ | ⠙ | ⠚ | ⠛ | ⠜ | ⠝ | ⠞ | ⠟
# U+282x | ⠠ | ⠡ | ⠢ | ⠣ | ⠤ | ⠥ | ⠦ | ⠧ | ⠨ | ⠩ | ⠪ | ⠫ | ⠬ | ⠭ | ⠮ | ⠯
# U+283x | ⠰ | ⠱ | ⠲ | ⠳ | ⠴ | ⠵ | ⠶ | ⠷ | ⠸ | ⠹ | ⠺ | ⠻ | ⠼ | ⠽ | ⠾ | ⠿
# U+284x | ⡀ | ⡁ | ⡂ | ⡃ | ⡄ | ⡅ | ⡆ | ⡇ | ⡈ | ⡉ | ⡊ | ⡋ | ⡌ | ⡍ | ⡎ | ⡏
# U+285x | ⡐ | ⡑ | ⡒ | ⡓ | ⡔ | ⡕ | ⡖ | ⡗ | ⡘ | ⡙ | ⡚ | ⡛ | ⡜ | ⡝ | ⡞ | ⡟
# U+286x | ⡠ | ⡡ | ⡢ | ⡣ | ⡤ | ⡥ | ⡦ | ⡧ | ⡨ | ⡩ | ⡪ | ⡫ | ⡬ | ⡭ | ⡮ | ⡯
# U+287x | ⡰ | ⡱ | ⡲ | ⡳ | ⡴ | ⡵ | ⡶ | ⡷ | ⡸ | ⡹ | ⡺ | ⡻ | ⡼ | ⡽ | ⡾ | ⡿
# U+288x | ⢀ | ⢁ | ⢂ | ⢃ | ⢄ | ⢅ | ⢆ | ⢇ | ⢈ | ⢉ | ⢊ | ⢋ | ⢌ | ⢍ | ⢎ | ⢏
# U+289x | ⢐ | ⢑ | ⢒ | ⢓ | ⢔ | ⢕ | ⢖ | ⢗ | ⢘ | ⢙ | ⢚ | ⢛ | ⢜ | ⢝ | ⢞ | ⢟
# U+28Ax | ⢠ | ⢡ | ⢢ | ⢣ | ⢤ | ⢥ | ⢦ | ⢧ | ⢨ | ⢩ | ⢪ | ⢫ | ⢬ | ⢭ | ⢮ | ⢯
# U+28Bx | ⢰ | ⢱ | ⢲ | ⢳ | ⢴ | ⢵ | ⢶ | ⢷ | ⢸ | ⢹ | ⢺ | ⢻ | ⢼ | ⢽ | ⢾ | ⢿
# U+28Cx | ⣀ | ⣁ | ⣂ | ⣃ | ⣄ | ⣅ | ⣆ | ⣇ | ⣈ | ⣉ | ⣊ | ⣋ | ⣌ | ⣍ | ⣎ | ⣏
# U+28Dx | ⣐ | ⣑ | ⣒ | ⣓ | ⣔ | ⣕ | ⣖ | ⣗ | ⣘ | ⣙ | ⣚ | ⣛ | ⣜ | ⣝ | ⣞ | ⣟
# U+28Ex | ⣠ | ⣡ | ⣢ | ⣣ | ⣤ | ⣥ | ⣦ | ⣧ | ⣨ | ⣩ | ⣪ | ⣫ | ⣬ | ⣭ | ⣮ | ⣯
# U+28Fx | ⣰ | ⣱ | ⣲ | ⣳ | ⣴ | ⣵ | ⣶ | ⣷ | ⣸ | ⣹ | ⣺ | ⣻ | ⣼ | ⣽ | ⣾ | ⣿


class Canvas:
    def __init__(self, size: Tuple[int, int]) -> None:
        if size[0] < 0 or size[1] < 0:
            raise ValueError(f"Invalid canvas size {size}")

        self._size: Tuple[int, int] = size
        dots_w = int(math.ceil(size[0] / 2) * 2)
        dots_h = int(math.ceil(size[0] / 4) * 4)
        self._dots: List[List[bool]] = [
            [False for _ in range(dots_h)] for _ in range(dots_w)
        ]

    @property
    def size(self) -> Tuple[int, int]:
        return self._size

    @property
    def width(self) -> int:
        return self.size[0]

    @property
    def height(self) -> int:
        return self.size[1]

    def get_dot(self, pos: Tuple[int, int]) -> bool:
        self._validate_dot_position(pos)
        return self._dots[pos[0]][pos[1]]

    def set_dot(self, pos: Tuple[int, int], raised: bool) -> None:
        self._validate_dot_position(pos)
        self._dots[pos[0]][pos[1]] = raised

    def clear(self, raised: bool = False) -> None:
        for x in range(self.width):
            for y in range(self.height):
                self._dots[x][y] = raised

    def __str__(self) -> str:
        s = ""
        for y in range(0, self.height, 4):
            for x in range(0, self.width, 2):
                bits = 0b00000000
                if self._dots[x + 0][y + 0]:
                    bits |= 0b00000001
                if self._dots[x + 0][y + 1]:
                    bits |= 0b00000010
                if self._dots[x + 0][y + 2]:
                    bits |= 0b00000100
                if self._dots[x + 1][y + 0]:
                    bits |= 0b00001000
                if self._dots[x + 1][y + 1]:
                    bits |= 0b00010000
                if self._dots[x + 1][y + 2]:
                    bits |= 0b00100000
                if self._dots[x + 0][y + 3]:
                    bits |= 0b01000000
                if self._dots[x + 1][y + 3]:
                    bits |= 0b10000000
                s += chr(0x2800 | bits)
            s += "\n"
        return s

    def _validate_dot_position(self, pos: Tuple[int, int]) -> None:
        if not (0 <= pos[0] < self.width):
            raise ValueError(
                (
                    f"Invalid x-position {pos[0]} "
                    f"(expected 0 <= x < {self.width})"
                )
            )
        if not (0 <= pos[1] < self.height):
            raise ValueError(
                (
                    f"Invalid y-position {pos[1]} "
                    f"(expected 0 <= y < {self.height})"
                )
            )


def main():
    # 640x480 dots
    # v
    # scale down by 4x
    # v
    # 160x120 dots
    # v
    # with 2x4 dots per monospace character
    # v
    # 80x30 characters total
    canvas = Canvas((160, 120))

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
