from enum import Enum
import pygame
from game import Direction


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

    def change_direction(self, key_type):

        # keys = pygame.key.get_pressed()
        # TODO: only one key check per move
        if key_type == pygame.K_LEFT:
            if self.direction != Direction.RIGHT:
                self.direction = Direction.LEFT
        elif key_type == pygame.K_RIGHT:
            if self.direction != Direction.LEFT:
                self.direction = Direction.RIGHT
        elif key_type == pygame.K_UP:
            if self.direction != Direction.DOWN:
                self.direction = Direction.UP
        elif key_type == pygame.K_DOWN:
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
