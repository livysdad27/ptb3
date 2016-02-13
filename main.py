#!/usr/bin/python
#Import some libraries and bullshit
import pygame, sys, math, pyganim
from pygame.locals import *

#Set some constants
BLACK = (0,0,0)
WHITE = (255,255,255)
FPS=60
GRAVITY=2

clock = pygame.time.Clock()
pygame.init
pygame.display.init()
screen = pygame.display.set_mode((500, 400))
pygame.display.set_caption("PTB Deux")

#Define animations here
spriteParamList = [["./bob.png", 1, 11, 40]]
animList = []
for params in spriteParamList:
  images = pyganim.getImagesFromSpriteSheet(params[0], rows=params[1], cols=params[2])
  timings = [params[3]] * len(images)
  frames = list(zip(images, timings))
  anim = pyganim.PygAnimation(frames)
  animList.append(anim)
  

def keyPressed(key):
  keysPressed = pygame.key.get_pressed()
  if keysPressed[key]:
    return True
  else:
    return False

class Player(pygame.sprite.Sprite):
  def __init__(self, x, y):
    super(Player, self).__init__()
    self.runningAnim = animList[0]
    self.goingLeft = True
    self.standing = False
    self.runningAnim.play()

    self.rect = self.runningAnim.getRect()
    self.rect.x = x
    self.rect.y = y

    self.maxSpeed = 8 
    self.jumpAccel = -20
    self.dx = 0
    self.dy = 0
    self.dvx= 0
    self.dvy= 0

  def update(self):
    if (not keyPressed(K_a)) and (not keyPressed(K_d)):
      if self.dx > 0:
        self.dvx = -1
      elif self.dx < 0:
        self.dvx = 1
      elif self.dx == 0:
        self.dvx = 0

    if (keyPressed(K_a) and keyPressed(K_d)):
      self.dvx = 0
      self.dx = 0
   
    if keyPressed(K_d):
      self.dvx += 1
      if self.goingLeft:
        self.runningAnim.flip(True, False)
        self.goingLeft = False
  
    if keyPressed(K_a):
      self.dvx -= 1
      if not self.goingLeft:
        self.runningAnim.flip(True, False)
        self.goingLeft = True
    
    if keyPressed(K_w) and self.standing:
      self.dvy = self.jumpAccel 
      self.standing = False 
      

  def reconcile(self):
    #Dont exceed the speed limit
    if abs(self.dx + self.dvx) > self.maxSpeed:
      self.dvx= 0
    else:
      self.dx += self.dvx

    self.dvy += GRAVITY
    if self.standing:
      self.dy = 0
      self.dvy = 0
    else:
      self.dy = self.dvy + GRAVITY

    self.rect.left += self.dx
    for block in block_hit_list:
      if self.dx > 0:
        self.rect.right = block.rect.left
      elif self.dx < 0:
        self.rect.left = block.rect.right
      else:
        pass
     
  
    self.rect.top += self.dy
    for block in block_hit_list:
      if self.dy > 0:
        self.rect.bottom = block.rect.top
        self.dvy = 0
        self.dy= 0
        self.standing = True
      else:
        self.rect.top = block.rect.bottom
        self.dvy = 0
        self.dy= 0
    print str(self.rect.y) + "," + str(self.dy) + "," + str(self.dvy) + " , " + str(self.standing)

class Wall(pygame.sprite.Sprite):
  def __init__(self, x, y, width, height):
    super(Wall, self).__init__()
    
    self.image = pygame.Surface([width, height])
    self.image.fill(BLACK)
    self.rect = self.image.get_rect()
    self.rect.y = y
    self.rect.x = x

all_sprite_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()
wall = Wall(0, 300, 500, 100)
wall_list.add(wall)
all_sprite_list.add(wall)

player = Player(300, 50)
#player.walls = wall_list
all_sprite_list.add(player)

#Setup the event loop and set the screen background
while True:
  for event in pygame.event.get():
    if event.type == QUIT or keyPressed(K_q):
      pygame.quit()
      sys.exit()
   
  screen.fill(WHITE)

  player.update()
  block_hit_list = pygame.sprite.spritecollide(player, wall_list, False)
  player.reconcile()
  wall_list.draw(screen)
  player.runningAnim.blit(screen, (player.rect.x, player.rect.y))
  pygame.display.update()
  pygame.display.flip()
  clock.tick(FPS)
