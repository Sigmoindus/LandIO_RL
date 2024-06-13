import pygame
import numpy as np
from enum import Enum

# Define constants
SCREEN_SIZE = 600
GRID_SIZE = 50
FPS = 2


class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4
    STAY = 5


class Colors(Enum):
    RED = 11
    YELLOW = 12
    GREEN = 13
    BROWN = 14
    PURPLE = 15
    BLUE = 16

    @staticmethod
    def to_color(color):
        if color == Colors.RED:
            return 255, 0, 0
        elif color == Colors.YELLOW:
            return 255, 255, 0
        elif color == Colors.GREEN:
            return 0, 255, 0
        elif color == Colors.BLUE:
            return 0, 0, 255
        elif color == Colors.PURPLE:
            return 128, 0, 128
        elif color == Colors.BROWN:
            return 165, 42, 42


class PlayerType(Enum):
    PLAYER = 0
    RL = 1


class Player:
    def __init__(self, name='Sigmoindus', mode=PlayerType.RL):
        self.color = None
        self.position = None
        self.direction = None
        self.name = name
        self.mode = mode

    def respawn(self, position):
        self.position = position
        self.direction = Direction.STAY

    def change_direction(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if not self.direction == Direction.RIGHT:
                self.direction = Direction.LEFT
        elif keys[pygame.K_RIGHT]:
            if not self.direction == Direction.LEFT:
                self.direction = Direction.RIGHT
        elif keys[pygame.K_UP]:
            if not self.direction == Direction.DOWN:
                self.direction = Direction.UP
        elif keys[pygame.K_DOWN]:
            if not self.direction == Direction.UP:
                self.direction = Direction.DOWN

    def move(self):
        if self.direction == Direction.UP:
            self.position[1] -= 1
        elif self.direction == Direction.DOWN:
            self.position[1] += 1
        elif self.direction == Direction.RIGHT:
            self.position[0] += 1
        elif self.direction == Direction.LEFT:
            self.position[0] -= 1


class Game:
    def __init__(self, size):
        self.size = size
        self.land = np.zeros((size + 2, size + 2))
        self.land[[0, -1]] = -1
        self.land[:, [0, -1]] = -1
        self.players = []

    def init_player_position(self, random=0):
        if random == 1:
            return np.random.randint(1, self.size + 1, size=(2,))
        elif random == 0:
            return [1, 1]

    def start_game(self):
        for player in self.players:
            player.respawn(self.init_player_position(random=1))
            self.land[tuple(player.position)] = player.color.value

    def add_player(self, player):
        self.players.append(player)
        available_colors = [color for color in Colors if color not in [p.color for p in self.players if p.color]]
        if available_colors:
            player.color = available_colors[0]

    def update(self):
        for player in self.players:
            self.land[tuple(player.position)] = 0  # Clear the old position
            player.move()
            self.land[tuple(player.position)] = player.color.value  # Set the new position


def draw_grid(screen, game):
    for y in range(game.size + 2):
        for x in range(game.size + 2):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)  # Draw grid lines
            if game.land[y, x] > 0:
                color = Colors.to_color(Colors(game.land[y, x]))
                pygame.draw.rect(screen, color, rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    clock = pygame.time.Clock()
    game = Game(size=10)
    player1 = Player(name="Player 1")
    game.add_player(player1)
    game.start_game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player1.change_direction()
        game.update()

        screen.fill((0, 0, 0))
        draw_grid(screen, game)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
