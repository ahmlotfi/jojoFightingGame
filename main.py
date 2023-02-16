import pygame
import os
from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

#define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]#player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

WIDTH, HEIGHT = 1000, 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Haram vs Halal prince!")

victory_img = pygame.image.load("pics/victory.png").convert_alpha()

clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
TURQUOISE = (64, 224, 208)

BACKGROUND = pygame.image.load(os.path.join('pics', 'background.png')).convert_alpha()

HALAL_IMAGE = pygame.image.load(os.path.join('pics', 'halal.png'))
HARAM_IMAGE = pygame.image.load(os.path.join('pics', 'haram.png'))
HARAM_STAND = pygame.image.load(os.path.join('pics', 'standHaram.png'))
HALAL_STAND = pygame.image.load(os.path.join('pics', 'standHalal.png'))

count_font = pygame.font.Font(os.path.join('pics', 'turok.ttf'), 80)
score_font = pygame.font.Font(os.path.join('pics', 'turok.ttf'), 30)

pygame.mixer.music.load(os.path.join("pics", "music.mp3"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound(os.path.join("pics", "sword.wav"))
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound(os.path.join("pics", "magic.wav"))
magic_fx.set_volume(0.75)

WARRIOR_SIZE = 250
WARRIOR_SCALE = 3
WARRIOR_OFFSET = [20, 107]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [20, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

score = [0, 0]#player scores. [P1, P2]
ROUND_OVER_COOLDOWN = 2000



#define number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  WIN.blit(img, (x, y))

#function for drawing background
def draw_bg():
  scaled_bg = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))
  WIN.blit(scaled_bg, (0, 0))

#function for drawing fighter health bars
def draw_health_bar(health, x, y):
  ratio = health / 100
  pygame.draw.rect(WIN, WHITE, (x - 2, y - 2, 404, 34))
  pygame.draw.rect(WIN, RED, (x, y, 400, 30))
  pygame.draw.rect(WIN, YELLOW, (x, y, 400 * ratio, 30))


#create two instances of fighters
fighter_1 = Fighter(1, 200, 400, False, WARRIOR_DATA, HALAL_IMAGE, sword_fx, HALAL_STAND)
fighter_2 = Fighter(2, 700, 400, True, WIZARD_DATA, HARAM_IMAGE, magic_fx, HARAM_STAND)

#game loop
run = True
while run:

  clock.tick(FPS)

  #draw background
  draw_bg()

  #show player stats
  draw_health_bar(fighter_1.health, 20, 20)
  draw_health_bar(fighter_2.health, 580, 20)
  draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
  draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

  #update countdown
  if intro_count <= 0:
    #move fighters
    fighter_1.move(HEIGHT, WIDTH, WIN, fighter_2, round_over)
    fighter_2.move(HEIGHT, WIDTH, WIN, fighter_1, round_over)
  else:
    #display count timer
    draw_text(str(intro_count), count_font, RED, WIDTH / 2, HEIGHT / 3)
    #update count timer
    if (pygame.time.get_ticks() - last_count_update) >= 1000:
      intro_count -= 1
      last_count_update = pygame.time.get_ticks()

  #update fighters
  fighter_1.update()
  fighter_2.update()

  #draw fighters
  fighter_1.draw(WIN)
  fighter_2.draw(WIN)

  #check for player defeat
  if round_over == False:
    if fighter_1.alive == False:
      score[1] += 1
      round_over = True
      round_over_time = pygame.time.get_ticks()
    elif fighter_2.alive == False:
      score[0] += 1
      round_over = True
      round_over_time = pygame.time.get_ticks()
  else:
    #display victory image
    WIN.blit(victory_img, (360, 150))
    if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
      round_over = False
      intro_count = 3
      fighter_1 = Fighter(1, 200, 400, False, WARRIOR_DATA, HALAL_IMAGE, sword_fx, HALAL_STAND)
      fighter_2 = Fighter(2, 700, 400, True, WIZARD_DATA, HARAM_IMAGE, magic_fx, HARAM_STAND)

  #event handler
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False


  #update display
  pygame.display.update()

#exit pygame
pygame.quit()