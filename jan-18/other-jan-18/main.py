import pygame
import math
import random
def dst(a,b,c,d):
    return math.hypot(c - a, d - b)
class trace:
    def __init__(self,pos,mov,color=None):
        self.pos = list(pos)
        mov = [math.cos(mov),math.sin(mov)]
        self.omov = mov
        self.mov = self.omov
        self.oldturn = 0
        if color == None:
            self.color = [random.randrange(255) for i in range(3)]
        else:
            self.color = color
        self.whatin = [False for i in speedmap]
        self.lastin = [False for i in speedmap]
        self.leng = 0
    def move(self):
        self.prevpos = self.pos
        self.pos[0] += self.mov[0]
        self.pos[1] += self.mov[1]
        self.leng += 1
    def isonscreen(self):
        mx = int(self.pos[0]) > 0
        my = int(self.pos[1]) > 0
        px = int(self.pos[0]) < screensize[0]
        py = int(self.pos[1]) < screensize[1]
        self.onscreen = mx and my and px and py
        return self.onscreen
    def detect(self):
        #self.intpos = [int(self.pos[0]),int(self.pos[1])]
        for i in range(len(speedmap)):
            x1 = self.pos[0]
            y1 = self.pos[1]
            x2 = speedmap[i][0]
            y2 = speedmap[i][1]
            dist = speedmap[i][2]
            if dst(x1,y1,x2,y2) < dist:
                self.whatin[i] = True
            else:
                self.whatin[i] = False
        for pl,i in enumerate(self.whatin):
            if i != self.lastin[pl]:
                whtd = speedmap[pl][3]
                self.mov = [0,0]
            self.lastin[pl] = self.whatin[pl]
        if max(self.whatin) > 0:
            self.move()
    def update(self):
        if self.isonscreen():
            self.move()
            self.render()
            self.detect()
    def render(self):
        pygame.draw.line(screen,self.color,self.pos,self.prevpos)
random.seed(0)
pygame.init()
screensize = (800,800)
screen = pygame.display.set_mode(screensize)
traces = []
raycount = 2000
speedmap = []
for x in range(4):
    x = x * 200 + 100
    for y in range(4):
        y = y * 200 + 100
        rc = random.choice(['block','reflect'])
        speedmap += [[x,y,50,rc]]
running = True
op = [400,400]
_t = []
for at2 in range(0,360):
    _t.append(trace(op,at2*math.pi/180,color=[255]*3))
while running:
    pygame.event.get()
    #screen.fill((0,0,0))
    mpos = pygame.mouse.get_pos()
    for i in range(500):
        for i in range(len(_t)):
            _t[i].update()
    for circ in speedmap:
        pl = (circ[0]-circ[2],circ[1]-circ[2],circ[2]*2,circ[2]*2)
        pygame.draw.ellipse(screen,(255,255,255),pl,1)
    pygame.display.flip()
