
from math import sqrt


class Cell:
    def __init__(self, x, y, cost):
        self.x = x
        self.y = y
        self.cost = cost
        self.value = 65535
        self.dir_x = 0
        self.dir_y = 0

class Field:
    def __init__(self, map):
        self.create_cost_field(map)
    def create_cost_field(self, map):
        self.height = len(map[0])
        self.width = len(map)
        self.grid = [[Cell(x, y, 1) for y in range(self.height)] for x in range(self.width)]
        for x in range(self.width):
            for y in range(self.height):
                if   map[x][y] == 1: self.grid[x][y].cost = 255
                elif map[x][y] == 0: self.grid[x][y].cost = 1
    def set_target(self, target_x, target_y):
        for x in range(self.width):
            for y in range(self.height):
                self.grid[x][y].value = 65535
        self.grid[target_x][target_y].value = 0
        open_list = [self.grid[target_x][target_y]]
        while len(open_list) > 0:
            current_cell = open_list.pop(0)
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == 0 and dy == 0: continue
                    if abs(dx) == abs(dy): continue
                    if current_cell.x+dx not in range(0, self.width) \
                    or current_cell.y+dy not in range(0, self.height): continue
                    neighbor_cell = self.grid[current_cell.x+dx][current_cell.y+dy]
                    if neighbor_cell.cost == 255: continue
                    new_value = current_cell.value+neighbor_cell.cost
                    if new_value >= neighbor_cell.value: continue
                    neighbor_cell.value = new_value
                    open_list.append(neighbor_cell)
        # generate_flow_field
        for x in range(self.width):
            for y in range(self.height):
                current_cell = self.grid[x][y]
                current_cell.dir_x = 0
                current_cell.dir_y = 0
                if current_cell.value == 0: continue
                if current_cell.value == 65535: continue
                dirs = []
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        if dx == 0 and dy == 0: continue
                        if current_cell.x+dx not in range(0, self.width) \
                        or current_cell.y+dy not in range(0, self.height): continue
                        neighbor_cell = self.grid[x+dx][y+dy]
                        dirs.append([neighbor_cell.value, dx, dy])
                dirs.sort(key=lambda x: x[0])
                current_cell.dir_x = dirs[0][1]
                current_cell.dir_y = dirs[0][2]
    def get_dir(self, x, y):
        x = int(x)
        y = int(y)
        if  x in range(0, self.width) \
        and y in range(0, self.height):
            cell = self.grid[x][y]
            return (cell.dir_x, cell.dir_y)
        else:
            return (0, 0)
    # def draw(self):
    #     for y in range(self.height):
    #         for x in range(self.width):
    #             cell = self.grid[x][y]
    #             if cell.cost == 255:
    #                 char = "#"
    #             else:
    #                 if   cell.dir_x <  0 and cell.dir_y == 0: char = "←"
    #                 elif cell.dir_x == 0 and cell.dir_y <  0: char = "↑"
    #                 elif cell.dir_x >  0 and cell.dir_y == 0: char = "→"
    #                 elif cell.dir_x == 0 and cell.dir_y >  0: char = "↓"
    #                 elif cell.dir_x <  0 and cell.dir_y <  0: char = "↖"
    #                 elif cell.dir_x >  0 and cell.dir_y <  0: char = "↗"
    #                 elif cell.dir_x >  0 and cell.dir_y >  0: char = "↘"
    #                 elif cell.dir_x <  0 and cell.dir_y >  0: char = "↙"
    #                 elif cell.dir_x == 0 and cell.dir_y == 0: char = "."
    #             print(char, end=" ")
    #         print()
