#!/usr/bin/python
#Import some libraries and bullshit
import pygame, sys, math, pyganim
from pygame.locals import *

#Set some constants
BLACK = (0,0,0)
WHITE = (255,255,255)
FPS=10 
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
    self.scan_rect = self.rect.copy()

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
    
    self.scan_rect.x = self.rect.x + self.dvx
    self.scan_rect.y = self.rect.y + self.dvy

    self.dvy += GRAVITY
    if self.standing:
      self.dy = 0
      self.dvy = 0
    else:
      self.dy = self.dvy + GRAVITY
        
    if abs(self.dx + self.dvx) > self.maxSpeed:
      self.dvx= 0
    else:
      self.dx += self.dvx

    block_hit_list = player.scan_rect.collidelistall(wall_rect_list) 
    for block_index in block_hit_list:
      block = wall_rect_list[block_index]
      if self.dy > 0:
        self.rect.bottom = block.top
        self.dvy = 0
        self.dy= 0
        self.standing = True
      elif self.dy < 0:
        self.rect.top = block.bottom
        self.dvy = 0
        self.dy= 0
    self.rect.top += self.dy
    self.scan_rect.y = self.rect.y

    block_hit_list = player.scan_rect.collidelistall(wall_rect_list) 
    print str(block_hit_list)
    for block_index in block_hit_list:
      block = wall_rect_list[block_index]
      if self.dx > 0:
        self.rect.right = block.left
      elif self.dx < 0:
        self.rect.left = block.right

    self.rect.left += self.dx
     
class Wall(pygame.sprite.Sprite):
  def __init__(self, x, y, width, height):
    super(Wall, self).__init__()
    
    self.image = pygame.Surface([width, height])
    self.image.fill(BLACK)
    self.rect = self.image.get_rect()
    self.rect.y = y
    self.rect.x = x

wall_rect_list = []
all_sprite_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()

wall = Wall(0, 390, 500, 1)
wall2 = Wall(0, 290, 30, 100)
wall_list.add(wall)
wall_list.add(wall2)
all_sprite_list.add(wall)
all_sprite_list.add(wall2)

for wall in wall_list:
  wall_rect_list.append(wall.rect)

player = Player(300, 50)
#player.walls = wall_list
all_sprite_list.add(player)

#block_hit_list = []
#Setup the event loop and set the screen background
while True:
  for event in pygame.event.get():
    if event.type == QUIT or keyPressed(K_q):
      pygame.quit()
      sys.exit()
   
  screen.fill(WHITE)
  player.update()
  #player.reconcile()
  wall_list.draw(screen)
  player.runningAnim.blit(screen, (player.rect.x, player.rect.y))
  pygame.display.update()
  pygame.display.flip()
  clock.tick(FPS)
