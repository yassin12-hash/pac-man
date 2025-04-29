import pygame

class InputHandler:
    def __init__(self):
        pass  # No joystick initialization needed

    def check_input(self, player):
        keys = pygame.key.get_pressed()
        player.movex = 0
        player.movey = 0

        # Left movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.angle = 180
            player.movex = -20
        
        # Right movement
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.angle = 0
            player.movex = 20
        
        # Up movement
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.angle = 90
            player.movey = -20
        
        # Down movement
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.angle = 270
            player.movey = 20
