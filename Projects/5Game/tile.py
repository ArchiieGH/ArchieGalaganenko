import pygame

class Tile:

    def __init__(self, size):

        self.surf = pygame.Surface(size)    # representing image of  Tile object, where size is a tuple (x, y)
        self.rect = self.surf.get_rect()    # uses pygame method get_rect for storing Tile object's rectangle properties
        self.neighbours = []    # list which will contain other Tile objects

    def set_neighbours(self, tile_background):  # finds neighbours of Tile object (for pathfinding)

        for neighbour in tile_background:
            # up
            if neighbour.rect.y == self.rect.y - 100 and neighbour.rect.x == self.rect.x:
                self.neighbours.append(neighbour)

            # right
            if neighbour.rect.x == self.rect.x + 100 and neighbour.rect.y == self.rect.y:
                self.neighbours.append(neighbour)

            # down
            if neighbour.rect.y == self.rect.y + 100 and neighbour.rect.x == self.rect.x:
                self.neighbours.append(neighbour)

            # left
            if neighbour.rect.x == self.rect.x - 100 and neighbour.rect.y == self.rect.y:
                self.neighbours.append(neighbour)
