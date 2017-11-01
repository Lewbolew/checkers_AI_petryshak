import random
from sys import maxsize  # infinity (a really big number)
from libcheckers.movement import *
import time


class Node(object):
    """
    Node for building minMax tree.
    """
    def __init__(self, player, board,max_player, move=None):
        self.player = player
        self.max_player = max_player
        self.children = list()
        self.move = move
        self.board = board
        self.value = 0

    def heuristic(self):
        """
        Calculate heuristic value of the current state
        :return: heuristic value(int)
        """
        # Giving additional points for the position in the board
        values_for_position = dict.fromkeys([6,16,26,36,46,1,2,3,4,5,15,25,35,45,47,48,49,50],1.4)
        values_for_position.update(dict.fromkeys([7,8,9,10,11,21,31,41,10,20,30,40, 41,42,43,44], 1.3))
        values_for_position.update(dict.fromkeys([12,13,14,17,18,19,22,23,24,27,28,29,32,33,34,37,38,39], 1.2))
        values_for_position.update(dict.fromkeys([18,19,22,23,28,29,32,33], 1.1))
        list_of_pieces_player = self.board.get_player_squares(self.max_player)
        list_of_pieces_other_player = self.board.get_player_squares(self.max_player % 2 + 1)
        scores_position_player = [values_for_position[x] for x in list_of_pieces_player]
        scores_position_other_player = [values_for_position[x] for x in list_of_pieces_other_player]

        # Giving additional points for the type of the piece
        pawns_owner_class = list(zip(self.board.owner, self.board.piece_class))
        scores_for_piece_type_player = [owner_class[1] for owner_class in pawns_owner_class if owner_class[0]
                                            == self.max_player]
        scores_for_piece_type_other_player = [owner_class[1] for owner_class in pawns_owner_class if owner_class[0]
                                                  == (self.max_player % 2 + 1)]

        final_scores_player = [a*b for a,b in zip(scores_position_player,scores_for_piece_type_player)]
        final_scores_other_player = [a*b for a,b in zip(scores_position_other_player,
                                                        scores_for_piece_type_other_player)]


        self.value = sum(final_scores_player) - sum(final_scores_other_player)
        return self.value

def min_max(node, depth, maximizing_player):
    """
    MinMax algo, which build the tree and return the optimal turn
    :param node: Node
    :param depth: depth of the tree
    :param maximizing_player:
    :return: heuristic value
    """
    player = node.max_player if maximizing_player else (node.max_player % 2 + 1)
    if depth == 0 or node.board.check_game_over(player):
        node.value = node.heuristic()
        return node.value

    available_moves = node.board.get_available_moves(player)

    if maximizing_player:
        best_value = -maxsize
        for move in available_moves:
            child = Node(player, move.apply(node.board),node.max_player, move)
            node.children.append(child)
            v = min_max(child, depth - 1, False)
            best_value = max(best_value, v)
        node.value = best_value
        return best_value
    else:
        best_value = maxsize
        for move in available_moves:
            child = Node(player, move.apply(node.board),node.max_player, move)
            node.children.append(child)
            v = min_max(child, depth - 1, True)
            best_value = min(best_value, v)
        node.value = best_value
        return best_value


def alpha_beta(node, depth, a, b, maximizing_player):
    """
    Function which realize alpha-beta pruning algo(modification of mim_max algo.
    :param node: Node
    :param depth: depth(int)
    :param a: alpha
    :param b: beta
    :param maximizing_player: max_player
    :return: best heuristic value(int)
    """
    player = node.max_player if maximizing_player else (node.max_player % 2 + 1)
    if depth == 0 or node.board.check_game_over(player):
        node.value = node.heuristic()
        return node.value

    if maximizing_player:
        v = -maxsize
        moves = node.board.get_available_moves(player)
        for move in moves:
            new_board = move.apply(node.board)
            child = Node(player % 2 + 1,new_board,node.max_player,move)
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
            child = Node(player % 2 + 1,new_board,node.max_player, move)
            node.children.append(child)
            v = min(v, alpha_beta(child, depth - 1, a, b, True))
            b = min(b, v)
            if b<= a:
                break
        node.value = v
        return v

def pick_next_move(board, player):
    origin = Node(player, board, player)
    best_turn_value = alpha_beta(origin, 5, -maxsize, maxsize, True)
    best_turns = [child.move for child in origin.children if child.value == best_turn_value]
    return random.choice(best_turns)

