# made by member of us gang

from my_map import MyMap
from heapq import *
import sys
import time


class Sokoban:

    def __init__(self, map):
        self.map = MyMap(map)
        self.root = self.map.create_root_node()

    def getPullDistance(self, node):
        sum = 0
        for goal in self.map.tgt_positions:
            for box in node.box_positions:
                sum += self.map.distance_to_goal[goal][box]
                # print(sum)
        return sum

    def astar(self):
        # Create start node
        node_expanded = 1
        start_node = self.root

        q = []
        visited = set()

        heappush(q, (0, start_node, []))

        while q:
            # Pop the element with least weight
            cost, node, path = heappop(q)

            # Check if the element is visited
            if node not in visited:
                visited.add(node)

            # Update the path
            path = path + [node.direction]

            # If found the goal
            if node.is_finished():
                return path[1:], node_expanded, len(q), len(visited)

            # Expand the node
            # Calculate the basic goal
            for child in node.get_successor(self.map):
                node_expanded += 1
                child.g = node.g + 1
                child.h = self.getPullDistance(child)
                child.f = child.g + child.h

                if node.is_finished():
                    return path[1:], node_expanded, len(q), len(visited)

                # Check if child has not been visited
                if child not in visited:
                    heappush(q, (child.f, child, path))
                    visited.add(child)

        return None

    def uniformCost(self):
        # Create start node
        node_count = 1
        start_node = self.root

        q = []
        visited = set()

        heappush(q, (0, start_node, []))

        while q:
            # Pop the element with least weight
            cost, node, path = heappop(q)

            # Check if the element is visited
            if node not in visited:
                visited.add(node)

            # Update the path
            path = path + [node.direction]

            # If found the goal
            if node.is_finished():
                return path[1:], node_count, len(q), len(visited)

            # Expand the node
            # Calculate the basic goal
            for child in node.get_successor(self.map):
                node_count += 1
                child.f = node.f + 1

                if node.is_finished():
                    return path[1:], node_count, len(q), len(visited)

                # Check if child has not been visited
                if child not in visited:
                    # print(child.f)
                    heappush(q, (child.f, child, path))
                    visited.add(child)

        return None


def execute_astar(input_map):
    start = time.time()
    search = Sokoban(input_map).astar()
    end = time.time()

    print("A* success!")
    print("Solved in " + str(len(search[0])) + " steps: " + str(search[0]))
    print("Time elapsed: " + str((end - start)) + " seconds")
    print("Nodes expanded: " + str(search[1]))
    print("Nodes left in the explored list: " + str(search[3]))

    return search[0]


def execute_ucs(input_map):
    start = time.time()
    search = Sokoban(input_map).uniformCost()
    end = time.time()

    print("UCS success!")
    print("Solved in " + str(len(search[0])) + " steps: " + str(search[0]))
    print("Time elapsed: " + str((end - start)) + " seconds")
    print("Node expanded: " + str(search[1]))
    print("Nodes left in the explored list: " + str(search[3]))

    return search[0]


def main(argslist):
    input_map = argslist[0]
    output_map = argslist[1]

    print(input_map)
    ucs_soln = execute_ucs(input_map)
    print("")
    astar_soln = execute_astar(input_map)
    print("")
    print("")

    f = open(output_map, 'w')
    output = ""
    if len(ucs_soln) > len(astar_soln):
        for i in astar_soln:
            output += i

    else:
        for i in ucs_soln:
            output += i

    f.write(output[0:])
    f.close()


if __name__ == '__main__':
    main(sys.argv[1:])
