from inky import inky
from inky.auto import auto
from PIL import Image, ImageFont, ImageDraw
import math

inky_display = auto()
#inky_display.border_colour(inky.RED)

colors = [inky.WHITE, inky.RED, inky.WHITE, inky.BLACK]
drawColor = ['white','black','red']
colorCount = len(colors)
colorWidth = 10

def getColor(x,y):
    """use the x and y values to calculate the color to display"""
    color = colors[(
                    math.floor(x/colorWidth) + 
                    math.floor(y/colorWidth)
                ) % colorCount] # check pattern
    return color

img = Image.new("P", (inky_display.width, inky_display.height))
draw = ImageDraw.Draw(img)

for x in range(inky_display.width):
    for y in range(inky_display.height):
        color = getColor(x,y)
        inky_display.set_pixel(x,y,color)
        draw.point([x, y], drawColor[color])
print("pixles set")
img.save(fp='/home/pi/dev/pi-playpen/inky/res.bmp', format='bmp')
# inky_display.set_image(img)
inky_display.show()
print("displayed")
