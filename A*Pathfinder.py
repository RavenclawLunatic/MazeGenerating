# Is the actual A* algorithm
# Code adapted from https://www.youtube.com/watch?v=ob4faIum4kQ&t=562s
# 4/4/22
# author = Charlotte Miller

import pygame
import random
import queue
from MazeGeneration import *

class State(object):
    def __init__(self, value, parent, start = 0, goal = 0):
        self.children = []
        self.parent = parent
        self.value = value
        self.dist = 0
        if parent:
            self.path = parent.path[:]
            self.path.append(value)
            self.start = parent.start
            self.goal = parent.goal
        else:
            self.path = [value]
            self.start = start
            self.goal = goal

class StateString(State):
    def __init__(self, value, parent, start = 0, goal = 0):
        super(StateString, self).__init__(value, parent, start, goal)
        self.dist = self.GetDist()

    def GetDist(self):
        if self.value == self.goal:
            return 0
        return self.goal[0] - self.value[0], self.goal[1] - self.value[1]

    def CreateChildren(self, maze):
        parentcell = maze.cell_at(self.value[0], self.value[1])
        parentx = self.value[0]
        parenty = self.value[1]
        if not self.children:
            if not parentcell.walls['N']:
                self.children.append(maze.cell_at(parentx, parenty + 1))
            if not parentcell.walls['S']:
                self.children.append(maze.cell_at(parentx, parenty - 1))
            if not parentcell.walls['E']:
                self.children.append(maze.cell_at(parentx + 1, parenty))
            if not parentcell.walls['W']:
                self.children.append(maze.cell_at(parentx - 1, parenty))
        print("parentcell:", parentcell)

class AStarSolver:
    def __init__(self, start, goal, nx, ny):
        self.path = []
        self.visitedQueue = []
        self.priorityQueue = queue.PriorityQueue()
        self.start = start
        self.goal = goal
        self.maze = maze
        self.maze.gen_maze()
        print(self.maze)
        self.maze.draw_background()

    def Solve(self):
        startState = StateString(self.start, 0, self.start, self.goal)
        # number of child nodes that have been visited
        count = 0
        self.priorityQueue.put((0, count, startState))
        while(not self.path and self.priorityQueue.qsize()):
            closestChild = self.priorityQueue.get()[2]
            closestChild.CreateChildren(self.maze)
            self.visitedQueue.append(closestChild.value)
            for child in closestChild.children:
                dist = goal[0] - child.x, goal[1] - child.y
                print(dist)
                if (child.x, child.y) not in self.visitedQueue:
                    count += 1
                    if not dist:
                        self.path = child.path
                        break
                    self.priorityQueue.put((dist, count, child))
        if not self.path:
            print("Goal is impossible to reach")
        return self.path

if __name__ == "__main__":
    start = 0, 0
    goal = 14, 14
    a = AStarSolver(start, goal, 15, 15)
    a.Solve()