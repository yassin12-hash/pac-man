import pgzrun
from handler_input import *
from game_map import *
from random import randint
from datetime import datetime

# Constants
WIDTH = 600
HEIGHT = 660
SPEED = 4

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
WIN = 3

class PacmanGame:
    def __init__(self):
        self.game_state = MENU
        self.score = 0
        self.high_score = 0
        self.reset_game()
    
    def reset_game(self):
        self.player = Actor("pacman_o")
        self.player.x = 290
        self.player.y = 570
        self.player.status = 0
        self.player.inputActive = True
        self.player.movex = 0
        self.player.movey = 0
        
        self.ghosts = []
        self.pac_dots = []
        self.move_ghosts_flag = 4
        
        self.game_map = GameMap()
        self.input_handler = InputHandler()
        
        # Reset score when starting a new game, but not when initializing
        if self.game_state != MENU:
            self.score = 0
            
        self.game_state = PLAYING
        
        self.init_dots()
        self.init_ghosts()
    
    def init_dots(self):
        self.pac_dots = []
        dot_index = 0
        
        for x in range(30):
            for y in range(29):
                if self.game_map.check_dot_point(10 + x * 20, 10 + y * 20):
                    self.pac_dots.append(Actor("dot", (10 + x * 20, 90 + y * 20)))
                    self.pac_dots[dot_index].status = 0
                    dot_index += 1
    
    def init_ghosts(self):
        self.ghosts = []
        self.move_ghosts_flag = 4
        
        for g in range(4):
            self.ghosts.append(Actor(f"ghost{g+1}", (270 + (g * 20), 370)))
            self.ghosts[g].dir = randint(0, 3)
    
    def get_player_image(self):
        dt = datetime.now()
        a = self.player.angle
        tc = dt.microsecond % (500000 / SPEED) / (100000 / SPEED)
        
        if tc > 2.5 and (self.player.movex != 0 or self.player.movey != 0):
            if a != 180:
                self.player.image = "pacman_c"
            else:
                self.player.image = "pacman_cr"
        else:
            if a != 180:
                self.player.image = "pacman_o"
            else:
                self.player.image = "pacman_or"
        
        self.player.angle = a
    
    def draw_ghosts(self):
        for g in range(len(self.ghosts)):
            if self.ghosts[g].x > self.player.x:
                self.ghosts[g].image = f"ghost{g+1}r"
            else:
                self.ghosts[g].image = f"ghost{g+1}"
            self.ghosts[g].draw()
    
    def draw_menu(self, screen):
        screen.fill((0, 0, 0))
        screen.draw.text("PACMAN", center=(WIDTH/2, HEIGHT/4), owidth=0.5, 
                       ocolor=(255, 255, 255), color=(255, 255, 0), fontsize=60)
        screen.draw.text("Press ENTER to start", center=(WIDTH/2, HEIGHT/2), owidth=0.5, 
                       ocolor=(255, 255, 255), color=(255, 255, 255), fontsize=30)
        screen.draw.text(f"High Score: {self.high_score}", center=(WIDTH/2, HEIGHT/2 + 50), owidth=0.5, 
                       ocolor=(255, 255, 255), color=(255, 64, 0), fontsize=20)
    
    def draw_game(self, screen):
        screen.blit('header', (0, 0))
        screen.blit('colourmap', (0, 80))
        
        # Draw score
        screen.draw.text(f"Score: {self.score}", topleft=(20, 40), owidth=0.5, 
                       ocolor=(0, 0, 0), color=(255, 255, 255), fontsize=20)
        screen.draw.text(f"High Score: {self.high_score}", topright=(WIDTH-20, 40), owidth=0.5, 
                       ocolor=(0, 0, 0), color=(255, 255, 255), fontsize=20)
        
        # Draw and check pac dots
        pac_dots_left = 0
        for a in range(len(self.pac_dots)):
            if self.pac_dots[a].status == 0:
                self.pac_dots[a].draw()
                pac_dots_left += 1
            if self.pac_dots[a].collidepoint((self.player.x, self.player.y)) and self.pac_dots[a].status == 0:
                self.pac_dots[a].status = 1
                self.score += 10  # Add points for eating a pac dot
        
        if pac_dots_left == 0:
            self.game_state = WIN
            if self.score > self.high_score:
                self.high_score = self.score
        
        self.draw_ghosts()
        self.get_player_image()
        self.player.draw()
        
        if self.game_state == GAME_OVER:
            screen.draw.text("GAME OVER", center=(300, 434), owidth=0.5, 
                           ocolor=(255, 255, 255), color=(255, 64, 0), fontsize=40)
            screen.draw.text("Press SPACE to restart", center=(300, 484), owidth=0.5, 
                           ocolor=(255, 255, 255), color=(255, 255, 255), fontsize=20)
        
        if self.game_state == WIN:
            screen.draw.text("YOU WIN!", center=(300, 434), owidth=0.5, 
                           ocolor=(255, 255, 255), color=(255, 64, 0), fontsize=40)
            screen.draw.text("Press SPACE to restart", center=(300, 484), owidth=0.5, 
                           ocolor=(255, 255, 255), color=(255, 255, 255), fontsize=20)
    
    def draw(self, screen):
        if self.game_state == MENU:
            self.draw_menu(screen)
        else:
            self.draw_game(screen)
    
    def ghost_collided(self, ghost_a, ghost_index):
        for g in range(len(self.ghosts)):
            if self.ghosts[g].colliderect(ghost_a) and g != ghost_index:
                return True
        return False
    
    def move_ghosts(self):
        dmoves = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.move_ghosts_flag = 0
        
        for g in range(len(self.ghosts)):
            dirs = self.game_map.get_possible_direction(self.ghosts[g])
            
            if self.ghost_collided(self.ghosts[g], g) and randint(0, 3) == 0:
                self.ghosts[g].dir = 3
            
            if dirs[self.ghosts[g].dir] == 0 or randint(0, 50) == 0:
                d = -1
                while d == -1:
                    rd = randint(0, 3)
                    if dirs[rd] == 1:
                        d = rd
                self.ghosts[g].dir = d
            
            animate(
                self.ghosts[g], 
                pos=(self.ghosts[g].x + dmoves[self.ghosts[g].dir][0] * 20, 
                     self.ghosts[g].y + dmoves[self.ghosts[g].dir][1] * 20), 
                duration=1/SPEED, 
                tween='linear', 
                on_finished=self.flag_move_ghosts
            )
    
    def flag_move_ghosts(self):
        self.move_ghosts_flag += 1
    
    def input_lock(self):
        self.player.inputActive = False
    
    def input_unlock(self):
        self.player.movex = self.player.movey = 0
        self.player.inputActive = True
    
    def check_key_input(self):
        # Check for game state transitions
        if self.game_state == MENU and keyboard.RETURN:
            self.reset_game()
        
        if (self.game_state == GAME_OVER or self.game_state == WIN) and keyboard.space:
            self.reset_game()
    
    def update(self):
        self.check_key_input()
        
        if self.game_state == PLAYING:
            if self.move_ghosts_flag == 4:
                self.move_ghosts()
            
            # Check ghost collisions
            for g in range(len(self.ghosts)):
                if self.ghosts[g].collidepoint((self.player.x, self.player.y)):
                    self.game_state = GAME_OVER
                    if self.score > self.high_score:
                        self.high_score = self.score
            
            # Handle player input and movement
            if self.player.inputActive:
                self.input_handler.check_input(self.player)
                self.game_map.check_move_point(self.player)
                
                if self.player.movex or self.player.movey:
                    self.input_lock()
                    animate(
                        self.player, 
                        pos=(self.player.x + self.player.movex, self.player.y + self.player.movey), 
                        duration=1/SPEED, 
                        tween='linear', 
                        on_finished=self.input_unlock
                    )

# Create game instance
game = PacmanGame()

# Pygame Zero functions
def draw():
    game.draw(screen)

def update():
    game.update()

# Run the game
pgzrun.go()