# made by members of TeamUS
# Group-14
# Prateek Jain (2010110477)
# Pratham Sharma (2010110479)
# Prateek Shakya (2010110478)
# Pranshu Agarwal (2010110475)
# Raghav Chaturvedy (2010110759)
# Anubhav Talus (2010110113)


from heapq import *
import time
import sys


class Puzzle:

    LEFT = 'l'
    DOWN = 'd'
    UP = 'u'
    RIGHT = 'r'

    BOX_SYMBOL = '$'
    TGT_SYMBOL = '.'
    PLAYER_SYMBOL = '@'
    OBSTACLE_SYMBOL = '#'
    EMPTY_SPACE = ' '
    BOX_ON_TGT_SYMBOL = '*'
    PLAYER_ON_TGT_SYMBOL = 'p'
    CORNER_SYMBOL = '+'

    def __init__(self, filename):
        f1 = open(filename, 'r')
        rows1 = []
        cols_max = 0
        for line in f1:
            rows1.append(line)
        rows_max = len(rows1)
        f1.close()
        i = 1
        f2 = open(filename, 'r')
        for line in f2:
            if i == rows_max:
                cols_max = max(len(rows1[i-1]), cols_max)
            else:
                cols_max = max(len(rows1[i-1])-1, cols_max)
            i += 1
        f2.close()
        wr = open("anubhav.txt", "w")
        for i in range(rows_max+2):
            j = 0
            while j < cols_max + 2:
                if i == 0 or i == rows_max+1:
                    wr.write('#')
                    j += 1
                elif j == 0 or j == cols_max+1:
                    wr.write('#')
                    j += 1
                else:
                    if i == rows_max:
                        for c in range(len(rows1[i-1])):
                            wr.write(rows1[i-1][c])
                            j += 1
                        for _ in range(cols_max-len(rows1[i-1])):
                            wr.write(' ')
                            j += 1
                    else:
                        for c in range(len(rows1[i-1])-1):
                            wr.write(rows1[i-1][c])
                            j += 1
                        for _ in range(cols_max-len(rows1[i-1])+1):
                            wr.write(' ')
                            j += 1
            wr.write('\n')
        wr.close()
        f = open("anubhav.txt", 'r')
        rows = []
        for line in f:
            if len(line.strip()) > 0:
                rows.append(list(line.strip()))

        f.close()

        row_len = len(rows[0])
        for row in rows:
            assert len(row) == row_len, "Mismatch in row length"

        num_rows = len(rows)

        box_cooridnates = []
        dot_coordinates = []
        player_position = None
        possible_positions = {}

        for i in range(num_rows):
            for j in range(row_len):
                if rows[i][j] == self.BOX_SYMBOL:
                    box_cooridnates.append((i, j))
                    rows[i][j] = self.EMPTY_SPACE
                elif rows[i][j] == self.PLAYER_SYMBOL:
                    player_position = (i, j)
                    rows[i][j] = self.EMPTY_SPACE
                elif rows[i][j] == self.TGT_SYMBOL:
                    dot_coordinates.append((i, j))
                    rows[i][j] = self.EMPTY_SPACE

                elif rows[i][j] == self.BOX_ON_TGT_SYMBOL:
                    box_cooridnates.append((i, j))
                    dot_coordinates.append((i, j))
                    rows[i][j] = self.EMPTY_SPACE
                elif rows[i][j] == self.PLAYER_ON_TGT_SYMBOL:
                    player_position = (i, j)
                    dot_coordinates.append((i, j))
                    rows[i][j] = self.EMPTY_SPACE

                if rows[i][j] != self.OBSTACLE_SYMBOL:
                    possible_positions[(i, j)] = sys.maxsize

        assert len(box_cooridnates) == len(
            dot_coordinates), "Number of boxes does not match number of targets"

        self.box_cooridnates = box_cooridnates
        self.dot_coordinates = dot_coordinates
        self.player_position = player_position
        self.cursor_x = player_position[1]
        self.cursor_y = player_position[0]
        self.hash_map = rows
        self.possible_positions = possible_positions
        self.stepd_a_box = False
        self.dist_from_target = self.h_dist()

        for i in self.dist_from_target:
            for j in self.dist_from_target[i]:
                if self.dist_from_target[i][j] == sys.maxsize:
                    rows[j[0]][j[1]] = self.CORNER_SYMBOL

        self.hash_map = rows

    def create_root_node(self):
        return Node(self.box_cooridnates, self.dot_coordinates, self.cursor_x, self.cursor_y, None)

    def hash_coordinate(self, boxPosition):
        if self.hash_map[boxPosition[0]][boxPosition[1]] == self.OBSTACLE_SYMBOL:
            return True
        else:
            return False

    def possible_steps(self, boxPosition):
        steps = []
        if not self.hash_coordinate((boxPosition[0] - 1, boxPosition[1])):
            steps.append(self.LEFT)
        if not self.hash_coordinate((boxPosition[0] + 1, boxPosition[1])):
            steps.append(self.RIGHT)
        if not self.hash_coordinate((boxPosition[0], boxPosition[1] - 1)):
            steps.append(self.UP)
        if not self.hash_coordinate((boxPosition[0], boxPosition[1] + 1)):
            steps.append(self.DOWN)
        return steps

    def h_dist(self):
        dist_from_target = {}

        for goal in self.dot_coordinates:
            self.possible_positions[goal] = 0
            dist_from_target[goal] = self.possible_positions

            priority_queue = list()
            priority_queue.append(goal)

            while priority_queue:
                position = priority_queue.pop()
                actions = self.possible_steps(position)
                for action in actions:
                    if action == self.LEFT:
                        playerPosition = (position[0] - 2, position[1])
                        boxPosition = (position[0] - 1, position[1])
                    elif action == self.UP:
                        playerPosition = (position[0], position[1] - 2)
                        boxPosition = (position[0], position[1] - 1)
                    elif action == self.RIGHT:
                        playerPosition = (position[0] + 2, position[1])
                        boxPosition = (position[0] + 1, position[1])
                    elif action == self.DOWN:
                        playerPosition = (position[0], position[1] + 2)
                        boxPosition = (position[0], position[1] + 1)

                    if dist_from_target[goal][boxPosition] == sys.maxsize:
                        if not self.hash_coordinate(boxPosition):
                            if not self.hash_coordinate(playerPosition):
                                dist_from_target[goal][boxPosition] = 1 + \
                                    dist_from_target[goal][position]
                                priority_queue.append(boxPosition)

        return dist_from_target


class Node:

    OBSTACLE_SYMBOL = '#'
    CORNER_SYMBOL = '+'

    LEFT = 'l'
    DOWN = 'd'
    UP = 'u'
    RIGHT = 'r'

    def __init__(self, box_positions, dot_coordinates, cursor_x, cursor_y, action=None):

        self.dot_coordinates = dot_coordinates
        self.box_positions = box_positions

        self.cursor_y = cursor_y
        self.cursor_x = cursor_x

        self.g = 0
        self.h = 0
        self.f = 0

        self.action = action

    def __hash__(self):
        if self.box_positions is not None:
            self.box_positions.sort()

        return hash((tuple(self.box_positions), self.cursor_x, self.cursor_y, self.action))

    def __lt__(self, other):
        return self.f < other.f

    def if_solved(self):
        finished = True
        for i in self.box_positions:
            if i not in self.dot_coordinates:
                finished = False
        return finished

    def __eq__(self, other):
        return isinstance(other, Node) and self.box_positions == other.box_positions \
            and self.cursor_x == other.cursor_x and self.cursor_y \
            and self.action == other.action

    def apply_step(self, step, sokoban_map):

        box_pos = self.box_positions[:]

        if step == self.RIGHT:
            if sokoban_map.hash_map[self.cursor_y][self.cursor_x + 1] != self.OBSTACLE_SYMBOL:
                new_x = self.cursor_x + 1
                new_y = self.cursor_y
            else:
                return None

        elif step == self.LEFT:
            if sokoban_map.hash_map[self.cursor_y][self.cursor_x - 1] != self.OBSTACLE_SYMBOL:
                new_x = self.cursor_x - 1
                new_y = self.cursor_y
            else:
                return None

        elif step == self.DOWN:
            if sokoban_map.hash_map[self.cursor_y + 1][self.cursor_x] != self.OBSTACLE_SYMBOL:
                new_x = self.cursor_x
                new_y = self.cursor_y + 1
            else:
                return None

        else:
            if sokoban_map.hash_map[self.cursor_y - 1][self.cursor_x] != self.OBSTACLE_SYMBOL:
                new_x = self.cursor_x
                new_y = self.cursor_y - 1
            else:
                return None

        is_box_pushed = False
        if (new_y, new_x) not in box_pos:
            pass
        else:
            if step == self.RIGHT:
                if (sokoban_map.hash_map[new_y][new_x + 1] == self.OBSTACLE_SYMBOL) or (new_y, new_x + 1) in box_pos:
                    return None
                if sokoban_map.hash_map[new_y][new_x + 1] == self.CORNER_SYMBOL and (new_y, new_x + 1) not in sokoban_map.dot_coordinates:
                    return None
                else:
                    new_box_x = new_x + 1
                    new_box_y = new_y
                    is_box_pushed = True
            elif step == self.LEFT:
                if (sokoban_map.hash_map[new_y][new_x - 1] == self.OBSTACLE_SYMBOL) or (new_y, new_x - 1) in box_pos:
                    return None
                if sokoban_map.hash_map[new_y][new_x - 1] == self.CORNER_SYMBOL and (new_y, new_x - 1) not in sokoban_map.dot_coordinates:
                    return None
                else:
                    new_box_x = new_x - 1
                    new_box_y = new_y
                    is_box_pushed = True

            elif step == self.DOWN:
                if (sokoban_map.hash_map[new_y + 1][new_x] == self.OBSTACLE_SYMBOL) or (new_y + 1, new_x) in box_pos:
                    return None
                if sokoban_map.hash_map[new_y + 1][new_x] == self.CORNER_SYMBOL and (new_y + 1, new_x) not in sokoban_map.dot_coordinates:
                    return None
                else:
                    new_box_x = new_x
                    new_box_y = new_y + 1
                    is_box_pushed = True
            else:
                if (sokoban_map.hash_map[new_y - 1][new_x] == self.OBSTACLE_SYMBOL) or (new_y - 1, new_x) in box_pos:
                    return None
                if sokoban_map.hash_map[new_y - 1][new_x] == self.CORNER_SYMBOL and (new_y - 1, new_x) not in sokoban_map.dot_coordinates:
                    return None
                else:
                    new_box_x = new_x
                    new_box_y = new_y - 1
                    is_box_pushed = True

            box_pos.remove(((new_y, new_x)))
            box_pos.append((new_box_y, new_box_x))

        if is_box_pushed == True:
            return (new_x, new_y), box_pos, step.upper()
        else:
            return (new_x, new_y), box_pos, step

    def get_successor(self, sokoban_map):
        successors = []
        actions = [self.UP, self.RIGHT, self.DOWN, self.LEFT]
        for action in actions:
            val = self.apply_step(action, sokoban_map)
            if val is not None:
                successors.append(
                    Node(val[1], self.dot_coordinates, val[0][0], val[0][1], val[2]))

        return successors


class Sokoban:

    def __init__(self, map):
        self.map = Puzzle(map)
        self.root = self.map.create_root_node()

    def getPullDistance(self, node):
        total = 0
        for target in self.map.dot_coordinates:
            for b in node.box_positions:
                total += self.map.dist_from_target[target][b]
        return total

    def astar(self):

        traversed = set()
        priority_queue = []

        node_expanded = 1
        first_node = self.root

        heappush(priority_queue, (0, [], first_node))

        while priority_queue:
            cost, order, node = heappop(priority_queue)

            if node not in traversed:
                traversed.add(node)

            order = order + [node.action]

            if node.if_solved():
                return order[1:], node_expanded, len(priority_queue), len(traversed)

            for succ in node.get_successor(self.map):
                node_expanded += 1
                succ.g = node.g + 1
                succ.h = self.getPullDistance(succ)
                succ.f = succ.g + succ.h

                if node.if_solved():
                    return order[1:], node_expanded, len(priority_queue), len(traversed)

                if succ not in traversed:
                    heappush(priority_queue, (succ.f, order, succ))
                    traversed.add(succ)

        return None

    def uniformCost(self):

        traversed = set()
        priority_queue = []

        total_nodes = 1
        first_node = self.root

        heappush(priority_queue, (0, [], first_node))

        while priority_queue:
            cost, order, node = heappop(priority_queue)

            if node not in traversed:
                traversed.add(node)

            order = order + [node.action]

            if node.if_solved():
                return order[1:], total_nodes, len(priority_queue), len(traversed)

            for succ in node.get_successor(self.map):
                total_nodes = total_nodes + 1
                succ.f = node.f + 1

                if node.if_solved():
                    return order[1:], total_nodes, len(priority_queue), len(traversed)

                if succ not in traversed:
                    heappush(priority_queue, (succ.f, order, succ))
                    traversed.add(succ)

        return None


def call_unformCost(infl):
    begin = time.time()
    steps = Sokoban(infl).uniformCost()
    last = time.time()

    print("Solution of uniform cost search :")
    print("Solved in " + str(len(steps[0])) + " steps: " + str(steps[0]))
    print("Explored list contains the following left over nodes : " +
          str(steps[3]))
    print("No of Nodes expanded : " + str(steps[1]))
    print("Amount of Time Taken : " + str((-1)*(begin - last)) + " seconds")
    return steps[0]


def call_astar(infl):
    begin = time.time()
    steps = Sokoban(infl).astar()
    last = time.time()

    print("Solution of A* search :")
    print("Solved in " + str(len(steps[0])) + " steps: " + str(steps[0]))
    print("Explored list contains the following left over nodes : " +
          str(steps[3]))
    print("No of Nodes expanded : " + str(steps[1]))
    print("Amount of Time Taken : " + str((last - begin)) + " seconds")
    return steps[0]


def main(arguments):
    infl = arguments[0]
    outfl = arguments[1]

    print(infl)
    ansbyastar = call_astar(infl)
    print("")
    ansbyucs = call_unformCost(infl)
    print("")

    obj = open(outfl, 'w')
    str = ""
    if len(ansbyastar) < len(ansbyucs):
        for k in range(len(ansbyastar)):
            str = str + ansbyastar[k]
    else:
        for k in range(len(ansbyucs)):
            str = str + ansbyucs[k]

    obj.write(str[0:])
    obj.close()


if __name__ == '__main__':
    main(sys.argv[1:])
