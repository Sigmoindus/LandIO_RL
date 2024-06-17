import pygame
from player import Player
from game import Game
from visualization import Visualization

def main():
    pygame.init()
    clock = pygame.time.Clock()

    vis = Visualization()

    game = Game(size=10)
    player1 = Player(name="Player 1")
    player2 = Player(name="Player 2")

    game.add_player(player1)
    game.add_player(player2)
    game.start_game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                player1.change_direction(event.key)
                player2.change_direction(pygame.K_LEFT)

        game.update()
        game.update_leaderboard()

        vis.draw_grid(game)

        clock.tick(vis.FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
