from math import sqrt
from field import Field
import pygame
import pygame.display
from random import randrange

class Object:
    def __init__(self, x, y, width, height, color, is_creature):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.is_creature = is_creature
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    def update(self, dt, events, objects):
        pass

class Creature(Object):
    def __init__(self, x, y, color, speed):
        super().__init__(x, y, 8, 8, color, True)
        self.speed = speed
    def move(self, dx, dy, objects):
        if abs(dx) < 0.001 and abs(dy) < 0.001: return
        new_x = self.x+dx
        new_y = self.y+dy
        move = True
        for object in objects:
            if object is self: continue
            if  object.x < new_x+self.width \
            and new_x < object.x+object.width \
            and object.y < new_y+self.height \
            and new_y < object.y+object.height:
                if object.is_creature:
                    object.move(dx/2, dy/2, objects)
                    # self.move(dx/4, dy/4, objects)
                move = False
        if move:
            self.x = new_x
            self.y = new_y

class Player(Creature):
    def __init__(self, x, y):
        super().__init__(x, y, (64, 64, 192), 64)
    def update(self, dt, events, objects):
        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_d]-keys[pygame.K_a]
        dy = keys[pygame.K_s]-keys[pygame.K_w]
        vel_x = dx*self.speed*dt
        vel_y = dy*self.speed*dt
        self.move(vel_x, 0, objects)
        self.move(0, vel_y, objects)

class Enemy(Creature):
    def __init__(self, x, y, color=(192, 64, 64), speed=48):
        super().__init__(x, y, color, speed)
        self.field = None
    def set_field(self, field):
        self.field = field
    def update(self, dt, events, objects):
        if self.field is not None:
            vel_x = 0
            vel_y = 0
            for dx in range(2):
                for dy in range(2):
                    dir_x, dir_y = self.field.get_dir((self.x+self.width*dx)//10, (self.y+self.height*dy)//10)
                    vel_x += dir_x
                    vel_y += dir_y
            length = sqrt(vel_x**2+vel_y**2)
            if length != 0:
                vel_x /= length
                vel_y /= length
            vel_x *= dt*self.speed
            vel_y *= dt*self.speed
            self.move(vel_x, 0, objects)
            self.move(0, vel_y, objects)

class Wall(Object):
    def __init__(self, x, y):
        super().__init__(x, y, 10, 10, (64, 64, 64), False)

class Game:
    def __init__(self):
        self.height = 64
        self.width = 36
        self.objects = [
            Player(80, 80),
            *[Enemy(5+i*11, 2+21*i) for i in range(5)],
            *[Enemy(16+i*11, 2, (64, 192, 64), 32) for i in range(8)],
            *[Enemy(5, 23+i*11, (64, 192, 192), 40) for i in range(8)],
        ]
        map = [[0 for y in range(self.height)] for x in range(self.width)]
        for i in range(100):
            x = randrange(self.width)
            y = randrange(self.height)
            if x < 10 and y < 10: continue
            if map[x][y] == 0:
                map[x][y] = 1
                self.objects.append(Wall(x*10, y*10))
        for i in range(15):
            x = 10+i
            y = 20
            if map[x][y] == 0:
                map[x][y] = 1
                self.objects.append(Wall(x*10, y*10))
            x = 10
            y = 10+i
            if map[x][y] == 0:
                map[x][y] = 1
                self.objects.append(Wall(x*10, y*10))
        self.field = Field(map)
        for object in self.objects:
            if type(object) == Enemy:
                object.set_field(self.field)
        self.running = False
        self.screen = pygame.display.set_mode((640, 360), pygame.SCALED)
    def draw(self):
        self.screen.fill((192, 192, 192))
        for object in self.objects:
            object.draw(self.screen)
        pygame.display.flip()
    def mainloop(self):
        self.running = True
        clock = pygame.time.Clock()
        while self.running:
            dt = clock.tick(60)/1000
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            player = self.objects[0]
            self.field.set_target(int(player.x//10), int(player.y//10))
            for object in self.objects:
                object.update(dt, events, self.objects)
            self.draw()
    

if __name__ == "__main__":
    game = Game()
    game.mainloop()
