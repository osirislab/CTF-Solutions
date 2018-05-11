import math
import matplotlib.pyplot as plt

stuff = []
for line in open('page_of_numbers.p'):
    if 'F' in line:
        stuff.append(float(line[line.index('F')+1:]))

stuff = [tuple(stuff[i:(i+5)]) for i in range(0, len(stuff), 5)]

xs = []
ys = []

def compute(x,y,speed,angle,direction,g):
    v_y = speed*math.sin(angle)
    t = 2*v_y/g
    d = speed*t*math.cos(angle)
    new_x = x - d*math.cos(direction)
    new_y = y - d*math.sin(direction)
    return new_x, new_y

def compute_g(x,y,speed,angle,direction,final_x,final_y):
    v_x = speed*math.cos(angle)
    v_y = speed*math.sin(angle)
    d = math.sqrt((x-final_x)**2 + (y-final_y)**2)
    t = d/v_x
    g = 2*v_y/t
    return g

if __name__ == "__main__":
    examples = []
    for l in open('examples'):
        if l.startswith('(('):
            ((x,y,speed,angle,direction),(final_y,final_x)) = eval(l)
            examples.append((x,y,speed,angle,direction,final_x,final_y))

    gs = []
    for e in examples:
        g=compute_g(*e)
        gs.append(g)
        print(g)
        print(compute(e[0],e[1],e[2],e[3],e[4],g))

    for (x,y,speed,angle,direction) in stuff:
        new_x, new_y = compute(x,y,speed,angle,direction, 9.81)
        xs.append(new_x)
        ys.append(new_y)

    plt.scatter(xs, ys)
    plt.show()
