from PIL import Image

im = Image.open('glance.gif')
im2 = Image.new('RGB', (400, 600))

for f in range(200):
	im.seek(f)
	
	im2.paste(im.copy(), (f*2, 0))

im2.save("out.png")