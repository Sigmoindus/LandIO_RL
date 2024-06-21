import numpy as np
from enum import Enum
from colors import Colors, ColorsEnum


class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4
    STAY = 5


class Game:
    def __init__(self, size):
        self.size = size
        self.land = np.zeros((size + 2, size + 2))
        self.land[[0, -1]] = -1
        self.land[:, [0, -1]] = -1
        self.players = []
        self.leaderboard = []

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
        for i in range(start_x - 1, start_x + 2):
            for j in range(start_y - 1, start_y + 2):
                if i < self.size + 2 and j < self.size + 2 and self.land[i, j] != -1:
                    self.land[i, j] = player.color.get_territory().value

    def add_player(self, player):
        self.players.append(player)
        player_colors = ColorsEnum.get_player_colors()
        available_colors = [color for color in player_colors if
                            color not in [p.color.color for p in self.players if p.color]]
        if available_colors:
            player.color = Colors(available_colors[0])

    def fill_region(self, array, x, y, fill_value):
        # Base cases to prevent the recursion from processing out of bounds or revisiting cells.
        if x < 0 or x >= array.shape[0] or y < 0 or y >= array.shape[1]:
            return False
        if array[x][y] == fill_value:
            return True  # boundary of the closed shape

        array[x][y] = fill_value  # Fill the cell with the target value

        # Recursive calls in four directions
        top = self.fill_region(array, x - 1, y, fill_value)
        bottom = self.fill_region(array, x + 1, y, fill_value)
        left = self.fill_region(array, x, y - 1, fill_value)
        right = self.fill_region(array, x, y + 1, fill_value)

        return top and bottom and left and right

    def find_and_fill_closed_shapes(self, player):
        array = self.land
        fill_value = player.color.get_territory().value
        # Scan the array to find enclosed regions and fill them.
        for i in range(1, array.shape[0] - 1):
            for j in range(1, array.shape[1] - 1):
                if array[i][j] != fill_value and array[i][j] != -1:  # start from a non-boundary cell
                    # Try to fill the region and check if it's actually enclosed
                    original_value = array[i][j]
                    array_copy = np.copy(array)
                    if self.fill_region(array_copy, i, j, fill_value):
                        array[i][j] = fill_value
                    else:
                        array[i][j] = original_value  # Restore the original value if not enclosed

    def update(self):
        print(self.land)
        for player in self.players:
            current_position = tuple(player.position)

            if not self.__is_border(player) and player.direction != Direction.STAY:
                previous_position = current_position
                previous_value = self.land[previous_position]

                if not self.__is_territory(current_position, player):

                    if player.now_color == player.color.get_territory().value:
                        self.land[previous_position] = player.now_color
                        player.now_color = 0
                    else:
                        self.land[previous_position] = player.color.get_pre_territory().value

                player.move()
                new_position = tuple(player.position)
                if self.__is_border(player):
                    player.direction = Direction.STAY
                    player.position = list(previous_position)
                    self.land[previous_position] = previous_value
                else:
                    if self.__is_pre_territory(new_position, player):
                        self.respawn_player(player)
                        continue
                    elif self.__is_territory(new_position, player):
                        player.now_color = player.color.get_territory().value
                        if self.__has_pre_territory(player):
                            self.convert_pre_territory_to_territory(player)
                            self.find_and_fill_closed_shapes(player)
                            # self.fill_enclosed_areas(player, self.land)
                    self.land[new_position] = player.color.get_player().value
            else:
                player.direction = Direction.STAY
                # TODO: resolve border stay problem
                self.land[current_position] = player.color.get_player().value

    def respawn_player(self, player):
        self.clear_territory(player)
        player.respawn(self.init_player_position(random=1))
        self.init_territory(player)

    def clear_territory(self, player):
        player_color = player.color.color.value // 10
        self.land[(self.land // 10) == player_color] = 0

    def convert_pre_territory_to_territory(self, player):
        mask = self.land == player.color.get_pre_territory().value
        self.land[mask] = player.color.get_territory().value

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

    def update_leaderboard(self):
        self.leaderboard = []
        for player in self.players:
            territory_percentage = np.sum(self.land == player.color.get_territory().value) / self.size ** 2 * 100
            self.leaderboard.append((player.name, territory_percentage))

        self.leaderboard.sort(key=lambda x: x[1], reverse=True)

    def get_leaderboard(self):
        return self.leaderboard
