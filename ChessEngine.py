import numpy as np
import time
import itertools
import copy


def _reverse(char_t):
    if char_t == 1:
        return "a"
    if char_t == 2:
        return "b"
    if char_t == 3:
        return "c"
    if char_t == 4:
        return "d"
    if char_t == 5:
        return "e"
    if char_t == 6:
        return "f"
    if char_t == 7:
        return "g"
    if char_t == 8:
        return "h"
    if char_t == "a":
        return 1
    if char_t == "b":
        return 2
    if char_t == "c":
        return 3
    if char_t == "d":
        return 4
    if char_t == "e":
        return 5
    if char_t == "f":
        return 6
    if char_t == "g":
        return 7
    if char_t == "h":
        return 8



class ChessBoard:
    moves = 0
    color_tm = "K"
    files= " abcdefgh "
    squares = [] # inside [ [rank, file, "name", False], [rank, file, "name"], [rank, file, "name"],
                 #         [rank, file, "name"],

    def fill_board(self):
        for rank in range(8,0,-1):

            for file in "hgfedcba":
               self.squares.append([rank, file, ""])
            # self.squares.append(_file)

    def evaluate(self):

        white = 0
        black = 0

        P = 100
        B = 300
        N = 300
        R = 500
        Q = 900

        for square in self.squares:
            if square[2].isupper() == True:

                if square[2].upper() == "P":
                    white += P
                if square[2].upper() == "B":
                    white += B
                if square[2].upper() == "N":
                    white += N
                if square[2].upper() == "R":
                    white += R
                if square[2].upper() == "Q":
                    white += Q
            if square[2].isupper() == False:
                if square[2].upper() == "P":
                    black += P
                if square[2].upper() == "B":
                    black += B
                if square[2].upper() == "N":
                    black += N
                if square[2].upper() == "R":
                    black += R
                if square[2].upper() == "Q":
                    black += Q
        return [white, black]

    def get_id_from_pos(self, rank, file):
        piece_id = 0
        find = False
        for square in self.squares:
            if square[0] == rank and square[1] == file:
                find = True
                break
            piece_id += 1
        if find == False:
            return "Piece Not found"

        return piece_id

    def import_game(self, fen_game):
        ranks = fen_game.split("/")
        # print(np.array(ranks))

        id = 0

        letters = 'abcdefgh'

        for rank, rank_n in zip(ranks, range(8, 0, -1)):
            letters_id = 0
            for piece in rank:
                try:
                    empty_squares = int(piece)
                    for emp in range(empty_squares):
                        self.squares[id] = [rank_n, letters[letters_id], " ", False]

                        letters_id += 1
                        id += 1
                except:

                    self.squares[id] = [rank_n, letters[letters_id], piece, False]

                    id += 1
                    letters_id += 1

            rank_n += 1

    def show_chessboard(self):
        print("==============================================")
        if self.color_tm == "K":
            print(f"Stats: \nNow is whites turn to move\nMoves count: {self.moves}")
        else:
            print(f"Stats: \nNow is blacks turn to move\nMoves count: {self.moves}")

        id = 0
        for numb in range(9, -1, -1):
            row = ""
            for char in " abcdefgh ":
                if numb == 9 or numb == 0:
                    row += str(char)
                elif char == " ":
                    row += str(numb)
                else:
                    row += self.squares[id][2]
                    id += 1
            print(row)


        print("==============================================")

    def is_square_empty(self, _rank, _file):

        for square in self.squares:
            if square[0] == _rank and square[1] == _file:
                if square[2] != " ":
                    return False
                else:
                    return True

    def is_enemy_in_square(self, _rank, _file, color):
        if _file == " ":
            return False
        if _rank == 0 or _rank == 9:
            return False


        for square in self.squares:
            if square[0] == _rank and square[1] == _file:

                if square[2] == " ":
                    return False

                if color.isupper() != square[2].isupper():

                    return True
                else:
                    return False

    def is_king_in_check(self, color):

        king = None
        if color == "K":
            for square in self.squares:
                if square[2] == 'K':
                    king = self.squares[self.get_id_from_pos(self, square[0], square[1])]
                    break
            for square in self.squares:
                if square[2] == " ":
                    continue

                if square[2].isupper() != color.isupper():
                    # print(square)
                    for attacked_square in self.find_legal_moves(self, square[0], square[1]):
                        # print(attacked_square)
                        if [king[0], king[1]] == attacked_square[1]:
                            print("White king is in check!")
                            return True
            return False
        if color == "k":
            for square in self.squares:

                if square[2] == 'k':
                    king = self.squares[self.get_id_from_pos(self, square[0], square[1])]

                    break
            for square in self.squares:
                if square[2] == " ":
                    continue
                if square[2].isupper() != color.isupper():
                    # print(square)
                    for attacked_square in self.find_legal_moves(self, square[0], square[1]):
                        # print(attacked_square)
                        if [king[0], king[1]] == attacked_square[1]:
                            print("Black king is in check!")
                            return True
            return False

    def find_legal_moves(self, _rank, _file):
        piece_id = self.get_id_from_pos(self, _rank, _file)

        piece_e = self.squares[piece_id]

        legal_moves = []


        if piece_e[2] == "P":
            next_square = self.is_square_empty(self, piece_e[0] + 1, piece_e[1])

            if piece_e[3] == False:
                if next_square == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [piece_e[0]+1, piece_e[1]]])
                    if self.is_square_empty(self, piece_e[0] + 2, piece_e[1]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [piece_e[0] + 2, piece_e[1]]])

            if piece_e[3] == True:
                if next_square == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [piece_e[0] + 1, piece_e[1]]])


            if self.is_enemy_in_square(self, piece_e[0]+1,
                                       self.files[self.files.index(piece_e[1])+1], piece_e[2]) == True:
                legal_moves.append([[piece_e[0], piece_e[1]],
                                    [piece_e[0] + 1, self.files[self.files.index(piece_e[1])+1]]])

            if self.is_enemy_in_square(self, piece_e[0] + 1,
                                       self.files[self.files.index(piece_e[1]) - 1], piece_e[2]) == True:
                legal_moves.append([[piece_e[0], piece_e[1]],
                                    [piece_e[0] + 1,
                                     self.files[self.files.index(piece_e[1]) - 1]]])
        if piece_e[2] == "p":
            next_square = self.is_square_empty(self, piece_e[0] - 1, piece_e[1])

            if piece_e[3] == False:
                if next_square == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [piece_e[0]-1, piece_e[1]]])
                    if self.is_square_empty(self, piece_e[0] - 2, piece_e[1]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [piece_e[0] - 2, piece_e[1]]])

            if piece_e[3] == True:
                if next_square == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [piece_e[0] - 1, piece_e[1]]])


            if self.is_enemy_in_square(self, piece_e[0]-1,
                                       self.files[self.files.index(piece_e[1])+1], piece_e[2]) == True:
                legal_moves.append([[piece_e[0], piece_e[1]],
                                    [piece_e[0] - 1, self.files[self.files.index(piece_e[1])+1]]])

            if self.is_enemy_in_square(self, piece_e[0] - 1,
                                       self.files[self.files.index(piece_e[1]) - 1], piece_e[2]) == True:
                legal_moves.append([[piece_e[0], piece_e[1]],
                                    [piece_e[0] - 1,
                                     self.files[self.files.index(piece_e[1]) - 1]]])
        if piece_e[2] == "R":
            for file_up in range(piece_e[0] + 1, 9):
                if self.is_square_empty(self, file_up, piece_e[1]) == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [file_up, piece_e[1]]])
                else:
                    if self.is_enemy_in_square(self, file_up, piece_e[1],
                                               piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [file_up, piece_e[1]]])
                    break

            for file_down in range(piece_e[0] - 1, 0, -1):
                if self.is_square_empty(self, file_down, piece_e[1]) == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [file_down, piece_e[1]]])
                else:
                    if self.is_enemy_in_square(self, file_down, piece_e[1],
                                               piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [file_down, piece_e[1]]])
                    break

            for rank_right in self.files[self.files.index(piece_e[1].lower()) + 1:]:

                if self.is_square_empty(self, piece_e[0], rank_right) == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [piece_e[0], rank_right]])
                else:
                    if self.is_enemy_in_square(self, piece_e[0], rank_right,
                                               piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [piece_e[0], rank_right]])
                    break

            # print(list(reversed(self.files[1:self.files.index(piece_e[1])])))

            for rank_left in list(reversed(self.files[1:self.files.index(piece_e[1])])):

                if self.is_square_empty(self, piece_e[0], rank_left) == True:

                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [piece_e[0], rank_left]])
                else:
                    if self.is_enemy_in_square(self, piece_e[0], rank_left,
                                               piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [piece_e[0], rank_left]])
                    break
        if piece_e[2] == "r":
            for file_up in range(piece_e[0] + 1, 9):
                if self.is_square_empty(self, file_up, piece_e[1]) == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [file_up, piece_e[1]]])
                else:
                    if self.is_enemy_in_square(self, file_up, piece_e[1],
                                               piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [file_up, piece_e[1]]])
                    break

            for file_down in range(piece_e[0] - 1, 0, -1):
                if self.is_square_empty(self, file_down, piece_e[1]) == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [file_down, piece_e[1]]])
                else:
                    if self.is_enemy_in_square(self, file_down, piece_e[1],
                                               piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [file_down, piece_e[1]]])
                    break

            for rank_right in self.files[self.files.index(piece_e[1].lower()) + 1:]:

                if self.is_square_empty(self, piece_e[0], rank_right) == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [piece_e[0], rank_right]])
                else:
                    if self.is_enemy_in_square(self, piece_e[0], rank_right,
                                               piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [piece_e[0], rank_right]])
                    break

            for rank_left in list(reversed(self.files[1:self.files.index(piece_e[1])])):

                if self.is_square_empty(self, piece_e[0], rank_left) == True:

                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [piece_e[0], rank_left]])
                else:
                    if self.is_enemy_in_square(self, piece_e[0], rank_left,
                                               piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [piece_e[0], rank_left]])
                    break
        if piece_e[2] == "B":

            for rank, file in zip(range(piece_e[0] + 1, 9),
                                  range(_reverse(piece_e[1]) + 1, 9)):

                file = _reverse(file)

                if self.is_square_empty(self, rank, file) == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [rank, file]])
                else:
                    if self.is_enemy_in_square(self, rank, file, piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [rank, file]])
                    break

            for rank, file in zip(range(piece_e[0] + 1, 9),
                                  range(_reverse(piece_e[1]) - 1, 0, -1)):
                file = _reverse(file)

                if self.is_square_empty(self, rank, file) == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [rank, file]])
                else:
                    if self.is_enemy_in_square(self, rank, file, piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [rank, file]])
                    break

            for rank, file in zip(range(piece_e[0] - 1, 0, -1),
                                  range(_reverse(piece_e[1]) - 1, 0, -1)):
                file = _reverse(file)


                if self.is_square_empty(self, rank, file) == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [rank, file]])
                else:
                    if self.is_enemy_in_square(self, rank, file, piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [rank, file]])
                    break

            for rank, file in zip(range(piece_e[0] - 1, 0, -1),
                                  range(_reverse(piece_e[1]) + 1, 9)):
                file = _reverse(file)

                if self.is_square_empty(self, rank, file) == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [rank, file]])
                else:
                    if self.is_enemy_in_square(self, rank, file, piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [rank, file]])
                    break
        if piece_e[2] == "b":

            for rank, file in zip(range(piece_e[0] + 1, 9),
                                  range(_reverse(piece_e[1]) + 1, 9)):

                file = _reverse(file)

                if self.is_square_empty(self, rank, file) == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [rank, file]])
                else:
                    if self.is_enemy_in_square(self, rank, file, piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [rank, file]])
                    break

            for rank, file in zip(range(piece_e[0] + 1, 9),
                                  range(_reverse(piece_e[1]) - 1, 0, -1)):
                file = _reverse(file)

                if self.is_square_empty(self, rank, file) == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [rank, file]])
                else:
                    if self.is_enemy_in_square(self, rank, file, piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [rank, file]])
                    break

            for rank, file in zip(range(piece_e[0] - 1, 0, -1),
                                  range(_reverse(piece_e[1]) - 1, 0, -1)):
                file = _reverse(file)

                if self.is_square_empty(self, rank, file) == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [rank, file]])
                else:
                    if self.is_enemy_in_square(self, rank, file, piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [rank, file]])
                    break

            for rank, file in zip(range(piece_e[0] - 1, 0, -1),
                                  range(_reverse(piece_e[1]) + 1, 9)):
                file = _reverse(file)

                if self.is_square_empty(self, rank, file) == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [rank, file]])
                else:
                    if self.is_enemy_in_square(self, rank, file, piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [rank, file]])
                    break
        if piece_e[2] == "Q":
            for rank, file in zip(range(piece_e[0] + 1, 9),
                                  range(_reverse(piece_e[1]) + 1, 9)):

                file = _reverse(file)

                if self.is_square_empty(self, rank, file) == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [rank, file]])
                else:
                    if self.is_enemy_in_square(self, rank, file, piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [rank, file]])
                    break

            for rank, file in zip(range(piece_e[0] + 1, 9),
                                  range(_reverse(piece_e[1]) - 1, 0, -1)):
                file = _reverse(file)

                if self.is_square_empty(self, rank, file) == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [rank, file]])
                else:
                    if self.is_enemy_in_square(self, rank, file, piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [rank, file]])
                    break

            for rank, file in zip(range(piece_e[0] - 1, 0, -1),
                                  range(_reverse(piece_e[1]) - 1, 0, -1)):
                file = _reverse(file)

                if self.is_square_empty(self, rank, file) == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [rank, file]])
                else:
                    if self.is_enemy_in_square(self, rank, file, piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [rank, file]])
                    break

            for rank, file in zip(range(piece_e[0] - 1, 0, -1),
                                  range(_reverse(piece_e[1]) + 1, 9)):
                file = _reverse(file)

                if self.is_square_empty(self, rank, file) == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [rank, file]])
                else:
                    if self.is_enemy_in_square(self, rank, file, piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [rank, file]])
                    break
            for file_up in range(piece_e[0] + 1, 9):
                if self.is_square_empty(self, file_up, piece_e[1]) == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [file_up, piece_e[1]]])
                else:
                    if self.is_enemy_in_square(self, file_up, piece_e[1],
                                               piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [file_up, piece_e[1]]])
                    break

            for file_down in range(piece_e[0] - 1, 0, -1):
                if self.is_square_empty(self, file_down, piece_e[1]) == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [file_down, piece_e[1]]])
                else:
                    if self.is_enemy_in_square(self, file_down, piece_e[1],
                                               piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [file_down, piece_e[1]]])
                    break

            for rank_right in self.files[self.files.index(piece_e[1].lower()) + 1:]:

                if self.is_square_empty(self, piece_e[0], rank_right) == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [piece_e[0], rank_right]])
                else:
                    if self.is_enemy_in_square(self, piece_e[0], rank_right,
                                               piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [piece_e[0], rank_right]])
                    break

            for rank_left in list(reversed(self.files[:self.files.index(piece_e[1]) - 1])):

                if self.is_square_empty(self, piece_e[0], rank_left) == True:

                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [piece_e[0], rank_left]])
                else:
                    if self.is_enemy_in_square(self, piece_e[0], rank_left,
                                               piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [piece_e[0], rank_left]])
                    break
        if piece_e[2] == "q":
            for rank, file in zip(range(piece_e[0] + 1, 9),
                                  range(_reverse(piece_e[1]) + 1, 9)):

                file = _reverse(file)

                if self.is_square_empty(self, rank, file) == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [rank, file]])
                else:
                    if self.is_enemy_in_square(self, rank, file, piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [rank, file]])
                    break

            for rank, file in zip(range(piece_e[0] + 1, 9),
                                  range(_reverse(piece_e[1]) - 1, 0, -1)):
                file = _reverse(file)

                if self.is_square_empty(self, rank, file) == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [rank, file]])
                else:
                    if self.is_enemy_in_square(self, rank, file, piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [rank, file]])
                    break

            for rank, file in zip(range(piece_e[0] - 1, 0, -1),
                                  range(_reverse(piece_e[1]) - 1, 0, -1)):
                file = _reverse(file)

                if self.is_square_empty(self, rank, file) == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [rank, file]])
                else:
                    if self.is_enemy_in_square(self, rank, file, piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [rank, file]])
                    break

            for rank, file in zip(range(piece_e[0] - 1, 0, -1),
                                  range(_reverse(piece_e[1]) + 1, 9)):
                file = _reverse(file)

                if self.is_square_empty(self, rank, file) == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [rank, file]])
                else:
                    if self.is_enemy_in_square(self, rank, file, piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [rank, file]])
                    break
            for file_up in range(piece_e[0] + 1, 9):
                if self.is_square_empty(self, file_up, piece_e[1]) == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [file_up, piece_e[1]]])
                else:
                    if self.is_enemy_in_square(self, file_up, piece_e[1],
                                               piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [file_up, piece_e[1]]])
                    break

            for file_down in range(piece_e[0] - 1, 0, -1):
                if self.is_square_empty(self, file_down, piece_e[1]) == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [file_down, piece_e[1]]])
                else:
                    if self.is_enemy_in_square(self, file_down, piece_e[1],
                                               piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [file_down, piece_e[1]]])
                    break

            for rank_right in self.files[self.files.index(piece_e[1].lower()) + 1:]:

                if self.is_square_empty(self, piece_e[0], rank_right) == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [piece_e[0], rank_right]])
                else:
                    if self.is_enemy_in_square(self, piece_e[0], rank_right,
                                               piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [piece_e[0], rank_right]])
                    break

            for rank_left in list(reversed(self.files[:self.files.index(piece_e[1]) - 1])):

                if self.is_square_empty(self, piece_e[0], rank_left) == True:

                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [piece_e[0], rank_left]])
                else:
                    if self.is_enemy_in_square(self, piece_e[0], rank_left,
                                               piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [piece_e[0], rank_left]])
                    break
        if piece_e[2] == "K":
            squares = []
            squares.append([piece_e[0] - 1, _reverse(piece_e[1])])
            squares.append([piece_e[0] - 1, _reverse(piece_e[1]) - 1])
            squares.append([piece_e[0] - 1, _reverse(piece_e[1]) + 1])
            squares.append([piece_e[0], _reverse(piece_e[1]) + 1])
            squares.append([piece_e[0], _reverse(piece_e[1]) - 1])
            squares.append([piece_e[0] + 1, _reverse(piece_e[1])])
            squares.append([piece_e[0] + 1, _reverse(piece_e[1]) - 1])
            squares.append([piece_e[0] + 1, _reverse(piece_e[1]) + 1])

            for move in squares:
                if self.is_square_empty(self, move[0], _reverse(move[1])) == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [move[0], _reverse(move[1])]])
                else:
                    if self.is_enemy_in_square(self, move[0], _reverse(move[1]), piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [move[0], _reverse(move[1])]])

            king = piece_e
            if king[3] == False:
                for file in self.files[self.files.index(king[1]) + 1:len(self.files) - 1]:

                    if self.squares[self.get_id_from_pos(self, king[0], file)][2] == " ":
                        continue
                    elif self.squares[self.get_id_from_pos(self, king[0], file)][2] == "R":

                        if self.squares[self.get_id_from_pos(self, king[0], file)][3] == False:
                            legal_moves.append([[piece_e[0], piece_e[1]],
                                                [king[0], self.files[self.files.index(king[1]) + 2]]])
                    else:
                        break


                for file in reversed(self.files[1 : self.files.index(king[1]) - 1]):
                    print(king[0], file)
                    if self.squares[self.get_id_from_pos(self, king[0], file)][2] == " ":
                        continue
                    elif self.squares[self.get_id_from_pos(self, king[0], file)][2] == "R":

                        if self.squares[self.get_id_from_pos(self, king[0], file)][3] == False:
                            legal_moves.append([[piece_e[0], piece_e[1]],
                                                [king[0], self.files[self.files.index(king[1]) - 2]]])
                    else:
                        break
        if piece_e[2] == "k":
            squares = []
            squares.append([piece_e[0] - 1, _reverse(piece_e[1])  ])
            squares.append([piece_e[0] - 1, _reverse(piece_e[1])-1])
            squares.append([piece_e[0] - 1, _reverse(piece_e[1])+1])
            squares.append([piece_e[0], _reverse(piece_e[1])+1])
            squares.append([piece_e[0], _reverse(piece_e[1])-1])
            squares.append([piece_e[0] + 1, _reverse(piece_e[1])])
            squares.append([piece_e[0] + 1, _reverse(piece_e[1])-1])
            squares.append([piece_e[0] + 1, _reverse(piece_e[1])+1])


            for move in squares:
                if self.is_square_empty(self, move[0], _reverse(move[1])) == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [move[0], _reverse(move[1])]])
                else:
                    if self.is_enemy_in_square(self, move[0], _reverse(move[1]), piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [move[0], _reverse(move[1])]])


            #castling
        if piece_e[2] == "N":

            squares = []

            squares.append([piece_e[0]+1, _reverse(piece_e[1])+2])
            squares.append([piece_e[0]+1, _reverse(piece_e[1])-2])
            squares.append([piece_e[0]-1, _reverse(piece_e[1])-2])
            squares.append([piece_e[0]-1, _reverse(piece_e[1])+2])
            squares.append([piece_e[0]+2, _reverse(piece_e[1])+1])
            squares.append([piece_e[0]-2, _reverse(piece_e[1])-1])
            squares.append([piece_e[0]+2, _reverse(piece_e[1])-1])
            squares.append([piece_e[0]-2, _reverse(piece_e[1])+1])

            for move in squares:
                if self.is_square_empty(self, move[0], _reverse(move[1])) == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [move[0], _reverse(move[1])]])
                else:
                    if self.is_enemy_in_square(self, move[0], _reverse(move[1]), piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [rank, file]])
        if piece_e[2] == "n":

            squares = []

            squares.append([piece_e[0]+1, _reverse(piece_e[1])+2])
            squares.append([piece_e[0]+1, _reverse(piece_e[1])-2])
            squares.append([piece_e[0]-1, _reverse(piece_e[1])-2])
            squares.append([piece_e[0]-1, _reverse(piece_e[1])+2])
            squares.append([piece_e[0]+2, _reverse(piece_e[1])+1])
            squares.append([piece_e[0]-2, _reverse(piece_e[1])-1])
            squares.append([piece_e[0]+2, _reverse(piece_e[1])-1])
            squares.append([piece_e[0]-2, _reverse(piece_e[1])+1])

            for move in squares:
                if self.is_square_empty(self, move[0], _reverse(move[1])) == True:
                    legal_moves.append([[piece_e[0], piece_e[1]],
                                        [move[0], _reverse(move[1])]])
                else:
                    if self.is_enemy_in_square(self, move[0], _reverse(move[1]), piece_e[2]) == True:
                        legal_moves.append([[piece_e[0], piece_e[1]],
                                            [move[0], _reverse(move[1])]])
        # print(np.array(legal_moves))

        return legal_moves

    def make_move(self, to_parse):


        backup_squares = copy.deepcopy(self.squares)

        print("making move")
        square_from = self.squares[self.get_id_from_pos(self, int(to_parse[1]), to_parse[0])]
        square_to = self.squares[self.get_id_from_pos(self, int(to_parse[3]), to_parse[2])]


        if square_from[2].isupper() != self.color_tm.isupper():
            print("It is not your turn to move")
            return


        find_legal_move = False




        legal_moves = self.find_legal_moves(self, square_from[0], square_from[1])



        for legal_move in legal_moves:

            if [square_to[0], square_to[1]] == legal_move[1]:

                if abs(_reverse(square_from[1]) - _reverse(square_to[1])) >= 2:
                    if square_from[2].upper() == "K":

                        if square_to[1] in self.files[4:]:
                            self.squares[self.get_id_from_pos(self, 1, "h")][2], self.squares[
                                self.get_id_from_pos(self, 1, self.files[self.files.index(square_from[1]) + 1])][
                                2] = " ", self.squares[self.get_id_from_pos(self, 1, "h")][2]

                            self.squares[self.get_id_from_pos(self, 1, "h")][3] = True
                            self.squares[
                                self.get_id_from_pos(self, 1, self.files[self.files.index(square_from[1]) + 1])][
                                3] = True
                        if square_to[1] in self.files[:4]:
                            self.squares[self.get_id_from_pos(self, 1, "a")][2], self.squares[
                                self.get_id_from_pos(self, 1, self.files[self.files.index(square_from[1]) - 1])][
                                2] = " ", self.squares[self.get_id_from_pos(self, 1, "a")][2]

                            self.squares[self.get_id_from_pos(self, 1, "a")][3] = True
                            self.squares[
                                self.get_id_from_pos(self, 1, self.files[self.files.index(square_from[1]) - 1])][
                                3] = True
                    if square_from[2].upper() == "k":
                        if square_to[1] in self.files[4:]:
                            self.squares[self.get_id_from_pos(self, 8, "h")][2], \
                            self.squares[
                                self.get_id_from_pos(self, 8, self.files[self.files.index(square_from[1]) + 1])][
                                2] = " ", self.squares[self.get_id_from_pos(self, 8, "h")][2]

                            self.squares[self.get_id_from_pos(self, 8, "h")][3] = True
                            self.squares[
                                self.get_id_from_pos(self, 8, self.files[self.files.index(square_from[1]) + 1])][
                                3] = True
                        if square_to[1] in self.files[:4]:
                            self.squares[self.get_id_from_pos(self, 8, "a")][2], \
                            self.squares[
                                self.get_id_from_pos(self, 8, self.files[self.files.index(square_from[1]) - 1])][
                                2] = " ", self.squares[self.get_id_from_pos(self, 8, "a")][2]

                            self.squares[self.get_id_from_pos(self, 8, "a")][3] = True
                            self.squares[
                                self.get_id_from_pos(self, 8, self.files[self.files.index(square_from[1]) - 1])][
                                3] = True


                find_legal_move = True
                print(square_from, "from")
                print(square_to, "to")
                square_from[2], square_to[2] = " ", square_from[2]

                square_from[3] = True
                square_to[3] = True

                print("after move:\n", square_from, "from")
                print(square_to, "to")

                if self.color_tm == "K":
                    self.moves += 1
                break
        # print("Time to go for all legal moves", time.time() - start)
        if find_legal_move == False:
            print("Move is illegal")
            return

        if self.is_king_in_check(self, self.color_tm) == True:
            self.squares = copy.deepcopy(backup_squares)
            print("This move is illegal, your king will be in check")
            return


        if self.color_tm.isupper() == True:
            self.color_tm = "k"
        else:
            self.color_tm = "K"
        return





if __name__ == "__main__":
    chessboard = ChessBoard
    chessboard.fill_board(chessboard)
    chessboard.import_game(chessboard, "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
    chessboard.show_chessboard(chessboard)

    while True:
        mv = input(f"Debugging\nMake your move \n")

        start = time.time()

        chessboard.make_move(chessboard, str(mv))
        print("Time to find legal moves:", time.time() - start)

        print(chessboard.evaluate(chessboard))

        chessboard.show_chessboard(chessboard)



