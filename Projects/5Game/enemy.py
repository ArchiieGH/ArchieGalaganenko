from tile import Tile

class Enemy(Tile):

    def __init__(self, x, y, size):

        self.size = size
        super().__init__(self.size)  # gives access to parent class Tile
        self.speed = 3
        self.diff_x = 0
        self.diff_y = 0
        self.rect.x = x
        self.rect.y = y

class BlueEnemy(Enemy):

    def __init__(self, x, y, size):

        super().__init__(x, y, size)  # gives access to parent class Enemy
        self.surf.fill("Blue")

class BossEnemy(Enemy):

    def __init__(self, x, y, size):

        super().__init__(x, y, size)  # gives access to parent class Enemy
        self.surf.fill("Yellow")
        self.dead = False
        self.health = 500
        self.health_pos = 750
        self.speed = 4
