import random
import time
import pygame
from pygame.locals import *

Size = 40
Background_color = (65, 116, 166)


class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load(r'resources\apple.jpg').convert()
        self.parent_screen = parent_screen
        self.Block_Y = Size * random.randint(1, 14)
        self.Block_X = Size * random.randint(1, 24)

    def draw(self):
        self.parent_screen.blit(self.image, (self.Block_X, self.Block_Y))
        pygame.display.flip()

    def move(self):
        self.Block_X = random.randint(1, 24) * Size
        self.Block_Y = random.randint(1, 14) * Size


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.Block = pygame.image.load(r'resources\block.jpg').convert()
        self.Block_X = [Size] * length
        self.Block_Y = [Size] * length
        self.direction = 'right'

    def increase_length(self):
        self.length += 1
        self.Block_X.append(-1)
        self.Block_Y.append(-1)

    def Draw(self):

        for i in range(self.length):
            self.parent_screen.blit(self.Block, (self.Block_X[i], self.Block_Y[i]))
        pygame.display.flip()

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.Block_X[i] = self.Block_X[i - 1]
            self.Block_Y[i] = self.Block_Y[i - 1]

        if self.direction == 'up':
            self.Block_Y[0] -= Size
        if self.direction == 'down':
            self.Block_Y[0] += Size

        if self.direction == 'right':
            self.Block_X[0] += Size

        if self.direction == 'left':
            self.Block_X[0] -= Size
        self.Draw()


class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game ")
        self.surface = pygame.image.load(r'resources\snake.png')
        pygame.display.set_icon(self.surface)
        pygame.mixer.init()
        self.background_music()
        self.surface = pygame.display.set_mode((1000, 600))
        self.surface.fill(Background_color)
        self.Snake = Snake(self.surface, 1)
        self.Snake.Draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def background_music(self):
        pygame.mixer.music.load(r"resources\bg_music_1.mp3")
        pygame.mixer.music.play(-1)

    def render_background(self):
        bg = pygame.image.load(r"resources\background.jpg")
        self.surface.blit(bg, (0, 0))

    def is_collision(self, x1, y1, x2, y2):
        if x1 == x2 and y1 == y2:
            return True
        return False

    def play(self):
        self.render_background()
        self.Snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()
        if self.is_collision(self.Snake.Block_X[0], self.Snake.Block_Y[0], self.apple.Block_X, self.apple.Block_Y):
            ding_sound = pygame.mixer.Sound(r"resources\ding.mp3")
            pygame.mixer.Sound.play(ding_sound)
            self.Snake.increase_length()
            self.apple.move()

        for i in range(1, self.Snake.length):
            if self.is_collision(self.Snake.Block_X[0], self.Snake.Block_Y[0], self.Snake.Block_X[i],
                                 self.Snake.Block_Y[i]):
                sound = pygame.mixer.Sound(r"resources\crash.mp3")
                pygame.mixer.Sound.play(sound)
                raise ("Game Over")

        if not (0 <= self.Snake.Block_X[0] <= 960 and 0 <= self.Snake.Block_Y[0] <= 560):
            sound = pygame.mixer.Sound(r"resources\crash.mp3")
            pygame.mixer.Sound.play(sound)
            raise ("Hit the boundary error")

    def pause_game(self):

        self.render_background()
        font = pygame.font.SysFont('arial', 35)
        font2 = pygame.font.SysFont('arial', 35)
        line1 = font.render('Press Space to unpause the game ', True, (200, 200, 200))
        self.surface.blit(line1, (30, 400))
        line2 = font2.render("Press Esc to exit the game ", True, (200, 200, 200))
        self.surface.blit(line2, (30, 350))
        font3 = pygame.font.SysFont('arial', 60)
        line3 = font3.render("Snake Game ", True, (109, 214, 207))
        self.surface.blit(line3, (350, 120))
        self.display_score()
        pygame.mixer.music.pause()

        pygame.display.flip()

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f'Score: {self.Snake.length}', True, (200, 200, 200))
        self.surface.blit(score, (0, 0))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 35)
        font2 = pygame.font.SysFont('arial', 30)
        line1 = font.render(f'Score: {self.Snake.length}', True, (200, 200, 200))
        self.surface.blit(line1, (450, 350))
        line2 = font2.render("To play the game again press Space . To exit the game press Esc", True, (200, 200, 200))
        self.surface.blit(line2, (150, 250))
        font3 = pygame.font.SysFont('arial', 50)
        line3 = font3.render("Game Over", True, (109, 214, 207))
        self.surface.blit(line3, (380, 90))
        pygame.display.flip()

    def start_menu(self):

        self.render_background()
        self.image = pygame.image.load(r'resources\snake.png')
        self.surface.blit(self.image,(650,60))
        font = pygame.font.SysFont('arial', 25)
        font2 = pygame.font.SysFont('arial', 25)
        line1 = font.render('press Space to start the game ', True, (200, 200, 200))
        self.surface.blit(line1, (30, 400))
        line2 = font2.render("press Esc to exit the game ", True, (200, 200, 200))
        self.surface.blit(line2, (30, 450))
        font3 = pygame.font.SysFont('arial', 60)
        line3 = font3.render("Snake Game ", True, (109, 214, 207))
        self.surface.blit(line3, (350, 90))
        font4 = pygame.font.SysFont('arial', 25)
        line4 = font4.render("press Enter to pause the game ", True, (200, 200, 200))
        self.surface.blit(line4, (30, 500))
        pygame.display.flip()

    def Run(self):

        pause = False
        running = True
        if running == True:
            pause = True
            self.start_menu()
        while running:

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_SPACE:
                        pause = False
                        pygame.mixer.music.unpause()
                    if not pause:
                        if event.key == K_UP:
                            self.Snake.move_up()
                        if event.key == K_DOWN:
                            self.Snake.move_down()
                        if event.key == K_RIGHT:
                            self.Snake.move_right()
                        if event.key == K_LEFT:
                            self.Snake.move_left()
                        if event.key == K_RETURN:
                            self.pause_game()
                            pause = True
                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.0900)

    def reset(self):
        self.Snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)


if __name__ == "__main__":
    game = Game()
    game.Run()
