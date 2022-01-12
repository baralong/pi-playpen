from inky import InkyPHAT, inky
from PIL import Image, ImageFont, ImageDraw

inky_display = InkyPHAT("red")
#inky_display.border_colour(InkyPHAT.RED)
#inky_display = inky.Inky(resolution=(106,104),colour='red')

colors = [InkyPHAT.WHITE, InkyPHAT.BLACK, InkyPHAT.WHITE, InkyPHAT.RED]
drawColor = ['white','black','red']
colorCount = len(colors)
colorWidth = 10

def getColor(x,y):
    """use the x and y values to calculate the color to display"""
    color = colors[(
                    (round(x/colorWidth)%colorCount) + 
                    (round(y/colorWidth)%colorCount)
                )%colorCount] # check pattern
    return color

img = Image.open("/home/pi/dev/pi-playpen/inky/logo.png")
img = Image.new("P", (inky_display.width, inky_display.height))
draw = ImageDraw.Draw(img)
for x in range(inky_display.width):
    for y in range(inky_display.height):
        color = getColor(x,y)
        inky_display.set_pixel(x,y,color)
        draw.point([x, y], drawColor[color])
        print (x,y, color, drawColor[color])
print("pixles set")
img.save(fp='/home/pi/dev/pi-playpen/inky/res.png', format='png')
inky_display.set_image(img)
inky_display.show()
print("displayed")
