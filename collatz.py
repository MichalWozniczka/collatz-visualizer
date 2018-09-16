from PIL import Image, ImageDraw
import math

x = 512
y = 512

class Point():
    def __init__(self, coords, dirn):
        self.coords = coords
        self.dirn = dirn

def isEven(i):
    return not i%2

def pointOnCircle(coords, theta):
    return [coords[0] + math.cos(theta), coords[1] + math.sin(theta)]

def buildCollatz():
    line_segs = []
    points = dict()
    points[1] = Point([0,0], math.pi/2)

    for i in range(1,21):
        ancestorList = []
        while i not in points:
            ancestorList.append(i)
            if isEven(i):
                i = i >> 1
            else:
                i = (i << 2) + 1 - i
        while ancestorList:
            j = ancestorList.pop()
            newDir = points[i].dirn
            if isEven(j):
                newDir -= math.pi/30
            else:
                newDir += math.pi/15
            points[j] = Point(pointOnCircle(points[i].coords, newDir), newDir)
            line_segs.append([points[i].coords, points[j].coords])
            i = j

    minx = x
    maxx = 0
    miny = y
    maxy = 0
    for key,point in points.items():
        print(key,point.coords)
        minx = min(minx, point.coords[0])
        maxx = max(maxx, point.coords[0])
        miny = min(miny, point.coords[1])
        maxy = max(maxy, point.coords[1])

    scale_factor = (x / (maxx-minx)) if (maxx-minx) > (maxy-miny) else (y / (maxy-miny))

    print(minx, maxx, miny, maxy, scale_factor)

    im = Image.new("RGB", (512,512), "gray")
    draw = ImageDraw.Draw(im)

    for line in line_segs:
        print(line)
        line1 = line[0][:]
        line1[0] = (line1[0]-minx) * scale_factor
        line1[1] = -((line1[1]-miny) * scale_factor)+y
        line2 = line[1][:]
        line2[0] = (line2[0]-minx) * scale_factor
        line2[1] = -((line2[1]-miny) * scale_factor)+y
        print(line)
        draw.line([tuple(line1), tuple(line2)])

    for key,point in points.items():
        coords = point.coords[:]
        coords[0] = (coords[0]-minx) * scale_factor
        coords[1] = -((coords[1]-miny) * scale_factor)+y
        draw.text(tuple(coords), str(key))
        print(key)

    im.save("visual.png")

if __name__ == "__main__": buildCollatz()
