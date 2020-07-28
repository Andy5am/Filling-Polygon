
#Andy Castillo 18040
#SR1: Point
# from obj import Obj
import struct

def char(c):
  return struct.pack('=c', c.encode('ascii'))

def word(c):
  return struct.pack('=h', c)

def dword(c):
  return struct.pack('=l', c)

class Render(object):
  def __init__(self):
    self.framebuffer = []

  def glInit(self):
    self.width = 400
    self.height = 400

  def glCreateWindow(self, width, height):
    self.width = width
    self.height= height

  def glViewPort(self, x ,y , width, height):
    self.xVP = x
    self.yVP = y
    self.widthVP = width
    self.heightVP = height

  def glClear(self):
    self.framebuffer = [
      [self.backgroundColor for x in range(self.width+1)]
      for y in range(self.height+1)
    ]
    
  def glClearColor(self, r, g , b):
    self.backgroundColor = bytes([b*255, g*255, r*255])

  def glVertex(self, x , y):
    if x>1:
      x=1
    if y>1:
      y=1
    coordX = round(self.xVP + (self.widthVP/2 * (1+x)))
    coordY = round(self.yVP + (self.heightVP/2 * (1+y)))
    print(coordX, coordY)
    self.framebuffer[coordX][coordY] = self.color

  def point(self, x, y):
     self.framebuffer[x][y] = self.color

  def glColor(self, r, g , b):
    self.color = bytes([int(b*255), int(g*255), int(r*255)])

  def glFinish(self, filename):
    f = open(filename, 'bw')


    #file header
    f.write(char('B'))
    f.write(char('M'))
    f.write(dword(14 + 40 + self.width * self.height * 3))
    f.write(dword(0))
    f.write(dword(14 + 40))

    #image header
    f.write(dword(40))
    f.write(dword(self.width))
    f.write(dword(self.height))
    f.write(word(1))
    f.write(word(24))
    f.write(dword(0))
    f.write(dword(self.width * self.height * 3))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))

    #pixel data

    for x in range(self.width):
      for y in range(self.height):
        f.write(self.framebuffer[y][x])

    f.close()

  def glLoad(self, filename='default.obj'):
    model = Obj(filename)

    for face in model.faces:
      vcount = len(face)
      for j in range(vcount):
        vi1 = face[j][0] - 1
        vi2 = face[(j + 1) % vcount][0] - 1

        v1 = model.vertices[vi1]
        v2 = model.vertices[vi2]

        self.glLine(v1[0],v2[0],v1[1],v2[1])

  def glLine(self, x0, y0, x1, y1):

    dy = abs(y1-y0)
    dx = abs(x1-x0)

    steep = dy > dx
    if steep:
      x0, y0 = y0, x0
      x1, y1 = y1, x1

    if x0 > x1:
      x0, x1 = x1, x0
      y0, y1 = y1, y0

    dy = abs(y1-y0)
    dx = abs(x1-x0)

    offset = 0
    threshold = dx

    y = y0
    x0 = int(x0)
    x1 = int(x1)

    inc = 1 if y1 > y0 else -1
    for x in range(x0, x1 + 1,):
      x = x
      # print(x, y)
      if steep:
        self.point(y, x)
      else:
        self.point(x, y)

      offset += dy * 2
      if offset >= threshold:
        y += inc
        threshold += 2*dx


#Basado en el algoritmo de https://es.wikipedia.org/wiki/Regla_par-impar
#Sin embargo se modificó para notar que se comprendió lo que hace, ya que en vez de calcular la x de la línea
#entre los dos vertices elegidos se dicidió calcular la y modificando la ecuación en coordY
#Además de que en vez de ser un booleano se entiendo que si es un número par de veces está fuera e impar dentro
  def fill(self, vertices):
    vertX=[]
    vertY=[]

    for vert in vertices:
      vertX.append(vert[0])
      vertY.append(vert[1])

    Xmax = max(vertX)
    Xmin = min(vertX)
    Ymax = max(vertY)
    Ymin = min(vertY) 
    length=len(vertX)


    for y in range(Ymin, Ymax):
      for x in range(Xmin, Xmax):
        num = len(vertices)
        j = num - 1
        paint = 0
        for i in range(num):
          x0=vertices[j][0]
          y0=vertices[j][1]
          x1=vertices[i][0]
          y1=vertices[i][1]

          between = ((x1 > x) != (x0 > x))
          if  between:
            coordY = (y0 - y1) * (x - x1) / (x0 - x1) + y1
            if y < coordY:
              paint +=1
          j = i
        if (paint%2) == 1:
          self.point(x,y)

bitmap = Render()

bitmap.glCreateWindow(1000, 1000)
bitmap.glClearColor(0,0,0)
bitmap.glClear()
bitmap.glViewPort(0,0,1000,1000)

#Poligono 1 azul
bitmap.glColor(0,0,1)
bitmap.fill([(165, 380), (185, 360), (180, 330), (207, 345), (233, 330), (230, 360), (250, 380), (220, 385), (205, 410), (193, 383)])
#Poligono 2 verde
bitmap.glColor(0,1,0)
bitmap.fill([(321,335),(288,286),(339,251),(374,302)])
# Poligono 3 morado
bitmap.glColor(1,0,1)
bitmap.fill([(377,249),(411,197),(436,249)])
# Poligono 4 color rojo
bitmap.glColor(1,0,0)
bitmap.fill([(413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37), (660, 52),
(750, 145), (761, 179), (672, 192), (659, 214), (615, 214), (632, 230), (580, 230),
(597, 215), (552, 214), (517, 144), (466, 180)])
#Poligono 5 color blanco
bitmap.glColor(1,1,1)
bitmap.fill([(682, 175), (708, 120), (735, 148), (739, 170)])


bitmap.glFinish('out.bmp')