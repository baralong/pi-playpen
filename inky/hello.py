from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw

inky_display = InkyPHAT("red")
inky_display.set_border(inky_display.RED)

img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)
from font_fredoka_one import FredokaOne
from font_source_sans_pro import SourceSansPro
y = 5
for h in range (5,50,5):
    font = ImageFont.truetype(SourceSansPro, h)
    message = f"Hello, World! {h}"
    w, h = font.getsize(message)
    x = (inky_display.WIDTH / 2) - (w / 2)
    draw.text((x, y), message, inky_display.BLACK, font)
    y += h
    if y >= inky_display.HEIGHT: break

inky_display.set_image(img)
inky_display.show()
