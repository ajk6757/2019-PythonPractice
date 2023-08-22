import sys
import random
import pygame
from pygame.locals import QUIT, KEYDOWN,\
    K_LEFT, K_RIGHT, K_UP, K_DOWN, Rect

pygame.init()
SURFACE = pygame.display.set_mode((1200, 1200))
FPSCLOCK = pygame.time.Clock()
myfont = pygame.font.SysFont(None, 80)
bombs = pygame.image.load('1.jpg')


FOODS = []
SNAKE = []
BOMBS = []
RED = (255,0,0)
(W, H) = (20, 20)



def add_food():
    """ 임의의 장소에 먹이를 배치 """
    while True:
        pos = (random.randint(0, W-1), random.randint(0, H-1))
        if pos in FOODS or pos in SNAKE:
            continue
        FOODS.append(pos)
        break
def add_bomb():
    while True:
        pos = (random.randint(0, W-1), random.randint(0 ,H-1))
        if pos in BOMBS or pos in SNAKE or pos in FOODS:
            continue
        BOMBS.append(pos)
        break
           
def move_food(pos):
    """ 먹이를 다른 장소로 이동 """
    i = FOODS.index(pos)
    del FOODS[i]
    add_food()

    
def paint(message):
    """ 화면 전체 그리기 """
    global score1
    SURFACE.fill((0, 0, 0))
    for food in FOODS:
        pygame.draw.ellipse(SURFACE, (0, 255, 0),
                            Rect(food[0]*60, food[1]*60, 60, 60))
    for bomb in BOMBS:
        SURFACE.blit(bombs,Rect(bomb[0]*60,bomb[1]*60,60,60))
        
    for body in SNAKE:
        pygame.draw.rect(SURFACE, (0, 255, 255),
                         Rect(body[0]*60, body[1]*60, 60,60))
    for index in range(20):
        pygame.draw.line(SURFACE, (128, 128, 128), (index*60, 0),
                         (index*60, 1200))
        pygame.draw.line(SURFACE, (128, 128, 128), (0, index*60),
                         (1200, index*60))
    if message != None:
        SURFACE.blit(message, (430, 550))
        pygame.mixer.music.stop()
    pygame.display.update()

def main():
    """ 메인 루틴 """
    pygame.mixer.music.load('mainmusic.wav')
    pygame.mixer.music.play(-1)
    food_sound = pygame.mixer.Sound('coin.wav')
    bomb_sound = pygame.mixer.Sound('bomb.wav')
    key = K_DOWN
    message = None
    game_over = False
    SNAKE.append((int(W/2), int(H/2)))
    
    for _ in range(10):
        add_food()
    for _ in range(15):
        add_bomb()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                key = event.key

        if not game_over:
            if key == K_LEFT:
                head = (SNAKE[0][0] - 1, SNAKE[0][1])
            elif key == K_RIGHT:
                head = (SNAKE[0][0] + 1, SNAKE[0][1])
            elif key == K_UP:
                head = (SNAKE[0][0], SNAKE[0][1] - 1)
            elif key == K_DOWN:
                head = (SNAKE[0][0], SNAKE[0][1] + 1)

            if head in SNAKE or \
               head[0] < 0 or head[0] >= W or \
               head[1] < 0 or head[1] >= H:
                message = myfont.render("Game Over!",
                                        True, (255, 255, 0))
                
                game_over = True
                
            SNAKE.insert(0, head)
            if head in FOODS:
                pygame.mixer.Sound.play(food_sound)
                move_food(head)
            elif head in BOMBS:
                pygame.mixer.Sound.play(bomb_sound)
                message = myfont.render("Game Over!",
                                        True, (255, 255, 0))
                game_over = True
            else:
                SNAKE.pop()
        paint(message)
        FPSCLOCK.tick(5)

if __name__ == '__main__':
    main()
