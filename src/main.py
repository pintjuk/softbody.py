MAX_FPS = 200

import math
import pygame
from functools import reduce
import uuid

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
LEFT = 1
enteties = []
DRAG = 1.2
GRAVITY = 300

FLOR = 30

class SpreadForce:
    def __init__(self, _enteties, strength):
        enteties.append(self)
        self.enteties = _enteties
        self.strength = strength
        print("AOEU")

    def update(self, dt, mouse_bttns, mouse_pos):
        print("update")
        # calculate center of gravity
        center = pygame.Vector2(0, 0)
        for entity in self.enteties:
            center += entity.pos * entity.mass

        center /= len(self.enteties)


        for entity in self.enteties:
            try :
                direction = (center - entity.pos).normalize()
            except:
                direction = pygame.Vector2(0,0)

            entity.forces.append(direction* -self.strength)
        

class Circle:
    __slots__ = ["pos", "radius", "color", "vel", "forces", "drag", "mass", "id"]

    def __init__(self, pos, radius, color, vel=pygame.Vector2(0, 0), mass=1):
        self.pos = pos
        self.radius = radius
        self.color = color
        self.vel = vel
        self.forces = []
        self.drag = False
        self.mass = mass
        self.id = uuid.uuid4()
        enteties.append(self)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)

    def overlaps(self, pos):
        return (self.pos - pos).length() < self.radius

    def event_mousedown(self, button, pos):
        if button == LEFT:
            pos = pygame.Vector2(pos[0], pos[1])
            if self.overlaps(pos):
                self.drag = True
                self.color = "green"
                self.pos = pos

    def event_mouseup(self, button, pos):
        if button == LEFT:
            self.drag = False
            self.color = "red"

    def update(self, dt, mouse_bttns, mouse_pos):
        if mouse_bttns[LEFT - 1]:
            if self.drag:
                self.pos = pygame.Vector2(mouse_pos[0], mouse_pos[1])

    def update_physics(self, dt):
        if self.drag:
            self.forces = []
            self.vel = pygame.Vector2(0, 0)
            return

        self.forces.append(pygame.Vector2(0, GRAVITY) * self.mass)
        acc = reduce(lambda a, b: a + b, self.forces, pygame.Vector2(0, 0)) / self.mass

        self.vel = (acc * dt) + self.vel - (self.vel * DRAG * dt)
        self.pos += self.vel * dt
        self.forces = []

    def get_pos(self):
        return self.pos


class Line:
    def __init__(self, start, end, color="green", stiffness=1000):
        self.start = start
        self.end = end
        self.color = color
        self.len = (self.start.pos - self.end.pos).length()
        if self.len == 0:
            self.len = 0.1
        self.stiffness = stiffness
        self.max_force = 14000
        enteties.append(self)

    def draw(self, screen):
        if hasattr(self.start, "pos"):
            start = self.start.pos

        if hasattr(self.end, "pos"):
            end = self.end.pos

        pygame.draw.line(screen, self.color, start, end, 5)

    def update(self, dt, mouse_bttns, mouse_pos):
        len = (self.start.pos - self.end.pos).length()
        f = -(len - self.len) * self.stiffness
        # if abs(f) > self.max_force:
        #     f = self.max_force if f > 0 else -self.max_force

        if self.start.pos == self.end.pos:
            self.start.pos += pygame.Vector2(0.1, 0.1)
        direction = (self.start.pos - self.end.pos).normalize()

        self.start.forces.append((self.start.pos - self.end.pos).normalize() * f)
        self.end.forces.append((self.end.pos - self.start.pos).normalize() * f)


def circle(num=5):

    circles = []
    p0=pygame.Vector2(100, 100)

    for i in range(num):
        circles.append(Circle(
            pos=p0 + pygame.Vector2(math.sin(i*math.pi*2/num)*100, math.cos(i*math.pi*2/num)*100),
            radius=5,
            color="red",
            mass=1,
        ))

    for i in range(num):
        Line(circles[i], circles[(i + 1) % num], stiffness=1000)
        

    SpreadForce(circles, 5000)

circle(200)

def create_tringale_with_rope():
    c1 = Circle(
        pos=pygame.Vector2(100, 100),
        radius=15,
        color="red",
        mass=10,
    )
    c2 = Circle(
        pos=pygame.Vector2(200, 200),
        radius=15,
        color="red",
        mass=10,
    )
    c3 = Circle(
        pos=pygame.Vector2(200, 100),
        radius=15,
        color="red",
        mass=10,
    )
    l1 = Line(
        start=c1,
        end=c2,
        color="green",
    )

    l2 = Line(
        start=c2,
        end=c3,
        color="green",
    )

    l3 = Line(
        start=c3,
        end=c1,
        color="green",
    )

    s1 = Circle(
        pos=pygame.Vector2(200, 120),
        radius=2,
        color="pink",
    )
    Line(s1, c3)
    spriv = s1

    num = 15
    for i in range(num):
        i1 = Circle(
            pos=pygame.Vector2(200, 140 + i * 20),
            radius=2 if i != num - 1 else 20,
            mass=1 if i != num - 1 else 20,
            color="pink",
        )
        Line(spriv, i1)
        spriv = i1
#create_tringale_with_rope()

def create_cloth(num=3, spacing=50):
    start= pygame.Vector2(200, 100)

    cash = []

    def c(x, y):
        return cash[(num*x)+y]


    for y in range(num+1):
        for x in range(num+1):
            cash.append(None)

    for y in range(num):
        line = []
        for x in range(num):
            i1 = Circle(
                pos=start+pygame.Vector2(x*spacing, y* spacing),
                radius=5,
                mass=1,
                color="pink",
            )

            cash[(num*x)+y] = i1

    for y in range(num):

        line = []
        for x in range(num):
            if x>0:
                Line(cash[(num*x)+y], cash[(num*(x-1))+y])

            if y>0:
                Line(cash[(num*x)+y], cash[(num*(x))+(y-1)])

            # if x%2==y%2:
            #     if x<num-1 and y<num-1:
            #         Line(cash[(num*x)+y], cash[(num*(x+1))+(y+1)])
            #     if x>0 and y<num-1:
            #         Line(cash[(num*x)+y], cash[(num*(x-1))+(y+1)])

    SpreadForce([ c for c in cash if c], 1000)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for entity in enteties:
                if hasattr(entity, "event_mousedown"):
                    entity.event_mousedown(event.button, event.pos)

        if event.type == pygame.MOUSEBUTTONUP:
            for entity in enteties:
                if hasattr(entity, "event_mouseup"):
                    entity.event_mouseup(event.button, event.pos)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    color = "black"

    pygame.draw.rect(
        screen,
        color,
        pygame.Rect(0, screen.get_height() - FLOR, screen.get_width(), FLOR),
    )

    for entity in enteties:
        if hasattr(entity, "draw"):
            entity.draw(screen)

    for entity in enteties:
        if hasattr(entity, "update"):
            entity.update(dt, pygame.mouse.get_pressed(), pygame.mouse.get_pos())

    for entity in enteties:
        if hasattr(entity, "pos"):
            if (entity.pos[1] > screen.get_height() - FLOR - entity.radius) and (
                not entity.drag
            ):
                entity.pos = pygame.Vector2(
                    entity.pos[0], screen.get_height() - FLOR - entity.radius
                )

                # entity.vel = pygame.Vector2(entity.vel[0], entity.vel[1] * -0.)
                entity.vel = pygame.Vector2(0,0)

    for entity in enteties:
        if hasattr(entity, "update_physics"):
            entity.update_physics(dt)

    # RENDER YOUR GAME HERE

    pygame.display.flip()

    dt = clock.tick(MAX_FPS) / 1000
pygame.quit()
