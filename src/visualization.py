import pygame
from colors import ColorsEnum

class Visualization:

    SCREEN_SIZE = 600
    GRID_SIZE = 50
    FPS = 2

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_SIZE + 200, self.SCREEN_SIZE))  # Adjust for leaderboard width

    def draw_grid(self, game):
        # Clear screen
        self.screen.fill((0, 0, 0))

        # Draw grid
        for y in range(game.size + 2):
            for x in range(game.size + 2):
                rect = pygame.Rect(x * self.GRID_SIZE, y * self.GRID_SIZE, self.GRID_SIZE, self.GRID_SIZE)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)  # Draw grid lines
                if game.land[y, x] > 0:
                    color = ColorsEnum.to_color(ColorsEnum(game.land[y, x]))
                    pygame.draw.rect(self.screen, color, rect)
                elif game.land[y, x] == -1:
                    pygame.draw.rect(self.screen, (100, 100, 100), rect)

        # Draw leaderboard side panel
        side_panel_rect = pygame.Rect(600, 0, 200, self.SCREEN_SIZE)
        pygame.draw.rect(self.screen, (50, 50, 50), side_panel_rect)

        # Draw leaderboard title
        font = pygame.font.Font(None, 36)
        title_text = font.render("Leaderboard", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(700, 50))
        self.screen.blit(title_text, title_rect)

        # Draw leaderboard entries
        font = pygame.font.Font(None, 24)
        leaderboard = game.get_leaderboard()  # Assume returns [(name, percentage, points), ...]
        y = 100
        for idx, (name, percentage) in enumerate(leaderboard):
            text = f"{idx + 1}. {name}: {percentage:.2f}%"
            text_render = font.render(text, True, (255, 255, 255))
            text_rect = text_render.get_rect(x=620, y=y)
            self.screen.blit(text_render, text_rect)
            y += 30

        # Update display
        pygame.display.flip()

# Assuming game instance and other setups are properly handled in the main application.
