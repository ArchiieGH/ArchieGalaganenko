import pygame
from tile import Tile

class Player(Tile):

    def __init__(self, x, y):

        self.size = (50, 50)
        super().__init__(self.size)  # gives access to parent class Tile

        self.y_speed = 0  # vertical player velocity
        self.jump_check = 0  # how many jumps the Player object has
        self.diff_x, self.diff_y = 0, 0  # buffer for collisions so object does not clip through level
        self.key = None
        self.advance = False
        self.dead = False
        self.rect.x, self.rect.y = x, y  # sets initial position of the Player object
        self.surf.fill("Red")

    def update(self):

        self.key = pygame.key.get_pressed()  # gets the state of all the keys on the keyboard
        # jump
        if self.key[pygame.K_SPACE] and self.jump_check == 0:
            self.y_speed = -18  # negative because y = 0 at the top of screen
            self.jump_check += 1
        # move left
        if self.key[pygame.K_a]:
            self.diff_x -= 5
        # move right
        if self.key[pygame.K_d]:
            self.diff_x += 5
        # gravity
        self.y_speed += 1
        if self.y_speed > 10:  # downward vertical velocity does not exceed 10
            self.y_speed = 10
        self.diff_y += self.y_speed
