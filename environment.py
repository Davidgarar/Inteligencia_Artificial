import random

class Environment:
    def __init__(self, size=10):
        self.size = size
        self.grid = [['.' for _ in range(size)] for _ in range(size)]
        self.start = (0, 0)
        self.goal = (size-1, size-1)
        self.generate()

    def generate(self):
        # Limpia el tablero
        for i in range(self.size):
            for j in range(self.size):
                self.grid[i][j] = '.'

        # Coloca obstáculos (venenos)
        for _ in range(int(self.size * 1.5)):
            x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)
            if (x, y) not in [self.start, self.goal]:
                self.grid[x][y] = 'X'

        # Coloca la hormiga y el hongo
        self.grid[self.start[0]][self.start[1]] = 'A'
        self.grid[self.goal[0]][self.goal[1]] = 'H'

    def get_neighbors(self, node):
        x, y = node
        moves = [(1,0), (-1,0), (0,1), (0,-1)]
        neighbors = []
        for dx, dy in moves:
            nx, ny = x+dx, y+dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if self.grid[nx][ny] != 'X':
                    neighbors.append((nx, ny))
        return neighbors
