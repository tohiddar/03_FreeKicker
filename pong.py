import pygame, math, sys
from sys import exit
from random import randint, choice
import random

class Ball(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		ball_image=pygame.image.load('graphics/bullet.png').convert_alpha()
		# Set the size for the image
		DEFAULT_IMAGE_SIZE = (8, 8)
		ball_image = pygame.transform.scale(ball_image, DEFAULT_IMAGE_SIZE)
		self.image = ball_image
		self.rect = self.image.get_rect(midtop = (400,200))
		self.speed=3
#		self.xfactor = random.uniform(-1,1)
		self.xfactor = -0.6
		self.ysign = math.copysign(1, random.uniform(-1,1))
		self.yfactor = math.sqrt(1-math.pow(self.xfactor,2))*self.ysign
		self.collision_num=0

	def change_dir(self):
		if self.rect.y > 300 or self.rect.y < 0:
			self.yfactor = -self.yfactor
		if self.collision_num == 1:
			print(self.xfactor)
			self.xfactor=-self.xfactor

	def update(self,collision_state):
		self.collision_num = collision_state
		self.change_dir()
		self.rect.x += self.xfactor*self.speed
		self.rect.y += self.yfactor*self.speed

class Racket(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()
		racket_image=pygame.image.load('graphics/bullet.png').convert_alpha()
		DEFAULT_IMAGE_SIZE = (6, 45)
		racket_image = pygame.transform.scale(racket_image, DEFAULT_IMAGE_SIZE)
		self.image = racket_image
		self.speed=3
		self.type=type
		self.ballypos=ball_group.sprites()[0].rect.y
		if type == 'player':
			self.rect = self.image.get_rect(midbottom = (200,180))
		elif type == 'ai':
			self.rect = self.image.get_rect(midbottom = (600,180))

	def player_input(self):
		if self.type == 'player':
			keys = pygame.key.get_pressed()
			if keys[pygame.K_UP] and self.rect.top > 0:
				self.rect.y -= self.speed
			elif keys[pygame.K_DOWN] and self.rect.bottom < 400:
				self.rect.y += self.speed
		elif self.type == 'ai':
			self.move_towards_ball()

	def move_towards_ball(self):
		self.ballypos = ball_group.sprites()[0].rect.y
		deltay = self.ballypos - self.rect.midleft[1]
		dysign = math.copysign(1, deltay)
		if self.rect.y < 308 and self.rect.y > -50:
			self.rect.y += self.speed*dysign

	def update(self,type):
		self.type = type
		self.player_input()

def display_score():
#	current_time = int(pygame.time.get_ticks() / 1000) - start_time
#	score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
#	score_rect = score_surf.get_rect(center = (400,50))
#	screen.blit(score_surf,score_rect)
	current_time = globalx
	score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
	score_rect = score_surf.get_rect(center = (400,50))
	screen.blit(score_surf,score_rect)
	return current_time

def collision_sprite():
	if pygame.sprite.groupcollide(racket,ball_group,False,False):
		return 1
	else:
		return 0

def clip(surface, x, y, x_size, y_size): #Get a part of the image
    handle_surface = surface.copy() #Sprite that will get process later
    clipRect = pygame.Rect(x,y,x_size,y_size) #Part of the image
    handle_surface.set_clip(clipRect) #Clip or you can call cropped
    image = surface.subsurface(handle_surface.get_clip()) #Get subsurface
    return image.copy() #Return

def divisible_by(x, y):
    if (x % y) == 0:
        return True
    else:
        return False

def time_increment(now,then,dt):
	if now-then>=dt:
		then=now
		return True, then
	else:
		return False, then

pygame.init()
FrameHeight = 400
FrameWidth = 800
globalx=0;globaly=0
screen = pygame.display.set_mode((FrameWidth,FrameHeight))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops = -1)

ball_group = pygame.sprite.Group()
ball_group.add(Ball())

#Groups
racket = pygame.sprite.Group()
racket.add(Racket('player',))
racket.add(Racket('ai',))


sky_surface = pygame.image.load('graphics/Sky.png').convert()
DEFAULT_IMAGE_SIZE = (FrameWidth, FrameHeight)
sky_surface = pygame.transform.scale(sky_surface, DEFAULT_IMAGE_SIZE)
ground_surface = pygame.image.load('graphics/ground.png').convert()
heart_surface = pygame.image.load('graphics/heart.png').convert_alpha()

# Intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
#player_stand = pygame.image.load('graphics/mama.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Pong!',False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('Press space to run',False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,330))

# Timer 
#obstacle_timer = pygame.USEREVENT + 1
#pygame.time.set_timer(obstacle_timer,1500)

now = pygame.time.get_ticks()
then=now

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if game_active:
			i=1
#			print(game_active)

		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True
				start_time = int(pygame.time.get_ticks() / 1000)

	if game_active:
		screen.blit(sky_surface, (0, 0))
		pygame.draw.line(screen, (0, 0, 0), (0, 308), (1000, 308),width=2)
		collision_state = collision_sprite()

		ball_group.draw(screen)
		ball_group.update(collision_state)

		racket.draw(screen)
#		racket.update('player')
		racket.sprites()[0].update('player')
		racket.sprites()[1].update('ai')

	else:
		screen.fill((94,129,162))
		screen.blit(player_stand,player_stand_rect)

		score_message = test_font.render(f'Your score: {score}',False,(111,196,169))
		score_message_rect = score_message.get_rect(center = (400,330))
		screen.blit(game_name,game_name_rect)

		if score == 0: screen.blit(game_message,game_message_rect)
		else: screen.blit(score_message,score_message_rect)

	pygame.display.update()
	clock.tick(60)