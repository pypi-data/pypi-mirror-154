import sys
import numbers
import typing

color_arg = typing.Union[int, str]


class Color:
    black = 0
    red = 1
    green = 2
    yellow = 3
    blue = 4
    pink = 5
    brown = 6
    white = 7

    color_dict = {
        "black": black,
        "red": red,
        "green": green,
        "yellow": yellow,
        "blue": blue,
        "pink": pink,
        "brown": brown,
        "white": white
    }

    named_colors = {
        "error": [1, red, black],
        "err": [1, red, black],
        "success": [1, green, None],
        "succ": [1, green, None],
        "warning": [1, yellow, None],
        "warn": [1, yellow, None],
        "info": [1, blue, None],
        "default": [None, None, None]
    }

    _end_string = "\x1b[0m"
    end = _end_string

    def __init__(self, style: numbers.Integral = None, color: color_arg = None, background: color_arg = None,
                 name: str = None, out: typing.IO = sys.stdout):
        self.out = out
        formats = []
        self.style, self.col, self.back = self.named_colors.get(name, [None, None, None])

        if isinstance(style, numbers.Integral):
            if 0 <= style < 8:
                self.style = style

        if isinstance(color, numbers.Integral):
            if 0 <= color < 8:
                self.col = color
        elif isinstance(color, str):
            self.col = self.color_dict.get(color, None)

        if isinstance(background, numbers.Integral):
            if 0 <= background < 8:
                self.back = background
        elif isinstance(background, str):
            self.back = self.color_dict.get(background, None)

        if self.style is not None:
            formats.append(str(self.style))
        if self.col is not None:
            formats.append(f"3{self.col}")
        if self.back is not None:
            formats.append(f"4{self.back}")

        self._color_string = f"\x1b[{';'.join(formats)}m"

    def start(self):
        return self._color_string

    def stop(self):
        return self._end_string

    def __str__(self):
        return self._color_string

    def __repr__(self):
        return f"<{self.__class__.__name__}({self._color_string[2:-1]})" \
               f"[{self._color_string}{self._color_string[2:-1]}{self._end_string}]>"

    def __enter__(self):
        self.out.write(self._color_string)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.out.write(self._end_string)

    def __getattr__(self, item):
        pass


# Color.error = Color(name="error")
for col in Color.named_colors:
    setattr(Color, col, Color(name=col))
# for name, col in Color.named_colors.items():
#     # Color.__setattr__(name, Color(*col))
#     print(col)
#     Color.__dict__[name] = Color(*col)
