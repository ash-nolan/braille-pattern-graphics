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

from typing import List
from abc import ABC, abstractmethod
import math


class Canvas:
    def __init__(self, width: int, height: int) -> None:
        if width < 0 or height < 0:
            raise ValueError(f"Invalid canvas size {width}x{height}")
        # fmt: off
        self._width:  int = width
        self._height: int = height
        dots_w = int(math.ceil(width  / 2) * 2)
        dots_h = int(math.ceil(height / 4) * 4)
        self._dots: List[List[bool]] = \
            [[False for _ in range(dots_w)] for _ in range(dots_h)]
        # fmt: on

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def get_dot(self, x: int, y: int) -> bool:
        if not (0 <= x < self.width and 0 <= y < self.height):
            # off-canvas
            return False
        return self._dots[y][x]

    def set_dot(self, x: int, y: int, raised: bool) -> None:
        if not (0 <= x < self.width and 0 <= y < self.height):
            # off-canvas
            return
        self._dots[y][x] = raised

    def clear(self, raised: bool = False) -> None:
        for y in range(self.height):
            for x in range(self.width):
                self._dots[y][x] = raised

    def draw(self, drawable: "Drawable") -> None:
        drawable.draw(self)

    def __repr__(self) -> str:
        name: str = type(self).__name__
        dots: str = repr(self._dots)
        return f"{name}({self.width}x{self.height}, {dots})"

    def __str__(self) -> str:
        s = ""
        for y in range(0, self.height, 4):
            for x in range(0, self.width, 2):
                bits = 0b00000000
                if self._dots[y + 0][x + 0]:
                    bits |= 0b00000001
                if self._dots[y + 1][x + 0]:
                    bits |= 0b00000010
                if self._dots[y + 2][x + 0]:
                    bits |= 0b00000100
                if self._dots[y + 0][x + 1]:
                    bits |= 0b00001000
                if self._dots[y + 1][x + 1]:
                    bits |= 0b00010000
                if self._dots[y + 2][x + 1]:
                    bits |= 0b00100000
                if self._dots[y + 3][x + 0]:
                    bits |= 0b01000000
                if self._dots[y + 3][x + 1]:
                    bits |= 0b10000000
                s += chr(0x2800 | bits)
            s += "\n"
        return s


class Drawable(ABC):
    @abstractmethod
    def draw(self, canvas: Canvas) -> None:
        pass


class Point(Drawable):
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y

    def draw(self, canvas: Canvas) -> None:
        canvas.set_dot(self.x, self.y, True)


class Line(Drawable):
    def __init__(self, p1: Point, p2: Point) -> None:
        self.p1: Point = p1
        self.p2: Point = p2

    def draw(self, canvas: Canvas) -> None:
        # Optimized line function from the article "Line drawing on a grid"
        # written by Red Blob Games, ported from C# to Python3.
        # https://www.redblobgames.com/grids/line-drawing.html
        #
        # The number of steps to take is exactly the diagonal distance between
        # (x1, y1) and (x2, y2).
        dx: int = self.p2.x - self.p1.x
        dy: int = self.p2.y - self.p1.y
        abs_dx: int = abs(dx)
        abs_dy: int = abs(dy)
        nsteps: int = abs_dx if abs_dx > abs_dy else abs_dy
        # Calculate the x and y step distance per step-iteration.
        nsteps_inverse: float = 1.0 / nsteps
        xstep: float = dx * nsteps_inverse
        ystep: float = dy * nsteps_inverse
        # Draw each (x, y) dot from (x1, y1) to (x2, y2). These dots are
        # connected by either an dot edge edge (e.g. ⠆) or a corner between the
        # two dots (e.g. ⠊).
        x: float = float(self.p1.x)
        y: float = float(self.p1.y)
        for i in range(nsteps + 1):
            canvas.set_dot(int(round(x)), int(round(y)), True)
            x += xstep
            y += ystep
