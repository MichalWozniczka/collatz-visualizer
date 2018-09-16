import PIL.Image, PIL.ImageDraw, PIL.ImageFont
from tkinter import *
import math
import time

class Point():
    def __init__(self, coords, dirn):
        self.coords = coords
        self.dirn = dirn

def isEven(i):
    return not i%2

def pointOnCircle(coords, theta):
    return [coords[0] + math.cos(theta), coords[1] + math.sin(theta)]

def buildCollatz():
    x = int(entries[0].get())
    y = int(entries[1].get())
    n = int(entries[2].get())
    bg = entries[3].get()
    branchColor = entries[4].get()
    textColor = entries[6].get()
    oddRot = float(entries[7].get()) * math.pi / 180
    evenRot = float(entries[8].get()) * math.pi / 180
    width = int(entries[9].get())

    line_segs = []
    points = dict()
    points[1] = Point([0,0], math.pi/2)

    for i in range(1,n+1):
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
                newDir += evenRot
            else:
                newDir += oddRot
            points[j] = Point(pointOnCircle(points[i].coords, newDir), newDir)
            line_segs.append([points[i].coords, points[j].coords])
            i = j

    minx = x
    maxx = 0
    miny = y
    maxy = 0
    for key,point in points.items():
        minx = min(minx, point.coords[0])
        maxx = max(maxx, point.coords[0])
        miny = min(miny, point.coords[1])
        maxy = max(maxy, point.coords[1])

    scale_factor = min(x / (maxx-minx), y / (maxy-miny))*.9

    im = PIL.Image.new("RGB", (x,y), bg)
    draw = PIL.ImageDraw.Draw(im)

    for line in line_segs:
        line1 = line[0][:]
        line1[0] = (line1[0]-minx) * scale_factor + x/2 - abs(maxx-minx)*scale_factor/2
        line1[1] = -((line1[1]-miny) * scale_factor + y/2 - abs(maxy-miny)*scale_factor/2)+y
        line2 = line[1][:]
        line2[0] = (line2[0]-minx) * scale_factor + x/2 - abs(maxx-minx)*scale_factor/2
        line2[1] = -((line2[1]-miny) * scale_factor + y/2 - abs(maxy-miny)*scale_factor/2)+y
        draw.line([tuple(line1), tuple(line2)], width=width, fill=branchColor)

    font = PIL.ImageFont.truetype("DejaVuSans.ttf", 10)

    if displayNums.get():
        for key,point in points.items():
            coords = point.coords[:]
            coords[0] = (coords[0]-minx) * scale_factor + x/2 - abs(maxx-minx)*scale_factor/2
            coords[1] = -((coords[1]-miny) * scale_factor + y/2 - abs(maxy-miny)*scale_factor/2)+y
            draw.text(tuple(coords), str(key), font=font, fill=textColor)

    fileName = "visual" + str(int(time.time())) + ".png"
    im.save(fileName)

master = Tk()
Label(master, text="Picture width (pixels)").grid(row=0)
Label(master, text="Picture height (pixels)").grid(row=1)
Label(master, text="Number of sequences").grid(row=2)
Label(master, text="Background color (format: #rrggbb)").grid(row=3)
Label(master, text="Branch color (format: #rrggbb)").grid(row=4)
Label(master, text="Display numbers?").grid(row=5)
Label(master, text="Number text color (format: #rrggbb)").grid(row=6)
Label(master, text="Odd number rotation (degrees)").grid(row=7)
Label(master, text="Even number rotation (degrees)").grid(row=8)
Label(master, text="Line width (pixels)").grid(row=9)

entries = [Entry(master) for i in range(5)]
displayNums = IntVar()
check = Checkbutton(master, text="", variable=displayNums).grid(row=5, column=1)
for i in range(5,10):
    entries.append(Entry(master))

entries[0].insert(10,"4000")
entries[1].insert(10,"4000")
entries[2].insert(10,"1000")
entries[3].insert(10,"#fff9c6")
entries[4].insert(10,"#211400")
entries[6].insert(10,"#27a01c")
entries[7].insert(10,"12")
entries[8].insert(10,"-6")
entries[9].insert(10,"5")

for idx, entry in enumerate(entries):
    if idx == 5:
        continue
    entry.grid(row=idx, column=1)

Button(master, text="Create", command=buildCollatz).grid(row=11, column=0, sticky=W, pady=4)
Button(master, text="Cancel", command=master.quit).grid(row=11, column=1, sticky=W, pady=4)

mainloop()
