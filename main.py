import json
import time
import sys

from Models.Assignment import Assignment
from Models.Frontier import Frontier
from Models.Node import Node

a = Assignment()
a.loadCost()
a.loadDist()
a.loadCoord()



def astar_search(problem):
    path = []
    explored_nodes = list()

    if problem.start == problem.goal:
        return path, explored_nodes

    path.append(problem.start)
    path_cost = problem.get_heuristic(problem.start, problem.goal)

    frontier = Frontier(Node(path_cost, path)) 
    while frontier.size() > 0:
        popped_node = frontier.pop_frontier()
        path_cost_till_now, path_till_now = popped_node.path_cost, popped_node.path
        curNode = path_till_now[-1]
        if len(path_till_now) == 1:
            manhattanPath = None
        else:
            manhattanPath = path_till_now
        path_cost_till_now -= problem.get_heuristic(curNode, problem.goal, manhattanPath)
        explored_nodes.append(curNode)

        
        if curNode == problem.goal:
            return path_till_now, path_cost_till_now

        neighbours = problem.graph[curNode]

        for neighbour in neighbours:
            path_to_neighbour = path_till_now.copy()
            path_to_neighbour.append(neighbour)

            extra_cost = problem.energy_cost_map[curNode + "," + neighbour]
            neighbour_cost = 1*extra_cost + path_cost_till_now + problem.get_heuristic(neighbour, problem.goal, path_to_neighbour)

            is_there, index, neighbour_old_cost, _ = frontier.getNewParams(neighbour)

            if (neighbour not in explored_nodes) and not is_there:
                frontier.append(Node(neighbour_cost, path_to_neighbour))
            
            elif is_there:
                if neighbour_old_cost > neighbour_cost:
                    frontier.pop(index)
                    frontier.append(Node(neighbour_cost, path_to_neighbour))

    return None, None

def uniform_cost_search(problem, minimize, energy_constraint=None):
    path = []
    explored_nodes = list()
    cost_map = 0
    if minimize == "Cost":
      cost_map = problem.energy_cost_map
    elif minimize == "Dist":
      cost_map = problem.dist_map

    if problem.start == problem.goal:
      return path, explored_nodes

    path.append(problem.start)
    path_cost = 0

    frontier = Frontier(Node(path_cost, path)) # initialize the frontier with the start node
    while frontier.size() > 0:
        # pop a node from the queue
        popped_node = frontier.pop_frontier()
        path_till_now = popped_node.path
        path_cost_till_now = popped_node.path_cost
        # check if there is an energy constraint and if expanding the path will exceed the energy budget
        if frontier.size() > 1 and energy_constraint:
            if problem.tracePath(path_till_now) > energy_constraint:
                continue
        curNode = path_till_now[-1]
        explored_nodes.append(curNode)

        # test goal condition
        if curNode == problem.goal:
            return path_till_now, path_cost_till_now

        neighbours = problem.graph[curNode]

        for neighbour in neighbours:
            path_to_neighbour = path_till_now.copy()
            path_to_neighbour.append(neighbour)

            extra_cost = cost_map[curNode + "," + neighbour]
            neighbour_cost = extra_cost + path_cost_till_now

            is_there, index, neighbour_old_cost, _ = frontier.getNewParams(neighbour)

            if neighbour not in explored_nodes and not is_there:
                frontier.append(Node(neighbour_cost, path_to_neighbour))
            # If the neighbour is in frontier but there exists a
            # costlier path to this neighbour, remove that costly path
            if is_there:
                if neighbour_old_cost > neighbour_cost:
                    frontier.pop(index)
                    frontier.append(Node(neighbour_cost, path_to_neighbour))

    return None, None
  
def formatPath(path_array):
  final_path = "1->"
  for node in path_array:
    if node == "1":
      continue
    elif (node == "50"):
      final_path = final_path + node
    else:
      final_path = final_path + node + "->"
  return final_path

print("====================  Task 1: Uniform Cost Search (No Energy Cost Search) ==================== ")
path, cost = uniform_cost_search(a, "Dist")
print("Length of Path: ", len(path),'\n')
print("Shortest path: ", formatPath(path),'\n')
print("Shortest distance:", a.traceDist(path),'\n')
print("Total energy cost:", a.tracePath(path),'\n')




print("==================== Task 2: Uniform Cost Search (Energy Budget: 287932) ==================== ")
path, cost = uniform_cost_search(a, "Dist", 287932)
print("Length of Path: ", len(path),'\n')
print("Shortest path:", formatPath(path),'\n')
print("Shortest distance:", a.traceDist(path),'\n')
print("Total energy cost:", a.tracePath(path),'\n')



print("====================  Task 3: A* Search (Energy Budget: 287932) ==================== ")
path, cost = astar_search(a)
print("Length of Path: ", len(path),'\n')
print("Shortest path:", formatPath(path),'\n')
print("Shortest distance:", a.traceDist(path),'\n')
print("Total energy cost:", a.tracePath(path),'\n')
