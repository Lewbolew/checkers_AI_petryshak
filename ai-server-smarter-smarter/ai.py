import random
from sys import maxsize  # infinity (a really big number)
from libcheckers.movement import *
import time


class Node(object):
    def __init__(self, player, board, max_player, move=None):
        self.player = player
        self.max_player = max_player
        self.children = list()
        self.move = move
        self.board = board
        self.value = 0

    def heuristic(self):
        self.value = len(self.board.get_player_squares(self.max_player)) - \
                     len(self.board.get_player_squares(self.max_player % 2 + 1))

        return self.value

    def heuristic_position(self):
        """
        Heuristic function which penalize on positions of checkers
        :return:
        """
        values = {0.4: [6, 16, 26, 36, 46, 2, 3, 4, 5, 15, 25, 35, 45, 47, 48, 49, 50],
                  0.3: [7, 8, 9, 10, 11, 21, 31, 41, 10, 20, 30, 40],
                  0.2: [12, 13, 14, 24, 34, 32, 22],
                  0.1: [18, 19, 28, 29]}
        list_of_pieces = self.board.get_player_squares(self.player)
        for piece in list_of_pieces:
            pass
        return


def min_max(node, depth, maximizing_player):
    player = node.max_player if maximizing_player else (node.max_player % 2 + 1)
    if depth == 0 or node.board.check_game_over(player):
        node.value = node.heuristic()
        return node.value

    available_moves = node.board.get_available_moves(player)

    if maximizing_player:
        best_value = -maxsize
        for move in available_moves:
            child = Node(player, move.apply(node.board), node.max_player, move)
            node.children.append(child)
            v = min_max(child, depth - 1, False)
            best_value = max(best_value, v)
        node.value = best_value
        return best_value

    else:
        best_value = maxsize
        for move in available_moves:
            child = Node(player, move.apply(node.board), node.max_player, move)
            node.children.append(child)
            v = min_max(child, depth - 1, True)
            best_value = min(best_value, v)
        node.value = best_value
        return best_value


def alpha_beta(node, depth, a, b, maximizing_player):
    player = node.max_player if maximizing_player else (node.max_player % 2 + 1)
    if depth == 0 or node.board.check_game_over(player):
        node.value = node.heuristic()
        return node.value

    if maximizing_player:
        v = -maxsize
        moves = node.board.get_available_moves(player)
        for move in moves:
            new_board = move.apply(node.board)
            child = Node(player % 2 + 1, new_board, node.max_player, move)
            node.children.append(child)
            v = max(v, alpha_beta(child, depth - 1, a, b, False))
            a = max(a, v)
            if b <= a:
                break
        node.value = v
        return v
    else:
        v = maxsize
        moves = node.board.get_available_moves(player)
        for move in moves:
            new_board = move.apply(node.board)
            child = Node(player % 2 + 1, new_board, node.max_player, move)
            node.children.append(child)
            v = min(v, alpha_beta(child, depth - 1, a, b, True))
            b = min(b, v)
            if b <= a:
                break
        node.value = v
        return v


def pick_next_move(board, player):
    origin = Node(player, board, player)
    best_turn_value = min_max(origin, 4, True)
    # best_turn_value = alpha_beta(origin, 5, -maxsize, maxsize, True)
    best_turns = [child.move for child in origin.children if child.value == best_turn_value]
    return random.choice(best_turns)
