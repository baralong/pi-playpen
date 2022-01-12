import LCD_1in44
import LCD_Config
import time
from PIL import Image,ImageDraw,ImageFont,ImageColor

#try:
def main():
    LCD = LCD_1in44.LCD()
    
    print( "**********Init LCD**********")
    Lcd_ScanDir = LCD_1in44.D2U_L2R #SCAN_DIR_DFT  #SCAN_DIR_DFT = D2U_L2R
    LCD.LCD_Init(Lcd_ScanDir)
    LCD.LCD_Clear()
    input("...")

    image = Image.new("RGB", (LCD.width, LCD.height), "YELLOW")
    LCD.LCD_ShowImage(image,0,0)
    input("...")
    draw = ImageDraw.Draw(image)
    #font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 16)
    print ("***draw line")
    draw.line([(0,0),(127,0)], fill = "BLUE",width = 5)
    draw.line([(127,0),(127,127)], fill = "BLUE",width = 5)
    draw.line([(127,127),(0,127)], fill = "BLUE",width = 5)
    draw.line([(0,127),(0,0)], fill = "BLUE",width = 5)
    LCD.LCD_ShowImage(image,0,0)
    input("...")
    
    print ("***draw rectangle")
    draw.rectangle([(18,10),(110,60)],fill = "RED")
    LCD.LCD_ShowImage(image,0,0)
    input("...")

    print ("***draw text")
    draw.line([(33, 22),(28,48)], fill="GREEN", width=2)
    LCD.LCD_ShowImage(image,0,0)
    input("...")
    # top left location
    draw.text((33, 22), 'WaveShare ', fill = "BLUE")
    draw.text((32, 36), 'Electronic ', fill = "BLUE")
    draw.text((28, 48), '1.44inch LCD ', fill = "BLUE")
    LCD.LCD_ShowImage(image,0,0)
    input("...")

    LCD_Config.Driver_Delay_ms(500)

    print ("***draw bitmap")
    image = Image.open('sky.bmp')
    LCD.LCD_ShowImage(image,0,0)
	
	#while (True):
	
if __name__ == '__main__':
    main()

#except:
#	print("except")
#	GPIO.cleanup()
