import sys

from Models.Node import Node

max_val = sys.maxsize


class Frontier:

    def __init__(self, node):
        self.list = [node]

    def size(self):
        return len(self.list)

    def pop_frontier(self):
        if self.size() == 0:
            return None
        max_val1 = max_val
        max_values = []
        for node in self.list:
            key = node.path_cost
            path = node.path
            if key == max_val1:
                max_values.append(path)
            elif key < max_val1:
                max_val1 = key
                max_values.clear()
                max_values.append(path)

        max_values = sorted(max_values, key=lambda x: x[-1])
        desired_value = max_values[0]
        nodeToRemove = 0
        node = 0
        for node in self.list:
            if node.path_cost == max_val1 and node.path == desired_value:
                nodeToRemove = node
                break
        self.list.remove(nodeToRemove)
        return node

    def pop(self, index):
        return self.list.pop(index)

    def getNewParams(self, nodeState):
        for i in range(self.size()):
            cost, path = self.list[i].path_cost, self.list[i].path
            if path[-1] == nodeState:
                return True, i, cost, path

        return False, None, None, None

    def append(self, node):
        self.list.append(node)
