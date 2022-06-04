import pygame
from random import randint
#default settings
pygame.init()
win = pygame.display.set_mode((600,600))
pygame.display.set_caption("Special Relativity Simulation")
screenWidth = 600
screenHeight = 600
blue = (0,0,255)
green = (0,255,0)
darkCyan = (0,139,139)
seaGreen = (32,178,170)
red = (255,0,0)
tomato = (255,99,71)
purple = (128,0,128)
darkOrchid = (153,50,204)
brown = (139,69,19)
chocolate = (210,105,30)
yellow = (255,255,0)
white = (255,255,255)
black = (0,0,0)
myFont = pygame.font.SysFont("Ariel",24)
otherFont = pygame.font.SysFont("Ariel",18)
reset = myFont.render("Reset", 1, white)
sta = myFont.render("Start", 1, white)
withText = myFont.render("With",1,white)
withoutText = otherFont.render("Without", 1, white)
linesText = myFont.render("lines", 1, white)
third = myFont.render("1/3 C", 1, white)
half = myFont.render("1/2 C", 1, white)
options = myFont.render("Options:", 1, white)
t = 0
choice1 = 'with'
start = False
running = True
class Point:
    def __init__(self,x,y,type,velocity):
        self.x = x
        self.y = y
        self.type = type  #light=0, tPrime=1, xPrime=2, myPerspective=3, events=4
        self.velocity = velocity
        self.px = 350+25*self.x
        self.py = 400-25*self.y
        self.lorentz = 1/(1-velocity**2)**0.5
        self.finalDestinationX = self.lorentz * (self.x - self.velocity * self.y)
        self.finalDestinationY = self.lorentz * (self.y - self.velocity * self.x)
        self.vX = self.px - (350+25*self.finalDestinationX)
        self.vY = self.py - (400-25*self.finalDestinationY)
    def change(self,t):
            self.px = (350+25*self.x)-self.vX*t
            self.py = (400-25*self.y)-self.vY*t
    def getPx(self):
        return int(self.px)
    def getPy(self):
        return int(self.py)

##simulation parameters##
velocity = 0.5 #relativity to light also called beta
light = []
for i in range(0,7):
  light.append(Point(i,i,0,velocity)) #x and y cordinates and type
tPrime = []
for w in range(0,7):
    tPrime.append(Point(w,(1/velocity)*w,1,velocity))
xPrime = []
for y in range(0,7):
    xPrime.append(Point(y,velocity*y,2,velocity))
myPerspective = []
for x in range(0,7):
    myPerspective.append(Point(0,x,3,velocity))
events = []
events.append(Point(4,5,4,velocity)) #the simple example of event
for z in range(0,3):
    events.append(Point(randint(2,5),randint(2,5),4,velocity))

#Auxiliary operations#
def unit(pj,type):
    if type=='x':
        return (pj-350)*0.04
    if type=='y':
        return (400-pj)*0.04
def pixel(h,type):
    if type=='x':
        return 350+25*h
    if type=='y':
        return 400-25*h
def dashedLines(a,b,vel):
    m1 = 1/vel
    xD = (m1*(m1*a-b))/(m1**2-1)
    yD = m1*xD-m1*a+b
    xC = (b*m1-a)/(m1**2-1)
    yC = (1/m1)*xC-(1/m1)*a+b
    pygame.draw.line(win, red,(pixel(a,'x'),pixel(b,'y')),(pixel(xD,'x'),pixel(yD,'y')),2)
    pygame.draw.line(win, red, (pixel(a, 'x'), pixel(b, 'y')), (pixel(xC, 'x'), pixel(yC, 'y')), 2)
    pygame.draw.line(win, red, (pixel(a, 'x'), pixel(b, 'y')), (pixel(a, 'x'), pixel(0, 'y')), 2)
    pygame.draw.line(win, red, (pixel(a, 'x'), pixel(b, 'y')), (pixel(0, 'x'), pixel(b, 'y')), 2)
def movingLine(l):
    lentgh=len(l)
    if l[0].type==0:
        color=yellow
    if l[0].type==1 or l[0].type==2:
        color=blue
    if l[0].type==3:
        color=green
    for f in range(lentgh-1):
        pygame.draw.line(win, color, (l[f].getPx(),l[f].getPy()), (l[f+1].getPx(),l[f+1].getPy()), 5)
        f+=1
def coordinateSystem():
    pygame.draw.line(win, white, (100, 0),(100,screenHeight), 4)
    pygame.draw.line(win, white, (350, 30), (350, screenHeight-30), 2) #y axis
    pygame.draw.line(win, white, (100+30, 300+100), (screenWidth-30, 300+100), 2) #x axis
    pygame.draw.line(win, white, (350, 30), (360, 40), 2) # y axis arrow
    pygame.draw.line(win, white, (350, 30), (340, 40), 2) # |-|
    pygame.draw.line(win, white, (560, 410), (570, 400), 2) # x axis arrow
    pygame.draw.line(win, white, (560, 390), (570, 400), 2) # |-|
    myFont = pygame.font.SysFont("Ariel", 20)
    t = myFont.render("T(s)", 1, (255, 255, 255))
    win.blit(t, (360, 20))
    x = myFont.render("X(3*10^8m)", 1, (255, 255, 255))
    win.blit(x, (525, 420))
    px=150
    for i in range(1,18):
        pygame.draw.line(win, white, (px,405), (px,395),1)
        px+=25
    py=50
    for i in range(1,22):
        pygame.draw.line(win, white, (345,py), (355,py),1)
        py+=25

###main loop###
while running:
    pygame.time.delay(10)
    win.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if (20 + 50 > mouse[0] > 20) and (50 + 50 > mouse[1] > 50):
                t = 0
                start = False
            if 20 + 50 > mouse[0] > 20 and 150 + 50 > mouse[1] > 150:
                start= True
            if 20 + 50 > mouse[0] > 20 and 250 + 50 > mouse[1] > 250:
                if choice1=='with':
                    choice1='without'
                else:
                    choice1='with'
            if 20 + 50 > mouse[0] > 20 and 350 + 50 > mouse[1] > 350:
                start = False
                t=0
                velocity = 1/3
                light.clear()
                tPrime.clear()
                xPrime.clear()
                myPerspective.clear()
                events.clear()
                for i in range(0, 7):
                    light.append(Point(i, i, 0, velocity))  # x and y cordinates and type
                for w in range(0, 5):
                    tPrime.append(Point(w, (1 / velocity) * w, 1, velocity))
                for y in range(0, 5):
                    xPrime.append(Point(y,velocity*y, 2, velocity))
                for x in range(0, 7):
                    myPerspective.append(Point(0, x, 3, velocity))
                events.append(Point(4, 4, 4, velocity))  # the simple example of event for specific velocity
                for z in range(0, 3):
                    events.append(Point(randint(2, 4), randint(2, 4), 4, velocity))
            if 20 + 50 > mouse[0] > 20 and 450 + 50 > mouse[1] > 450:
                start = False
                t=0
                velocity = 0.5
                light.clear()
                tPrime.clear()
                xPrime.clear()
                myPerspective.clear()
                events.clear()
                for i in range(0, 7):
                    light.append(Point(i, i, 0, velocity))  # x and y cordinates and type
                for w in range(0, 7):
                    tPrime.append(Point(w, (1 / velocity) * w, 1, velocity))
                for y in range(0, 7):
                    xPrime.append(Point(y,velocity*y, 2, velocity))
                for x in range(0, 7):
                    myPerspective.append(Point(0, x, 3, velocity))
                events.append(Point(4, 5, 4, velocity))  # the simple example of event for specific velocity
                for z in range(0, 3):
                    events.append(Point(randint(2, 4), randint(2, 4), 4, velocity))
    mouse = pygame.mouse.get_pos() #0 for x value 1 for y value
    if 20 + 50 > mouse[0] > 20 and 50 + 50 > mouse[1] > 50:
        pygame.draw.rect(win, tomato, (20, 50, 50, 50))
    else:
        pygame.draw.rect(win, red, (20, 50, 50, 50))
    if 20+50>mouse[0]>20 and 150+50>mouse[1]>150:
        pygame.draw.rect(win,seaGreen,(20,150,50,50))
    else:
        pygame.draw.rect(win, darkCyan, (20, 150, 50, 50))
    if 20+50>mouse[0]>20 and 250+50>mouse[1]>250:
        pygame.draw.rect(win,darkOrchid,(20,250,50,50))
    else:
        pygame.draw.rect(win, purple, (20, 250, 50, 50))
    if 20+50>mouse[0]>20 and 350+50>mouse[1]>350:
        pygame.draw.rect(win,chocolate,(20,350,50,50))
    else:
        pygame.draw.rect(win,brown,(20, 350, 50, 50))
    if 20+50>mouse[0]>20 and 450+50>mouse[1]>450:
        pygame.draw.rect(win,chocolate,(20,450,50,50))
    else:
        pygame.draw.rect(win,brown,(20, 450, 50, 50))
    if start:
        if t<1:
            t+=0.004
    if t<1:
        for i in range(len(light)):
            light[i].change(t)
        for i in range(len(tPrime)):
            tPrime[i].change(t)
        for i in range(len(xPrime)):
            xPrime[i].change(t)
        for i in range(len(myPerspective)):
            myPerspective[i].change(t)
        for i in range(len(events)):
            events[i].change(t)
    coordinateSystem()
    if choice1=='with':
        movingLine(light)
        movingLine(tPrime)
        movingLine(xPrime)
        movingLine(myPerspective)
    for i in range(len(light)):
        pygame.draw.circle(win, yellow, (int(light[i].getPx()), int(light[i].getPy())), 6)
    for i in range(len(events)):
        pygame.draw.circle(win, red, (events[i].getPx(), events[i].getPy()), 6)
    for i in range(len(tPrime)):
        pygame.draw.circle(win, blue, (tPrime[i].getPx(), tPrime[i].getPy()), 6)
    for i in range(len(xPrime)):
        pygame.draw.circle(win, blue, (xPrime[i].getPx(), xPrime[i].getPy()), 6)
    for i in range(len(myPerspective)):
        pygame.draw.circle(win, green, (myPerspective[i].getPx(), myPerspective[i].getPy()), 6)
    if t==0 and choice1=='with':
      dashedLines(events[0].x,events[0].y,velocity)
    if t >0.995 and choice1=='with':
      pygame.draw.line(win, red, (events[0].getPx(), events[0].getPy()), (pixel(0, 'x'), events[0].getPy()), 2)
      pygame.draw.line(win, red, (events[0].getPx(), events[0].getPy()), (events[0].getPx(), pixel(0,'y')), 2)
    win.blit(reset, (25, 70))
    win.blit(sta, (25, 170))
    if choice1=='with':
        win.blit(withoutText,(23,260))
    else:
        win.blit(withText, (27, 260))
    win.blit(linesText, (28, 280))
    win.blit(third,(25,370))
    win.blit(half,(25,470))
    lol = str(round(velocity,2))
    lorent = myFont.render(("Lorentz factor: %3.2f" % light[0].lorentz), 1, white)
    speed = myFont.render(("Velocity: %.2f" % velocity), 1, white)
    c = myFont.render(("C"), 1, white)
    win.blit(speed,(120,40))
    win.blit(c,(227,40))
    win.blit(lorent,(120, 80))
    win.blit(options,(15,20))
    pygame.display.update()
pygame.quit()