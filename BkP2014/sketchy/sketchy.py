from PIL import Image, ImageDraw
import struct

# any image will work. I hardcoded the dimensions from the pcap
im = Image.open('blank.png')
drawer = ImageDraw.Draw(im)
# input.txt contains the data between the server and the client
# this data is replayed in this program
data = open('input.txt', 'r').read()

keywords = {
        'meta': '5shh',
        'laser_state': '12s?',
        'move': '5shh',
        'corner': '7s?',
}

i = 0
cursor = (0, 0)
head_down = False
while i < len(data):
        try:
                corner = struct.unpack(keywords['corner'], data[i:i+struct.calcsize(keywords['corner'])])
        except:
                corner = ['']
        try:
                meta = struct.unpack(keywords['meta'], data[i:i+struct.calcsize(keywords['meta'])])
        except:
                meta = ['']
        try:
                laser_state = struct.unpack(keywords['laser_state'], data[i:i+struct.calcsize(keywords['laser_state'])])
        except:
                laser_state = ['']
        try:
                move = struct.unpack(keywords['move'], data[i:i+struct.calcsize(keywords['move'])])
        except:
                move = ['']

        if meta[0] == 'meta\x00':
                i += 10
        elif laser_state[0] == 'LASER_STATE\x00':
                head_down = laser_state[1]
                i += 13
        elif move[0] == 'MOVE\x00':
                temp = (cursor[0]+move[1], cursor[1]+move[2])
                if head_down:
                        drawer.line(cursor + temp, fill=128)
                cursor = temp
                i += 10
        elif corner[0] == 'CORNER\x00':
                i += 8
        else:
                i += 1
                print "unknown :{"

output = open('output.png', 'w')
im.save(output, 'PNG')


