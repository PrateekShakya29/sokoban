from copy import deepcopy


class Node:

    LEFT = 'l'
    RIGHT = 'r'
    UP = 'u'
    DOWN = 'd'

    OBSTACLE_SYMBOL = '#'
    CORNER_SYMBOL = '+'

    def __init__(self, box_positions, tgt_positions, player_x, player_y, direction=None):

        self.box_positions = box_positions
        self.tgt_positions = tgt_positions
        self.player_x = player_x
        self.player_y = player_y

        # information about the previous node
        self.direction = direction

        # weight of the node for informed search
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

    def __hash__(self):
        if self.box_positions is not None:
            self.box_positions.sort()

        return hash((tuple(self.box_positions), self.player_x, self.player_y, self.direction))

    def __eq__(self, other):
        return isinstance(other, Node) and self.box_positions == other.box_positions \
            and self.player_x == other.player_x and self.player_y \
            and self.direction == other.direction

    def is_finished(self):
        finished = True
        for i in self.box_positions:
            if i not in self.tgt_positions:
                finished = False
        return finished

    def get_successor(self, sokoban_map):
        successors = []
        directions = [self.UP, self.RIGHT, self.DOWN, self.LEFT]
        for direction in directions:
            val = self.apply_move(direction, sokoban_map)
            if val is not None:
                successors.append(
                    Node(val[1], self.tgt_positions, val[0][0], val[0][1], val[2]))

        return successors

    def apply_move(self, move, sokoban_map):
        """
        Apply a player move to the map.
        :param move: 'L', 'R', 'U' or 'D'
        :return: True if move was successful, false if move could not be completed
        """
        # basic obstacle check
        box_pos = self.box_positions[:]
        if move == self.LEFT:
            if sokoban_map.obstacle_map[self.player_y][self.player_x - 1] == self.OBSTACLE_SYMBOL:
                return None
            else:
                new_x = self.player_x - 1
                new_y = self.player_y

        elif move == self.RIGHT:
            if sokoban_map.obstacle_map[self.player_y][self.player_x + 1] == self.OBSTACLE_SYMBOL:
                return None
            else:
                new_x = self.player_x + 1
                new_y = self.player_y

        elif move == self.UP:
            if sokoban_map.obstacle_map[self.player_y - 1][self.player_x] == self.OBSTACLE_SYMBOL:
                return None
            else:
                new_x = self.player_x
                new_y = self.player_y - 1

        else:
            if sokoban_map.obstacle_map[self.player_y + 1][self.player_x] == self.OBSTACLE_SYMBOL:
                return None
            else:
                new_x = self.player_x
                new_y = self.player_y + 1

        # pushed box collision check
        is_box_pushed = False
        if (new_y, new_x) in box_pos:
            if move == self.LEFT:
                if (sokoban_map.obstacle_map[new_y][new_x - 1] == self.OBSTACLE_SYMBOL) or (new_y, new_x - 1) in box_pos:
                    return None
                if sokoban_map.obstacle_map[new_y][new_x - 1] == self.CORNER_SYMBOL and (new_y, new_x - 1) not in sokoban_map.tgt_positions:
                    return None
                else:
                    new_box_x = new_x - 1
                    new_box_y = new_y
                    is_box_pushed = True

            elif move == self.RIGHT:
                if (sokoban_map.obstacle_map[new_y][new_x + 1] == self.OBSTACLE_SYMBOL) or (new_y, new_x + 1) in box_pos:
                    return None
                if sokoban_map.obstacle_map[new_y][new_x + 1] == self.CORNER_SYMBOL and (new_y, new_x + 1) not in sokoban_map.tgt_positions:
                    return None
                else:
                    new_box_x = new_x + 1
                    new_box_y = new_y
                    is_box_pushed = True

            elif move == self.UP:
                if (sokoban_map.obstacle_map[new_y - 1][new_x] == self.OBSTACLE_SYMBOL) or (new_y - 1, new_x) in box_pos:
                    return None
                if sokoban_map.obstacle_map[new_y - 1][new_x] == self.CORNER_SYMBOL and (new_y - 1, new_x) not in sokoban_map.tgt_positions:
                    return None
                else:
                    new_box_x = new_x
                    new_box_y = new_y - 1
                    is_box_pushed = True

            else:
                if (sokoban_map.obstacle_map[new_y + 1][new_x] == self.OBSTACLE_SYMBOL) or (new_y + 1, new_x) in box_pos:
                    return None
                if sokoban_map.obstacle_map[new_y + 1][new_x] == self.CORNER_SYMBOL and (new_y + 1, new_x) not in sokoban_map.tgt_positions:
                    return None
                else:
                    new_box_x = new_x
                    new_box_y = new_y + 1
                    is_box_pushed = True

            # update box position
            # self.box_pos.remove((new_y, new_x))
            # self.box_pos.append((new_box_y, new_box_x))
            box_pos.remove(((new_y, new_x)))
            box_pos.append((new_box_y, new_box_x))

        # update player position
        # self.player_x = new_x
        # self.player_y = new_y
        if is_box_pushed == True:
            return (new_x, new_y), box_pos, move.upper()
        else:
            return (new_x, new_y), box_pos, move
