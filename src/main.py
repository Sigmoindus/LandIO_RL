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


class ColorsEnum(Enum):
    RED = 10
    RED_PLAYER = 11
    RED_PRE_TERRITORY = 12
    RED_TERRITORY = 13

    YELLOW = 20
    YELLOW_PLAYER = 21
    YELLOW_PRE_TERRITORY = 22
    YELLOW_TERRITORY = 23

    GREEN = 30
    GREEN_PLAYER = 31
    GREEN_PRE_TERRITORY = 32
    GREEN_TERRITORY = 33

    BROWN = 40
    BROWN_PLAYER = 41
    BROWN_PRE_TERRITORY = 42
    BROWN_TERRITORY = 43

    PURPLE = 50
    PURPLE_PLAYER = 51
    PURPLE_PRE_TERRITORY = 52
    PURPLE_TERRITORY = 53

    BLUE = 60
    BLUE_PLAYER = 61
    BLUE_PRE_TERRITORY = 62
    BLUE_TERRITORY = 63

    @staticmethod
    def get_player_colors():
        return [ColorsEnum.RED, ColorsEnum.YELLOW, ColorsEnum.GREEN,
                ColorsEnum.BROWN, ColorsEnum.PURPLE, ColorsEnum.BLUE]

    @staticmethod
    def _get_player_color(color):
        if color == ColorsEnum.RED_PLAYER:
            return 128, 0, 0
        elif color == ColorsEnum.YELLOW_PLAYER:
            return 128, 128, 0
        elif color == ColorsEnum.GREEN_PLAYER:
            return 0, 128, 0
        elif color == ColorsEnum.BLUE_PLAYER:
            return 0, 0, 128
        elif color == ColorsEnum.PURPLE_PLAYER:
            return 128, 0, 128
        elif color == ColorsEnum.BROWN_PLAYER:
            return 80, 21, 21
        return None

    @staticmethod
    def _get_territory_color(color):
        if color == ColorsEnum.RED_TERRITORY:
            return 255, 0, 0
        elif color == ColorsEnum.YELLOW_TERRITORY:
            return 255, 255, 0
        elif color == ColorsEnum.GREEN_TERRITORY:
            return 0, 255, 0
        elif color == ColorsEnum.BLUE_TERRITORY:
            return 0, 0, 255
        elif color == ColorsEnum.PURPLE_TERRITORY:
            return 255, 0, 255
        elif color == ColorsEnum.BROWN_TERRITORY:
            return 165, 42, 42
        return None

    @staticmethod
    def _get_pre_territory_color(color):
        if color == ColorsEnum.RED_PRE_TERRITORY:
            return 255, 153, 153
        elif color == ColorsEnum.YELLOW_PRE_TERRITORY:
            return 255, 255, 153
        elif color == ColorsEnum.GREEN_PRE_TERRITORY:
            return 153, 255, 153
        elif color == ColorsEnum.BLUE_PRE_TERRITORY:
            return 153, 153, 255
        elif color == ColorsEnum.PURPLE_PRE_TERRITORY:
            return 255, 153, 255
        elif color == ColorsEnum.BROWN_PRE_TERRITORY:
            return 255, 84, 84
        return None

    @staticmethod
    def to_color(color):
        for getter_func in [ColorsEnum._get_player_color, ColorsEnum._get_territory_color,
                            ColorsEnum._get_pre_territory_color]:
            returned_color = getter_func(color)
            if returned_color:
                return returned_color


class Colors:
    def __init__(self, color=None):
        self.color = color

    def get_player(self):
        return ColorsEnum(self.color.value + 1)

    def get_player_color(self):
        return ColorsEnum.to_color(self.get_player())

    def get_pre_territory(self):
        return ColorsEnum(self.color.value + 2)

    def get_pre_territory_color(self):
        return ColorsEnum.to_color(self.get_pre_territory())

    def get_territory(self):
        return ColorsEnum(self.color.value + 3)

    def get_territory_color(self):
        return ColorsEnum.to_color(self.get_territory())


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
        self.pre_territory = []
        self.territory = []

    def respawn(self, position):
        self.position = position
        self.direction = Direction.STAY

    def change_direction(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.direction != Direction.RIGHT:
                self.direction = Direction.LEFT
        elif keys[pygame.K_RIGHT]:
            if self.direction != Direction.LEFT:
                self.direction = Direction.RIGHT
        elif keys[pygame.K_UP]:
            if self.direction != Direction.DOWN:
                self.direction = Direction.UP
        elif keys[pygame.K_DOWN]:
            if self.direction != Direction.UP:
                self.direction = Direction.DOWN

    def move(self):
        if self.direction == Direction.UP:
            self.position[0] -= 1
        elif self.direction == Direction.DOWN:
            self.position[0] += 1
        elif self.direction == Direction.RIGHT:
            self.position[1] += 1
        elif self.direction == Direction.LEFT:
            self.position[1] -= 1


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
            self.land[tuple(player.position)] = player.color.get_player().value
            self.init_territory(player)

    def init_territory(self, player):
        start_x, start_y = player.position
        for i in range(start_x, start_x + 3):
            for j in range(start_y, start_y + 3):
                if i < self.size + 2 and j < self.size + 2:
                    self.land[i, j] = player.color.get_territory().value
                    player.territory.append((i, j))

    def add_player(self, player):
        self.players.append(player)
        player_colors = ColorsEnum.get_player_colors()
        available_colors = [color for color in player_colors if color not in [p.color for p in self.players if p.color]]
        if available_colors:
            player.color = Colors(available_colors[0])

    def update(self):
        for player in self.players:
            current_position = tuple(player.position)

            if not self.__is_border(player) and player.direction != Direction.STAY:
                previous_position = current_position
                previous_value = self.land[previous_position]

                # Mark the previous position as pre-invasion territory
                if not self.__is_territory(current_position, player):
                    self.land[previous_position] = player.color.get_pre_territory().value
                    player.pre_territory.append(previous_position)

                player.move()

                new_position = tuple(player.position)
                if self.__is_border(player):
                    player.direction = Direction.STAY
                    player.position = list(previous_position)
                    self.land[previous_position] = previous_value
                else:
                    if self.__is_pre_territory(new_position, player):
                        self.respawn_player(player)
                    elif self.__is_territory(new_position, player) and self.__has_pre_territory(player):
                        self.convert_pre_territory_to_territory(player)
                    else:
                        self.land[new_position] = player.color.get_player().value
            else:
                player.direction = Direction.STAY
                self.land[current_position] = player.color.get_player().value

    def respawn_player(self, player):
        self.clear_territory(player)
        player.respawn(self.init_player_position(random=1))
        self.init_territory(player)

    def clear_territory(self, player):
        for position in player.territory:
            self.land[position] = 0
        player.territory.clear()
        for position in player.pre_territory:
            self.land[position] = 0
        player.pre_territory.clear()

    def convert_pre_territory_to_territory(self, player):
        for position in player.pre_territory:
            self.land[position] = player.color.get_territory().value
            player.territory.append(position)
        player.pre_territory.clear()

    def __is_border(self, player):
        return self.land[tuple(player.position)] == -1

    def __is_pre_territory(self, position, player):
        return self.land[position] == player.color.get_pre_territory().value

    def __is_territory(self, position, player):
        return self.land[position] == player.color.get_territory().value

    def __has_pre_territory(self, player):
        return np.sum(self.land == player.color.get_pre_territory().value)

    def __is_free(self, position):
        return self.land[position] == 0


def draw_grid(screen, game):
    for y in range(1, game.size + 1):
        for x in range(1, game.size + 1):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)  # Draw grid lines
            if game.land[y, x] > 0:
                color = ColorsEnum.to_color(ColorsEnum(game.land[y, x]))
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


def tests():
    test_color = Colors(ColorsEnum.RED)
    print(test_color)
    print(test_color.get_player())


if __name__ == '__main__':
    main()
