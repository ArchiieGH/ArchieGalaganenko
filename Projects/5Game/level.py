import random

class Level:

    def __init__(self):

        self.rows = 10
        self.cols = 15
        self.graph = []
        self.rand_start_row = random.randint(2, 7)
        self.rand_end_row = random.randint(self.rand_start_row - 1, self.rand_start_row + 2)
        self.base_row = (self.rand_start_row + self.rand_end_row) // 2

        # 0 - background
        # 1 - wall
        # 2 - bounce
        # 3 - spawn
        # 4 - finish

        self.create_level_graph()

    def create_level_graph(self):

        # creates a 15x10 level graph all filled with background
        for row in range(self.rows):
            layer = []
            for col in range(self.cols):
                layer.append(0)
            self.graph.append(layer)

        for col in range(self.cols):
            # creates start and end platforms at a random row
            if col < 3:
                self.graph[self.rand_start_row][col] = 1
            if col > 11:
                self.graph[self.rand_end_row][col] = 1

        self.graph[self.rand_start_row - 1][0] = 3
        self.graph[self.rand_end_row - 1][14] = 4

        for col in range(3, 12):
            hole = random.randint(0, 4)  # 25% chance

            if hole < 3:
                self.graph[self.base_row][col] = 1
            if hole != 2 or 1:
                self.graph[self.base_row - 2][col] = 1
            if self.base_row < 6:
                if hole > 0:
                    self.graph[self.base_row + 3][col] = 1
                if hole > 2:
                    self.graph[self.base_row + 3][col] = 2
