import pygame
from pygame.locals import *
import time
import random
import pygame_menu

SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load('resources/apple.jpg').convert()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 24) * SIZE
        self.y = random.randint(1, 19) * SIZE


class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load('resources/block.jpg').convert()
        self.direction = 'down'

        self.length = 1
        self.x = [40]
        self.y = [40]

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        # update body
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # update head
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


class Game:
    def __init__(self):
        self.dificuldade = 0.3

        self.surface = pygame.display.set_mode((1000, 800))

        pygame.mixer.init()

        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def play_background_music(self):
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play(-2, 0)

    def play_sound(self, sound_name):
        if sound_name == 'crash':
            sound = pygame.mixer.Sound('resources/crash.mp3')
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound('resources/ding.mp3')

        pygame.mixer.Sound.play(sound)

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def is_colision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def render_background(self):
        bg = pygame.image.load('resources/background.jpg')
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake eating apple
        if self.is_colision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound('ding')
            self.snake.increase_length()
            self.apple.move()

        # snake coliding with itself
        for i in range(1, self.snake.length):
            if self.is_colision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise 'Collision Itself'

        # snake colliding the borders
        if self.snake.x[0] < 0 or self.snake.y[0] < 0 or self.snake.x[0] >= 1000 or self.snake.y[0] >= 800:
            self.play_sound('crash')
            raise 'Collision Border'

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(
            f'Score: {self.snake.length - 1}', True, (200, 200, 200))
        self.surface.blit(score, (850, 10))

    def show_game_over(self):
        self.dificuldade = 0.3
        self.render_background()
        pygame.display.flip()

        menu = pygame_menu.Menu(
            height=400, theme=pygame_menu.themes.THEME_BLUE, title='Welcome', width=500)
        menu.add.label(f'Game is over! Your score is: {self.snake.length - 1}')
        menu.add.selector('Difficulty: ', [('Easy', 0.3), ('Normal', 0.2), (
            'Hard', 0.1), ('Insane', 0.05)], onchange=self.set_difficulty)
        menu.add.button('Play Again', self.start_the_game)
        menu.add.button('Quit', pygame_menu.events.EXIT)

        self.reset()
        menu.mainloop(self.surface)

    def inicialize(self):
        pygame.init()
        pygame.display.set_caption('Codebasics Snake And Apple Game')
        # Size of board
        surface = pygame.display.set_mode((1000, 800))

        menu = pygame_menu.Menu(
            height=400, theme=pygame_menu.themes.THEME_BLUE, title='Welcome', width=500)
        menu.add.selector('Difficulty: ', [('Easy', 0.3), ('Normal', 0.2), (
            'Hard', 0.1), ('Insane', 0.05)], onchange=self.set_difficulty)
        menu.add.button('Play', self.start_the_game)
        menu.add.button('Quit', pygame_menu.events.EXIT)

        menu.mainloop(surface)

    def set_difficulty(self, selected, value):
        self.dificuldade = value

    def start_the_game(self):
        game.run()

    def run(self):
        self.play_background_music()
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.mixer.music.pause()
                        self.show_game_over()
                        pause = True

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False
                    self.reset()

            try:
                if not pause:
                    self.play()
            except Exception as e:
                pygame.mixer.music.pause()
                self.show_game_over()
                pause = True

            time.sleep(self.dificuldade)


if __name__ == '__main__':
    game = Game()
    game.inicialize()
