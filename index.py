from PIL import Image,ImageMorph,ImageChops,ImageOps
import numpy as np


image = Image.open("./sapo.png")
image2 = Image.open("./cachorro.png")
image3 = Image.open("./blue_pen.png")

out = ImageChops.invert(image)
out = out.rotate(180)
temp_out = out.composite(image2,image3,image)
ImageChops.lighter(temp_out,out).show()

print(image.size)
width, height = image.size
print(image.filename)
print(image.format)
print(image.format_description)