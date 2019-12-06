from PIL import Image
img = Image.new('RGB', (30,33), (0, 0, 0))
img.save("./blocks/void.bmp", "BMP")