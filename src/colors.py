from enum import Enum


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


