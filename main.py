#!/usr/bin/python
#Import some libraries and bullshit
import pygame, sys, math, pyganim
from pygame.locals import *

#Set some constants
BLACK = (0,0,0)
WHITE = (255,255,255)
FPS=30 
GRAVITY=1

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
  

def key_pressed(key):
  keysPressed = pygame.key.get_pressed()
  if keysPressed[key]:
    return True
  else:
    return False

class Player(pygame.sprite.Sprite):
  def __init__(self, x, y):
    super(Player, self).__init__()
    self.runningAnim = animList[0]
    self.going_left = True
    self.standing = False
    self.runningAnim.play()

    self.rect = self.runningAnim.getRect()
    self.rect.x = x
    self.rect.y = y
    self.scan_rect = self.rect.copy()

    self.max_speed = 10
    self.jump_accel = -15
    self.dx = 0
    self.dy = 0
    self.dvx= 0
    self.dvy= 0

  def check_falling(self):
    test_rect = self.rect.copy()
    test_rect.y += 2
    if len(test_rect.collidelistall(wall_rect_list)) == 0:
      self.standing = False
    else:
      self.standing = True
      self.dvy = 0
      self.dy = 0
  
  def calculate_gravity(self):
    test_rect = self.rect.copy()
    test_rect.y += self.dy
    block_hit_list = test_rect.collidelistall(wall_rect_list)
    if len(block_hit_list) == 0:
      self.dvy = GRAVITY
      self.standing = False
    else:
      highest_top = 10000
      for block_index in block_hit_list:
        current_top = wall_rect_list[block_index].top  
        if current_top < highest_top:
          highest_top = current_top 
      self.rect.bottom = highest_top - 1
      self.dvy = 0
      self.dy = 0
      self.standing = True

  def calculate_collide(self):
    test_rect = self.rect.copy()
    test_rect.y = self.rect.y
    test_rect.x += self.dx
    block_hit_list = test_rect.collidelistall(wall_rect_list)
    if len(block_hit_list) > 0:
      for block_index in block_hit_list:
        if self.going_left == True:
          furthest_right = -100
          current_right = wall_rect_list[block_index].right
          if current_right > furthest_right:
            furthest_right = current_right
          self.rect.left = furthest_right + 1
          self.dvx = 0
          self.dx = 0
        elif self.going_left == False:
          furthest_left = 10000
          current_left = wall_rect_list[block_index].left
          if current_left < furthest_left:
            furthest_left = current_left
          self.rect.right = furthest_left -1
          self.dvx = 0
          self.dx = 0

  def jump(self):
    self.dvy = self.jump_accel
    self.standing = False

  def update(self):
    self.check_falling()
    if self.standing == False:
      self.calculate_gravity()
    self.calculate_collide()

    if self.standing == True:
      if (key_pressed(K_w)):
        self.jump()

    if key_pressed(K_a) == True:
      if (self.dx > -self.max_speed):
        self.dvx = -1 
      else:
        self.dvx = 0
      if self.going_left == False:
        self.runningAnim.flip(True, False)
      self.going_left = True

    if key_pressed(K_d) == True:
      if (self.dx < self.max_speed):
        self.dvx = 1  
      else:  
        self.dvx = 0
      if self.going_left == True:
        self.runningAnim.flip(True, False)
      self.going_left = False
 
    if (not key_pressed(K_d)) and (not key_pressed(K_a)):
      self.dvx = 0
      self.dx = 0

    self.dx += self.dvx
    self.rect.x += self.dx

    self.dy += self.dvy
    self.rect.y += self.dy
    
 
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

wall = Wall(0, 390, 500, 100)
wall2 = Wall(0, 290, 30, 100)
wall3 = Wall(200, 290, 30, 100)
wall_list.add(wall)
wall_list.add(wall2)
wall_list.add(wall3)
all_sprite_list.add(wall)
all_sprite_list.add(wall2)
all_sprite_list.add(wall3)

for wall in wall_list:
  wall_rect_list.append(wall.rect)

player = Player(200, 50)
#player.walls = wall_list
all_sprite_list.add(player)

#block_hit_list = []
#Setup the event loop and set the screen background
while True:
  for event in pygame.event.get():
    if event.type == QUIT or key_pressed(K_q):
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
