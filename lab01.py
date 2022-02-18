from lib import *
from algorithms import *
from time import time as clock


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

  def writeImage(self):
    writebmp('discrete.bmp', self.size, self.size, self.map)
  
  def writePath(self, path, name='path.bmp'):
    mat = self.map[:]
    for item in path:
      x = item[0]
      y = item[1]
      if mat[y][x] == floor: mat[y][x] = pathc
    writebmp(name, self.size, self.size, mat)
  
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

mat = discretize_image('./img/Test2.bmp', 25)
    
f1 = Framework(mat)
f1.writeImage()

# npath = breath_first(f1)
# npath = depth_first(f1)
start = clock()
npath1 = astar(f1, heuristic1)
mid = clock()
npath2 = astar(f1, heuristic1)
end = clock()
h1 = mid - start
h2 = end - mid
print('Tiempos: h1=%s    h2=%s'%(h1,h2))
f1.writePath(npath1, 'path1.bmp')
f1.writePath(npath2, 'path2.bmp')
