from lib import *


#pendiente
class graphSearch(object):
  def __init__(self, mat):
    self.map = mat
    self.size = len(mat)




im = Image('img/Test.bmp')

n = 20

mat = []

sqSize = im.width/n

wall = color(0, 0, 0)
floor = color(255, 255, 255)
start = color(255, 0, 0)
finish = color(0, 255, 0)
path = color(180, 0, 180)
pos=(0, 0)
avCols = [wall, floor]
startFound = False

for y in range(n):
  row = []
  for x in range(n):
    skip = False
    red = 0
    green = 0
    blue = 0
    pixnum = 0
    for iy in range(int(y * sqSize), int((y+1) * sqSize)):
      if skip: break
      for ix in range(int(x * sqSize), int((x+1) * sqSize)):
        if 255 - im.pixels[iy][ix].r + im.pixels[iy][ix].g + im.pixels[iy][ix].b < 25 and not startFound:
          startFound = True
          skip = True
          row.append(start)
          break
        elif 255 - im.pixels[iy][ix].g + im.pixels[iy][ix].r + im.pixels[iy][ix].b < 25:
          if (x == 0 or row[x-1] != finish) and (y == 0 or (mat[y-1][x] != finish and mat[y-1][x-1] != finish)):
            skip = True
            row.append(finish)
            break
        red += im.pixels[iy][ix].r
        green += im.pixels[iy][ix].g
        blue += im.pixels[iy][ix].b
        pixnum += 1
    if skip: continue
    obcol = color(red/pixnum, green/pixnum, blue/pixnum)
    dif = 100000000
    ncol = wall
    for i in avCols:
      subdif = abs(obcol.r - i.r) + abs(obcol.g - i.g) + abs(obcol.b - i.b)
      if subdif < dif:
        ncol = i
        dif = subdif
    row.append(ncol)
  mat.append(row)
    
writebmp('output.bmp', len(mat[0]), len(mat), mat)
