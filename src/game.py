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
                    player.territory.append((i, j))

    def add_player(self, player):
        self.players.append(player)
        player_colors = ColorsEnum.get_player_colors()
        available_colors = [color for color in player_colors if color not in [p.color for p in self.players if p.color]]
        if available_colors:
            player.color = Colors(available_colors[0])

    def flood_fill(self, matrix, x, y, target, replacement):
        # Using a stack instead of recursion to avoid recursion depth issues
        stack = [(x, y)]
        while stack:
            x, y = stack.pop()
            if x < 0 or x >= len(matrix) or y < 0 or y >= len(matrix[0]):
                continue
            if matrix[x][y] != target:
                continue
            matrix[x][y] = replacement
            stack.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])

    def is_enclosed_area(self, matrix, x, y, value):
        if matrix[x][y] != 0:
            return False
        # Check if the zero area touches the boundary
        touched_boundary = [False]

        def dfs(x, y):
            if x <= 0 or x >= len(matrix) - 1 or y <= 0 or y >= len(matrix[0]) - 1:
                touched_boundary[0] = True
                return
            if matrix[x][y] != 0:
                return
            matrix[x][y] = -2  # Temporarily marking the cell to avoid revisiting
            dfs(x + 1, y)
            dfs(x - 1, y)
            dfs(x, y + 1)
            dfs(x, y - 1)

        dfs(x, y)
        # Restore the matrix
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == -2:
                    matrix[i][j] = 0
        return not touched_boundary[0]

    def fill_enclosed_areas(self, player, matrix):
        value = player.color.get_territory().value
        # Using a copied matrix for flood fill checks to avoid modifying the original during checks
        temp_matrix = np.copy(matrix)
        for i in range(1, len(matrix) - 1):
            for j in range(1, len(matrix[0]) - 1):
                if temp_matrix[i][j] == 0 and self.is_enclosed_area(temp_matrix, i, j, value):
                    self.flood_fill(matrix, i, j, 0, value)
                    if (i, j) not in player.territory:
                        player.territory.append((i, j))

    def update(self):

        leaderboard = []
        for player in self.players:
            current_position = tuple(player.position)

            if not self.__is_border(player) and player.direction != Direction.STAY:
                previous_position = current_position
                previous_value = self.land[previous_position]

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
                        self.fill_enclosed_areas(player, self.land)
                    else:
                        self.land[new_position] = player.color.get_player().value
            else:
                player.direction = Direction.STAY
                # TODO: resolve border stay problem
                self.land[current_position] = player.color.get_player().value

            leaderboard.append(len(player.territory) / self.size ** 2 * 100)

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
            if position not in player.territory:
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

    def update_leaderboard(self):
        self.leaderboard = []
        for player in self.players:
            if len(player.territory) > 0:
                territory_percentage = len(player.territory) / self.size ** 2 * 100
            else:
                territory_percentage = 0.0
            self.leaderboard.append((player.name, territory_percentage))

        self.leaderboard.sort(key=lambda x: x[1], reverse=True)

    def get_leaderboard(self):
        return self.leaderboard
