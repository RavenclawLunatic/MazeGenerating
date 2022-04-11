# Generates the maze for the A*Pathfinder to navigate through
# Code adapted from https://scipython.com/blog/making-a-maze/
# 4/4/22
# author = Charlotte Miller

import pygame
import random

background_color = (0, 157, 255)
black = (0, 0, 0)
pygame.init()

# an individual square in the maze
class Cell:
    # each cell has walls NSEW, but an N wall is an S
    # wall for the cell above and etc.
    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    # initializes Cell self at x, y, with all walls on
    def __init__(self, x, y):
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}
        self.x = x
        self.y = y

    # checks to see which walls still exist
    def all_walls(self):
        return all(self.walls.values())

    # gets rid of the wall between self and other
    def kill_wall(self, other, wall):
        self.walls[wall] = False
        other.walls[Cell.wall_pairs[wall]] = False

    def __str__(self):
        return str(self.x) + ' ' + str(self.y) + ' ' + str(self.walls.values())

# a grid of cells
class Maze:
    # initializes maze grid of nx*ny dimensions
    def __init__(self, nx, ny):
        ix = 0
        iy = 0
        self.nx, self.ny = nx, ny
        self.ix, self.iy = ix, iy
        self.maze_map = [[Cell(x, y) for y in range(ny)] for x in range(nx)]

    # returns Cell at xy
    def cell_at(self, x, y):
        return self.maze_map[x][y]

    # attempting to draw maze in pygame
    def wall_draw(self, ix, iy, iix, iiy):
        pygame.draw.line(screen, black, [ix,iy], [iix, iiy], 4)

    # event queue and background drawer
    def draw_background(self):
        global screen, running
        screen = pygame.display.set_mode(size=(1000, 1000))
        screen.fill(background_color)
        pygame.display.set_caption("Maze Generator")
        running = True
        pygame.display.flip()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    maze.draw_maze()

    # draws the actual maze
    def draw_maze(self):
        global screen
        corner_coords = []
        spacing = 250
        xsize = 500/self.nx
        ysize = 500/self.ny
        for x in range(self.nx + 1):
            for y in range(self.ny + 1):
                corner_coords.append((spacing + x * xsize, spacing + y * ysize))
                pygame.draw.circle(screen, black, (spacing + x * xsize, spacing + y * ysize), 2)
        # print(corner_coords)
        maze.wall_draw(250, 250, 750, 250)
        maze.wall_draw(250, 250, 250, 750)
        maze.wall_draw(250, 750, 750, 750)
        maze.wall_draw(750, 250, 750, 750)
        for x in range(self.nx):
            # vertical walls
            for y in range(self.ny):
                if self.maze_map[x][y].walls['E'] and corner_coords[ny*x+y+ny+x+1][1] != 750:
                    maze.wall_draw(corner_coords[ny*x+y+ny+x+1][0], corner_coords[ny*x+y+ny+x+1][1], corner_coords[ny*x+y+ny+x+2][0], corner_coords[ny*x+y+ny+x+2][1])
                else:
                    continue
            # horizontal walls
            for y in range(self.ny):
                if self.maze_map[x][y].walls['S']:
                    maze.wall_draw(corner_coords[ny*x+y+x+1][0], corner_coords[ny*x+y+x+1][1], corner_coords[ny*x+y+ny+x+2][0], corner_coords[ny*x+y+ny+x+2][1])
                else:
                    continue
        pygame.display.flip()


    # directly taken from site
    def __str__(self):
        """Return a (crude) string representation of the maze."""

        maze_rows = ['-' * self.nx * 2]
        for y in range(self.ny):
            maze_row = ['|']
            for x in range(self.nx):
                if self.maze_map[x][y].walls['E']:
                    maze_row.append(' |')
                else:
                    maze_row.append('  ')
            maze_rows.append(''.join(maze_row))
            maze_row = ['|']
            for x in range(self.nx):
                if self.maze_map[x][y].walls['S']:
                    maze_row.append('-+')
                else:
                    maze_row.append(' +')
            maze_rows.append(''.join(maze_row))
        return '\n'.join(maze_rows)

    # returns list of neighbors to self that have not
    # been visited yet
    def find_new_neighbors(self, cell):
        diff = [('W', (-1, 0)), ('E', (1, 0)), ('S', (0, 1)), ('N', (0, -1))]
        neighbors = []
        for direction, (dx, dy) in diff:
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < self.nx) and (0 <= y2 < self.ny):
                neighbor = self.cell_at(x2, y2)
                if neighbor.all_walls():
                    neighbors.append((direction, neighbor))
        return neighbors

    # finally generates the maze
    def gen_maze(self):
        # n is total num of cells
        n = self.nx * self.ny
        cell_stack = []
        current_cell = self.cell_at(self.ix, self.iy)
        # Total num of visited cells during generation of maze
        nv = 1
        while nv < n:
            neighbors = self.find_new_neighbors(current_cell)
            if not neighbors:
                # dead end has occurred so backtrack
                current_cell = cell_stack.pop()
                continue

            # Choose random neighboring cell and go there
            direction, next_cell = random.choice(neighbors)
            current_cell.kill_wall(next_cell, direction)
            cell_stack.append(current_cell)
            current_cell = next_cell
            nv += 1

nx, ny = 15, 15
maze = Maze(nx, ny)
maze.gen_maze()
maze.draw_background()