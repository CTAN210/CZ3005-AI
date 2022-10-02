import json
from math import log

from .Node import Node


class Assignment:
    def __init__(self):
        self.start = "1"
        self.goal = "50"

        self.dist_map = None
        self.energy_cost_map = None
        self.coord_map = None

        with open("G.json", "r") as a:
            self.graph = json.load(a)

    def loadCost(self):
        with open("Cost.json", "r") as b:
            self.energy_cost_map = json.load(b)

    def loadDist(self):
        with open("Dist.json", "r") as c:
            self.dist_map = json.load(c)

    def loadCoord(self):
        with open("Coord.json", "r") as d:
            self.coord_map = json.load(d)

    def get_heuristic(self, node, goal, path=None):
        if path is None:
            path = []
        i, j = self.coord_map[node]

        i_goal, j_goal = self.coord_map[goal]

        i_delta = abs(i - i_goal)
        j_delta = abs(j - j_goal)

        manhattan_dist = i_delta + j_delta

        if path:
            manhattan_dist = 11*manhattan_dist + 11*self.traceDist(path)
        else:
            manhattan_dist *= 1
        return manhattan_dist

    def traceDist(self, solution):
        solution = solution.copy()
        dist = 0
        solution_txt = "{},{}".format(solution[-2],solution[-1])
        dist += self.dist_map[solution_txt]

        while True:
            if solution[-2] == self.start:
                return dist
            solution.pop()
            solution_txt = "{},{}".format(solution[-2],solution[-1])
            dist += self.dist_map[solution_txt]

    def tracePath(self, solution):
        solution = solution.copy()
        cost = 0
        solution_txt = "{},{}".format(solution[-2],solution[-1])
        cost += self.energy_cost_map[solution_txt]

        while True:
            if solution[-2] == self.start:
                return cost
            solution.pop()
            solution_txt = "{},{}".format(solution[-2],solution[-1])
            cost += self.energy_cost_map[solution_txt]
