import struct


def char(c):
  return struct.pack('=c', c.encode('ascii'))

def hword(w):
  return struct.pack('=h', w)

def word(d):
  return struct.pack('=l', d)

def ccolor(v):
  return max(0, min(255, int(v)))

class color(object):
  def __str__(self):
    return 'r: %i, g: %i, b: %i'%(self.r, self.g, self.b)

  def __repr__(self):
    return '[r%ig%ib%i]'%(self.r, self.g, self.b)

  def __init__(self, r, g, b):
    self.r = r
    self.g = g
    self.b = b

  def __add__(self, other_color):
    r = self.r + other_color.r
    g = self.g + other_color.g
    b = self.b + other_color.b

    return color(r, g, b)

  def __mul__(self, other):
    r = self.r * other
    g = self.g * other
    b = self.b * other
    return color(r, g, b)
  
  
  def toBytes(self):
    r = ccolor(self.r)
    g = ccolor(self.g)
    b = ccolor(self.b)
    return bytes([b, g, r])

def writebmp(filename, width, height, pixels):
  f = open(filename, 'bw')

  f.write(char('B'))
  f.write(char('M'))
  f.write(word(54 + width * height * 3))
  f.write(word(0))
  f.write(word(54))

  f.write(word(40))
  f.write(word(width))
  f.write(word(height))
  f.write(hword(1))
  f.write(hword(24))
  f.write(word(0))
  f.write(word(width * height * 3))
  f.write(word(0))
  f.write(word(0))
  f.write(word(0))
  f.write(word(0))
  for y in range(height):
    for x in range(width):
      f.write(pixels[y][x].toBytes())
    for _ in range(width % 4):
      f.write(struct.pack('=x'))
  f.close()

class Image(object):
  def __init__(self, path):
    self.path = path
    self.read()
  
  def read(self):
    image = open(self.path, 'rb')
    image.seek(10)
    header_size = struct.unpack('=l', image.read(4))[0]
    image.seek(18)

    self.width = struct.unpack('=l', image.read(4))[0]
    self.height = struct.unpack('=l', image.read(4))[0]
    self.pixels = []
    image.seek(28)
    pixel_size = struct.unpack('=h', image.read(2))[0]
    image.seek(header_size)
    for y in range(self.height):
      self.pixels.append([])
      for _ in range(self.width):
        b = ord(image.read(1))
        g = ord(image.read(1))
        r = ord(image.read(1))
        if pixel_size == 32: image.read(1)
        self.pixels[y].append(color(r, g, b))
      for _ in range(self.width%4):
        image.read(1)
    image.close()

wall = color(0, 0, 0)
floor = color(255, 255, 255)
start = color(255, 0, 0)
finish = color(0, 255, 0)
pathc = color(180, 0, 180)

def discretize_image(path, n):
  im = Image(path)
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
      dif = float('inf')
      ncol = wall
      for i in avCols:
        subdif = abs(obcol.r - i.r) + abs(obcol.g - i.g) + abs(obcol.b - i.b)
        if subdif < dif:
          ncol = i
          dif = subdif
      row.append(ncol)
    mat.append(row)
  return mat