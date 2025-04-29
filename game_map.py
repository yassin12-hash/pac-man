import pygame

# Constants
WIDTH = 600

class GameMap:
    def __init__(self):
        self.move_image = pygame.image.load('images/pacmanmovemap.png')
        self.dot_image = pygame.image.load('images/pacmandotmap.png')
    
    def check_move_point(self, player):
        if (player.x + player.movex < 0):
            player.x = player.x + WIDTH
        if (player.x + player.movex > WIDTH):
            player.x = player.x - WIDTH
        if self.move_image.get_at((int(player.x + player.movex), int(player.y + player.movey - 80))) != pygame.Color('black'):
            player.movex = player.movey = 0
    
    def check_dot_point(self, x, y):
        if self.dot_image.get_at((int(x), int(y))) == pygame.Color('black'):
            return True
        return False
    
    def get_possible_direction(self, ghost):
        if ghost.x - 20 < 0:
            ghost.x = ghost.x + WIDTH
        if ghost.x + 20 > WIDTH:
            ghost.x = ghost.x - WIDTH
        
        directions = [0, 0, 0, 0]
        
        # Check right
        if ghost.x + 20 < WIDTH:
            if self.move_image.get_at((int(ghost.x + 20), int(ghost.y - 80))) == pygame.Color('black'):
                directions[0] = 1
        
        # Check down
        if ghost.x < WIDTH and ghost.x >= 0:
            if self.move_image.get_at((int(ghost.x), int(ghost.y - 60))) == pygame.Color('black'):
                directions[1] = 1
        
        # Check left
        if ghost.x - 20 >= 0:
            if self.move_image.get_at((int(ghost.x - 20), int(ghost.y - 80))) == pygame.Color('black'):
                directions[2] = 1
        
        # Check up
        if ghost.x < WIDTH and ghost.x >= 0:
            if self.move_image.get_at((int(ghost.x), int(ghost.y - 100))) == pygame.Color('black'):
                directions[3] = 1
        
        return directions