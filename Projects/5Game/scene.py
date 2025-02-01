from random import randint
from tile import Tile
from math import sqrt
from player import Player
from enemy import BossEnemy
from enemy import BlueEnemy

class Scene:

    def __init__(self, screen, level):

        self.screen = screen
        self.level = level

        self.tile_size = (100, 100)
        self.tile_list = []
        self.tile_wall_list = []
        self.tile_background = []
        self.tile_bounce_list = []
        self.create_tile_list()

        # enemy initialisation
        self.enemy = None
        self.enemy_change_direction = []

        self.place_enemy()

        # creates instance of Player class
        self.player = Player(self.spawn_tile.rect.x + 25, self.spawn_tile.rect.y + 25)

    def create_tile_list(self):
        # create level
        for row in range(self.level.rows):
            for col in range(self.level.cols):
                # loops through every item in the level_graph

                if self.level.graph[row][col] == 0:
                    tile = Tile(self.tile_size)  # initialise Tile object
                    tile.rect.x = col * 100  # assigns actual x coordinate to tile using col number
                    tile.rect.y = row * 100  # assigns actual y coordinate to tile using row number
                    self.tile_background.append(tile)
                    self.tile_list.append(tile)

                if self.level.graph[row][col] == 1:
                    tile = Tile(self.tile_size)
                    tile.rect.x = col * 100
                    tile.rect.y = row * 100
                    tile.surf.fill("Grey")
                    self.tile_wall_list.append(tile)
                    self.tile_list.append(tile)

                if self.level.graph[row][col] == 2:
                    tile = Tile(self.tile_size)
                    tile.rect.x = col * 100
                    tile.rect.y = row * 100
                    tile.surf.fill("Purple")
                    self.tile_bounce_list.append(tile)
                    self.tile_list.append(tile)

                if self.level.graph[row][col] == 3:
                    self.spawn_tile = Tile(self.tile_size)
                    self.spawn_tile.rect.x = col * 100
                    self.spawn_tile.rect.y = row * 100
                    self.spawn_tile.surf.fill("Cyan")
                    self.tile_list.append(self.spawn_tile)

                if self.level.graph[row][col] == 4:
                    self.finish_tile = Tile(self.tile_size)
                    self.finish_tile.rect.x = col * 100
                    self.finish_tile.rect.y = row * 100
                    self.finish_tile.surf.fill("Green")
                    self.tile_list.append(self.finish_tile)

    def place_enemy(self):
        tile_enemy_list = []
        # finds available tile to place the enemy on
        for tile_background in self.tile_background:
            for tile_wall in self.tile_wall_list:
                # finds available wall tiles that have a background tile on top
                if tile_background.rect.bottom - tile_wall.rect.top == 0 and tile_background.rect.x == tile_wall.rect.x:
                    tile_enemy_list.append(tile_background)
        random_tile = tile_enemy_list[randint(0, len(tile_enemy_list) - 1)]
        # creates instance of BlueEnemy class
        self.enemy = BlueEnemy(random_tile.rect.x, random_tile.rect.y + 50, (50, 50))

    def player_collision(self):  # all collisions that occur with the player

        # stops player if tries to leave the edges of the screen
        if self.player.rect.x < 0:
            self.player.rect.x = 0
        if self.player.rect.x > 1500:
            self.player.rect.x = 1450
        if self.player.rect.y < 0:
            self.player.rect.y = 0
            self.player.y_speed = 0
        if self.player.rect.y > 1000:
            self.player.dead = True

        for tile in self.tile_wall_list:
            # stops player if it hits the side of the wall tile
            if tile.rect.colliderect((self.player.rect.x + self.player.diff_x, self.player.rect.y), self.player.size):
                self.player.diff_x = 0
            if tile.rect.colliderect((self.player.rect.x, self.player.rect.y + self.player.diff_y), self.player.size):
                # stops player if it hits bottom of the wall tile
                if self.player.y_speed < 0:
                    self.player.diff_y = tile.rect.bottom - self.player.rect.top
                    self.player.y_speed = 0  # so player does not "stick" to the bottom of the wall tile
                # stops player if it hits top of the wall tile
                elif self.player.y_speed >= 0:
                    self.player.diff_y = tile.rect.top - self.player.rect.bottom
                    self.player.y_speed = 0
                # resets jump_check if player hits top of the wall tile
                if tile.rect.top - self.player.rect.bottom == 0:
                    self.player.jump_check = 0

        for tile in self.tile_bounce_list:
            # stops player if it hits top of the wall tile
            if tile.rect.colliderect((self.player.rect.x, self.player.rect.y + self.player.diff_y), self.player.size):
                if self.player.y_speed >= 0:
                    self.player.diff_y = tile.rect.top - self.player.rect.bottom
                    self.player.y_speed = -18  # makes the player "jump"

        # moves on to the next level if player collides with the green tile
        if self.finish_tile.rect.colliderect(self.player.rect):
            self.player.advance = True

        self.player.rect.x += self.player.diff_x  # adds the x buffer to the player's x coord
        self.player.rect.y += self.player.diff_y  # adds the y buffer to the player's y coord
        # resets the buffers back to 0 for the next turn in the game loop
        self.player.diff_x = 0
        self.player.diff_y = 0

    def draw(self):  # draws everything using surf and rect onto the screen

        for tile in self.tile_list:
            self.screen.blit(tile.surf, tile.rect)

        self.screen.blit(self.enemy.surf, self.enemy.rect)

        self.screen.blit(self.player.surf, self.player.rect)

    def update(self):  # adds all the functions in order into 1 function

        self.player.update()
        self.player_collision()
        self.draw()


class BossScene:

    def __init__(self, screen, level_graph):

        self.screen = screen
        self.level_graph = level_graph
        self.player = Player(50, 850)
        self.boss = BossEnemy(1400, 0, (100, 100))
        self.orb = Tile((50, 50))

        self.tile_size = (100, 100)
        self.tile_list = []
        self.tile_wall_list = []
        self.tile_background = []
        self.tile_orb_list = []

        # pathfind variables
        self.parent = dict()
        self.g_score = dict()
        self.f_score = dict()

        self.target_tile = None

        self.create_tile_lists()

        random_tile = self.tile_orb_list[randint(0, len(self.tile_orb_list) - 1)]
        self.orb.surf.fill("Cyan")
        self.orb.rect.x = random_tile.rect.x + 25
        self.orb.rect.y = random_tile.rect.y + 50

        for tile in self.tile_background:
            tile.set_neighbours(self.tile_background)

        self.create_a_star()

    def create_tile_lists(self):

        # initialise level
        for row in range(10):
            for col in range(15):
                # loops through every character in the level_map
                if self.level_graph[row][col] == 0:
                    tile = Tile(self.tile_size)  # initialise Tile object
                    tile.rect.x = col * 100
                    tile.rect.y = row * 100
                    self.tile_background.append(tile)

                if self.level_graph[row][col] == 1:
                    tile = Tile(self.tile_size)  # initialise Tile object
                    tile.rect.x = col * 100
                    tile.rect.y = row * 100
                    tile.surf.fill("Grey")
                    self.tile_wall_list.append(tile)

        # finds random tile for the first orb
        for tile_background in self.tile_background:
            for tile_wall in self.tile_wall_list:
                if tile_background.rect.bottom - tile_wall.rect.top == 0 and tile_background.rect.x == tile_wall.rect.x:
                    self.tile_orb_list.append(tile_background)

    def create_a_star(self):

        # initialises pathfind variables
        self.path = []
        self.start_tile = self.closest_tile(self.boss)
        for tile in self.tile_background:
            self.g_score[tile] = float('inf')
            self.f_score[tile] = float('inf')

        self.end_tile = self.closest_tile(self.player)
        self.opened = {self.start_tile}
        self.g_score[self.start_tile] = 0
        self.f_score[self.start_tile] = self.find_h_score(self.end_tile, self.start_tile)


    def player_collision(self):  # all collisions that occur with the player

        # stops player if tries to leave the edges of the screen
        if self.player.rect.x < 0:
            self.player.rect.x = 0
        if self.player.rect.x > 1500:
            self.player.rect.x = 1450
        if self.player.rect.y < 0:
            self.player.rect.y = 0
            self.player.y_speed = 0
        if self.player.rect.y > 1000:
            self.player.dead = True

        for tile in self.tile_wall_list:
            # stops player if it hits the side of the wall tile
            if tile.rect.colliderect((self.player.rect.x + self.player.diff_x, self.player.rect.y), self.player.size):
                self.player.diff_x = 0
            if tile.rect.colliderect((self.player.rect.x, self.player.rect.y + self.player.diff_y), self.player.size):
                # stops player if it hits bottom of the wall tile
                if self.player.y_speed < 0:
                    self.player.diff_y = tile.rect.bottom - self.player.rect.top
                    self.player.y_speed = 0  # so player does not "stick" to the bottom of the wall tile
                # stops player if it hits top of the wall tile
                elif self.player.y_speed >= 0:
                    self.player.diff_y = tile.rect.top - self.player.rect.bottom
                    self.player.y_speed = 0
                # resets jump_check if player hits top of the wall tile
                if tile.rect.top - self.player.rect.bottom == 0:
                    self.player.jump_check = 0

        if self.boss.rect.colliderect(self.player):
            self.player.dead = True

        if self.orb.rect.colliderect(self.player.rect):
            self.boss.health -= 50
            if self.boss.health == 0:
                self.boss.dead = True
            self.boss.health_pos -= 25
            random_tile = self.tile_orb_list[randint(0, len(self.tile_orb_list) - 1)]

            self.orb.rect.x = random_tile.rect.x + 25
            self.orb.rect.y = random_tile.rect.y + 50

        self.player.rect.x += self.player.diff_x  # adds the x buffer to the player's rect x coord
        self.player.rect.y += self.player.diff_y  # adds the y buffer to the player's rect y coord
        # resets the buffers back to 0 for the next turn in the game loop
        self.player.diff_x = 0
        self.player.diff_y = 0

    def closest_tile(self, object_tile):  # finds the closest tile to the object_tile using pythagoras

        length_to_object_tile = dict()
        for tile in self.tile_background:
            dx = object_tile.rect.centerx - tile.rect.centerx
            dy = object_tile.rect.centery - tile.rect.centery
            length = sqrt(dx * dx + dy * dy)
            length_to_object_tile[tile] = length  # assigns each length to each tile in tile_background
        # finds the smallest length value out of every tile
        return min(length_to_object_tile, key=lambda x: length_to_object_tile[x])

    def find_h_score(self, end_tile, current_tile):  # finds euclidean distance between 2 the two arguments

        h_dx = current_tile.rect.x - end_tile.rect.x
        h_dy = - current_tile.rect.y - end_tile.rect.y
        return sqrt(h_dx * h_dx + h_dy * h_dy)

    def a_star_algorithm(self):  # finds the shortest path between boss and player

        while len(self.opened) > 0:
            current_tile = min(self.opened, key=lambda x: self.f_score[x])
            if current_tile == self.end_tile:
                self.path = [current_tile]
                while current_tile in self.parent:
                    current_tile = self.parent[current_tile]
                    self.path.insert(0, current_tile)
                    if current_tile == self.start_tile:
                        self.target_tile = self.path[1]
                        break
                break
            self.opened.remove(current_tile)
            for neighbour in current_tile.neighbours:
                est_g_score = self.g_score[current_tile] + 100
                if est_g_score < self.g_score[neighbour]:
                    self.parent[neighbour] = current_tile
                    self.g_score[neighbour] = est_g_score
                    self.f_score[neighbour] = est_g_score + self.find_h_score(self.end_tile, neighbour)
                    if neighbour not in self.opened:
                        self.opened.add(neighbour)

    def move_boss(self):  # moves boss towards the target_tile

        if self.boss.rect.x < self.target_tile.rect.x:
            self.boss.diff_x += self.boss.speed
        if self.boss.rect.x > self.target_tile.rect.x:
            self.boss.diff_x -= self.boss.speed
        if self.boss.rect.y < self.target_tile.rect.y:
            self.boss.diff_y += self.boss.speed
        if self.boss.rect.y > self.target_tile.rect.y:
            self.boss.diff_y -= self.boss.speed
        # resets all variables for pathfinding for the next target_tile to be found
        if self.boss.rect.center == self.target_tile.rect.center:
            self.create_a_star()

        self.boss.rect.x += self.boss.diff_x  # adds x buffer to x coord
        self.boss.rect.y += self.boss.diff_y  # adds y buffer to y coord
        # resets buffers for the next turn in game loop
        self.boss.diff_x = 0
        self.boss.diff_y = 0

    def draw(self):  # draws everything using surf rect onto the screen

        for tile in self.tile_wall_list:
            self.screen.blit(tile.surf, tile.rect)

        for tile in self.tile_background:
            tile.surf.fill("Black")
            self.screen.blit(tile.surf, tile.rect)

        self.screen.blit(self.player.surf, self.player.rect)
        self.screen.blit(self.boss.surf, self.boss.rect)
        self.screen.blit(self.orb.surf, self.orb.rect)

        # initialises and draws boss health bar using its health
        health_outline = Tile((510, 50))
        health_outline.rect.center = (750, 950)
        health_bar = Tile((self.boss.health, 40))
        health_bar.rect.center = (self.boss.health_pos, 950)
        health_outline.surf.fill("White")
        health_bar.surf.fill("Red")

        self.screen.blit(health_outline.surf, health_outline.rect)
        self.screen.blit(health_bar.surf, health_bar.rect)

    def update(self):  # adds all the functions in order into 1 function

        self.player.update()
        self.player_collision()
        self.a_star_algorithm()
        self.move_boss()
        self.draw()
