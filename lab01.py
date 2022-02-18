#Universidad del Valle de Guatemala
#Sebastian Maldonado
#Laurelinda Gomez
#Laboratorio 1


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

#Impresion
  def printInfo(self):
    print(self.map)
    print(self.size)
    print(self.startpos)
    print(self.finishlist)

#Escritura de la imagen
  def writeImage(self):
    writebmp('discrete.bmp', self.size, self.size, self.map)
  
#Escritura del path
  def writePath(self, path):
    mat = self.map[:]
    for item in path:
      x = item[0]
      y = item[1]
      if mat[y][x] == floor: mat[y][x] = pathc
    writebmp('path.bmp', self.size, self.size, mat)

#Acciones  
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
  
#Resultado  
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
def breath_first(problem):
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

def depth_first(problem, node = None, visited=[]):
  if node is None: node = problem.startpos
  if not node in visited:
    posible_paths = []
    visited.append(node)
    if problem.goalTest(node):
      return [node]
    for a in problem.actions(node):
      result = problem.result(node, a)
      path = depth_first(problem, result, visited[:])
      if path: posible_paths.append(path)
    if not posible_paths: return []
    smallest = posible_paths[0]
    for p in posible_paths:
      if len(p) < len(smallest):
        smallest = p
    smallest.insert(0, node)
    return smallest
  else:
    return []

#La heuristica 1
def heuristic1(problem, node):
  d = float('inf')
  for finish in problem.finishlist:
    dy = abs(finish[1] - node[1])
    dx = abs(finish[0] - node[0])
    if dx + dy < d: d = dx + dy
  return d

def astar(problem, heu):
  openList = [(problem.startpos,0,[])]
  closedList = []
  while openList:
    current = openList[0]
    for node in openList:
      if node[1] < current[1]:
        current = node
    openList.remove(current)
    s = current[0]
    closedList.append(s)
    if problem.goalTest(s):
      return current[2]
    for a in problem.actions(s):
      result = problem.result(s, a)
      if result in closedList: continue
      g = current[2][:]
      g.append(result)
      h = heu(problem, s)
      f = len(g) + h
      cont = False
      for op in openList:
        if op[0] == result and len(g) > len(op[2]):
          cont = True
          break
      if cont: continue
      openList.append((result, f, g))
  else:
    return []


npath = astar(f1, heuristic1)
print(npath)
f1.writePath(npath)
#npath = graph_search(f1)

#f1.writePath(npath)

#(2,12) 22
#(16,19) 24
