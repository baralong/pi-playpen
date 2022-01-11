from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw

inky_display = InkyPHAT("red")
colors = [InkyPHAT.BLACK, InkyPHAT.WHITE, InkyPHAT.RED]
colorCount = len(colors)

def getColor(x,y):
    """use the x and y values to calculate the color to display"""
    color = colors[round((x+y)/2) % colorCount] # diagonal stripes
    return color

# img = Image.open("/home/pi/dev/pi-playpen/inky/inky-test-1.png")
#inky_display.set_image(img))
for x in range(inky_display.WIDTH):
    for y in range(inky_display.HEIGHT):
        inky_display.set_pixel(x, y, getColor(x,y))
print("pixles set")
inky_display.show()
print("displayed")
