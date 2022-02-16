from lib import *

wall = color(0, 0, 0)
floor = color(255, 255, 255)
start = color(255, 0, 0)
finish = color(0, 255, 0)
pathc = color(180, 0, 180)

class Framework(object):
  def __init__(self, mat):
    self.map = mat
    self.size = len(mat)
    self.startpos = (0, 0)
    self.finishlist = []
    for y in range(self.size):
      for x in range(self.size):
        if mat[y][x] == start:
          self.startpos = (x, y)
        elif mat[y][x] == finish:
          self.finishlist.append((x, y))
    self.currentpos = self.startpos

  def printInfo(self):
    print(self.map)
    print(self.size)
    print(self.startpos)
    print(self.finishlist)

  def writeImage(self):
    writebmp('discrete.bmp', self.size, self.size, self.map)
  
  def writePath(self, path):
    mat = self.map[:]
    for item in path:
      x = item[0]
      y = item[1]
      if mat[y][x] == floor: mat[y][x] = pathc
    writebmp('path.bmp', self.size, self.size, mat)
  
  def actions(self, s):
    a = {'l','r','u','d'}
    x = s[0]
    y = s[1]
    if x == 0 or self.map[y][x-1] == wall:
      a.remove('l')
    if x == self.size - 1 or self.map[y][x+1] != floor:
      a.remove('r')
    if y == 0 or self.map[y-1][x] == wall:
      a.remove('d')
    if y == self.size - 1 or self.map[y+1][x] != floor:
      a.remove('u')
    return a
  
  def result(self, s, a):
    x = s[0]
    y = s[1]
    if a == 'u':
      sp = (x, y + 1)
    elif a == 'd':
      sp = (x, y - 1)
    elif a == 'l':
      sp = (x - 1, y)
    else:
      sp = (x + 1, y)
    return sp

  def goalTest(self, s):
    return s in self.finishlist
  
  def stepCost(self, s, a, sp):
    pass

  def pathCost(self, ls):
    return len(ls)  


im = Image('img/Test2.bmp')

n = 20

mat = []

sqSize = im.width/n

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
    
f1 = Framework(mat)
f1.writeImage()
def graph_search(problem):
  frontier = [[problem.startpos]]
  explored = []

  while True:
    if len(frontier):
      path = frontier.pop(0)
      #print(len(path))
      s = path[-1]
      explored.append(s)
      if problem.goalTest(s):
        return path
      for a in problem.actions(s):
        result = problem.result(s, a)
        if result not in explored:
          new_path = path[:]
          new_path.append(result)
          frontier.append(new_path)
    else:
      return False

npath = graph_search(f1)

f1.writePath(npath)

#(2,12) 22
#(16,19) 24