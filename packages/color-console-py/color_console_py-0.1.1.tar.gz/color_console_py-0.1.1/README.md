# color_console_py

Small tool that enables you to write to the console in color using context mangers or f-strings.

It uses ANSI codes to color the console.

# How to use

## Getting a color

Creating a color requires `style`, `color` and `background`, all of which can be called as positional or keyword arguments.
If not specified they will default to the console's default.

Colors can also be called as attributes of `Color` or strings:
 - `Color.black` = `0`
 - `Color.red` = `1`
 - `Color.green` = `2`
 - `Color.yellow` = `3`
 - `Color.blue` = `4`
 - `Color.pink` = `5`
 - `Color.brown` = `6`
 - `Color.white` = `7`

Possible ways to call:
```python
from color_console import Color

Color(1, 2, 3) # resulting color will be in style 1, color green, background yellow
Color() # resulting color will in default style, default color, default background
Color(1, "black", "white") #resulting color will be in style 1, color black, background white
Color(color=Color.red) # resulting color will be in default style, color red, default background
```

There are also some color presets like `error`/`err`, `success`/`succ`, `warning`/`warn`, `info`, 
that can be called with the positional keyword `name` or as an attribute of `Color`.

In this you can also define your own colors:

```python
from color_console import Color

Color(name="error") # resulting color will be style 1, color red, background black
Color.info # resulting color will be style 1, color blue, default background

Color.test = Color(1, Color.pink, Color.brown) # color saved
Color.test # resulting color will be style 1, color pink, background brown
```

## Using a color

Using a color can be done by printing it directly or using context managers:

Simple example:
```python
from color_console import Color

col1 = Color(1, 2, 3) # get your color
print(col1.start()) # changes your console to the desired color/style
print("This is in color/style specified by col1")

col2 = Color(4, 5, 6) # get your color, no need to reset before
print(col2.start())
print("This is in color/style specified by col2")

print(col2.stop()) # resets the color
```

Better example using implicit conversion to str in f-strings:
```python
from color_console import Color

print(f"{Color(1, 2, 3)}This is in the first color, {Color(4, 5, 6)} This is in the second color, {Color.end} This is in the default color")
```

Using context managers:
```python
from color_console import Color

with Color.info:
    print("This will be in the specified color")
    print("You can print as much as you want in the with-statement")
print("This will be in the default color again")
```

# Color combinations

Here it shows the used ANSI codes in its respective style and color. 
The following are the numbers that are used under the hood (the Color class uses the numbers 0-8 for everything)

First number (0-7): Style

Second number(30-37): Text color

Third number(40-47): Background color

## Style 0

![style 0](readme_img/style0.png)

## Style 1

![style 1](readme_img/style1.png)

## Style 2

![style 2](readme_img/style2.png)

## Style 3

![style 3](readme_img/style3.png)

## Style 4

![style 4](readme_img/style4.png)

## Style 5

![style 5](readme_img/style5.png)

## Style 6

![style 6](readme_img/style6.png)

## Style 7

![style 7](readme_img/style7.png)

## Misc

![misc](readme_img/seperate.png)
