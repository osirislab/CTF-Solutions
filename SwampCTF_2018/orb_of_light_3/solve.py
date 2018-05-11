import glob
from PIL import Image

width = int(320*2.5)
height = 6400*10*10/width

imgs = glob.glob('shadow_fragments/*/*.png')

comp = Image.new('RGB', (width, height))

imgs = sorted(imgs, key=lambda fn: int(fn.split('fragment-')[1].split('.')[0]))

for i, img in enumerate(imgs):
    comp.paste(Image.open(img), (i * 10 % width, (i * 10 // width) * 10))

comp.save('thing.png')
