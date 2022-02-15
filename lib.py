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
