import numpy as np


class Piece:

    # name = "" #Pawn/Bishop/Knight/Rook/Quine/King
    _char = "P" # white --> P/B/K/R/Q/K black --> p/b/k/r/q/k
    price = 100

    rank = "1" #12345678
    file = "a" #abcdefgh


class ChessBoard:
    files= " abcdefgh "
    squares = [] # inside [ [rank, file, "name", False], [rank, file, "name"], [rank, file, "name"],
                 #         [rank, file, "name"],
    def fill_board(self):
        for rank in range(8,0,-1):

            for file in "hgfedcba":
               self.squares.append([rank, file, ""])
            # self.squares.append(_file)
    def import_game(self, fen_game):
        ranks = fen_game.split("/")
        print(np.array(ranks))

        id = 0

        letters = 'abcdefgh'

        for rank, rank_n in zip(ranks, range(8, 0, -1)):
            letters_id = 0
            for piece in rank:
                try:
                    empty_squares = int(piece)
                    for emp in range(empty_squares):
                        self.squares[id] = [rank_n, letters[letters_id], " ", False]
                        # print(self.squares[id])
                        letters_id += 1
                        id += 1
                except:

                    self.squares[id] = [rank_n, letters[letters_id], piece, False]
                    # print(self.squares[id])
                    id += 1
                    letters_id += 1

            rank_n += 1

    def show_chessboard(self):
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


    def find_legal_moves(self, _rank, _file):
        piece_id = 0


        for square in self.squares:
            if square[0] == _rank and square[1] == _file:
                 break
            piece_id += 1

        print(self.squares[piece_id])

        legal_moves = []
        if self.squares[piece_id][2] == "P":
            next_square = self.is_square_empty(self, self.squares[piece_id][0] + 1, self.squares[piece_id][1])

            if self.squares[piece_id][3] == False:
                if next_square == True:
                    legal_moves.append([[self.squares[piece_id][0], self.squares[piece_id][1]],
                                        [self.squares[piece_id][0]+1, self.squares[piece_id][1]]])
                    if self.is_square_empty(self, self.squares[piece_id][0] + 2, self.squares[piece_id][1]) == True:
                        legal_moves.append([[self.squares[piece_id][0], self.squares[piece_id][1]],
                                            [self.squares[piece_id][0] + 2, self.squares[piece_id][1]]])

            if self.squares[piece_id][3] == True:
                if next_square == True:
                    legal_moves.append([[self.squares[piece_id][0], self.squares[piece_id][1]],
                                        [self.squares[piece_id][0] + 1, self.squares[piece_id][1]]])


            if self.is_enemy_in_square(self, self.squares[piece_id][0]+1,
                                       self.files[self.files.index(self.squares[piece_id][1])+1], self.squares[piece_id][2]) == True:
                legal_moves.append([[self.squares[piece_id][0], self.squares[piece_id][1]],
                                    [self.squares[piece_id][0] + 1, self.files[self.files.index(self.squares[piece_id][1])+1]]])

            if self.is_enemy_in_square(self, self.squares[piece_id][0] + 1,
                                       self.files[self.files.index(self.squares[piece_id][1]) - 1], self.squares[piece_id][2]) == True:
                legal_moves.append([[self.squares[piece_id][0], self.squares[piece_id][1]],
                                    [self.squares[piece_id][0] + 1,
                                     self.files[self.files.index(self.squares[piece_id][1]) - 1]]])
        if self.squares[piece_id][2] == "p":
            next_square = self.is_square_empty(self, self.squares[piece_id][0] - 1, self.squares[piece_id][1])

            if self.squares[piece_id][3] == False:
                if next_square == True:
                    legal_moves.append([[self.squares[piece_id][0], self.squares[piece_id][1]],
                                        [self.squares[piece_id][0]-1, self.squares[piece_id][1]]])
                    if self.is_square_empty(self, self.squares[piece_id][0] - 2, self.squares[piece_id][1]) == True:
                        legal_moves.append([[self.squares[piece_id][0], self.squares[piece_id][1]],
                                            [self.squares[piece_id][0] - 2, self.squares[piece_id][1]]])

            if self.squares[piece_id][3] == True:
                if next_square == True:
                    legal_moves.append([[self.squares[piece_id][0], self.squares[piece_id][1]],
                                        [self.squares[piece_id][0] - 1, self.squares[piece_id][1]]])


            if self.is_enemy_in_square(self, self.squares[piece_id][0]-1,
                                       self.files[self.files.index(self.squares[piece_id][1])+1], self.squares[piece_id][2]) == True:
                legal_moves.append([[self.squares[piece_id][0], self.squares[piece_id][1]],
                                    [self.squares[piece_id][0] - 1, self.files[self.files.index(self.squares[piece_id][1])+1]]])

            if self.is_enemy_in_square(self, self.squares[piece_id][0] - 1,
                                       self.files[self.files.index(self.squares[piece_id][1]) - 1], self.squares[piece_id][2]) == True:
                legal_moves.append([[self.squares[piece_id][0], self.squares[piece_id][1]],
                                    [self.squares[piece_id][0] - 1,
                                     self.files[self.files.index(self.squares[piece_id][1]) - 1]]])
        if self.squares[piece_id][2] == "R":
            for file_up in range(self.squares[piece_id][0] + 1, 9):
                if self.is_square_empty(self, file_up, self.squares[piece_id][1]) == True:
                    legal_moves.append([[self.squares[piece_id][0], self.squares[piece_id][1]],
                                        [file_up, self.squares[piece_id][1]]])
                else:
                    if self.is_enemy_in_square(self, file_up, self.squares[piece_id][1],
                                               self.squares[piece_id][2]) == True:
                        legal_moves.append([[self.squares[piece_id][0], self.squares[piece_id][1]],
                                            [file_up, self.squares[piece_id][1]]])
                    break
            print("hiii")
            for file_down in range(self.squares[piece_id][0] - 1, 0, -1):
                if self.is_square_empty(self, file_down, self.squares[piece_id][1]) == True:
                    legal_moves.append([[self.squares[piece_id][0], self.squares[piece_id][1]],
                                        [file_down, self.squares[piece_id][1]]])
                else:
                    if self.is_enemy_in_square(self, file_down, self.squares[piece_id][1],
                                               self.squares[piece_id][2]) == True:
                        legal_moves.append([[self.squares[piece_id][0], self.squares[piece_id][1]],
                                            [file_down, self.squares[piece_id][1]]])
                    break

            for rank_right in self.files[self.files.index(self.squares[piece_id][1].lower()) + 1:]:

                if self.is_square_empty(self, self.squares[piece_id][0], rank_right) == True:
                    legal_moves.append([[self.squares[piece_id][0], self.squares[piece_id][1]],
                                        [self.squares[piece_id][0], rank_right]])
                else:
                    if self.is_enemy_in_square(self, self.squares[piece_id][0], rank_right,
                                               self.squares[piece_id][2]) == True:
                        legal_moves.append([[self.squares[piece_id][0], self.squares[piece_id][1]],
                                            [self.squares[piece_id][0], rank_right]])
                    break

            print(list(reversed(self.files[:self.files.index(self.squares[piece_id][1]) + 1])))

            for rank_left in list(reversed(self.files[:self.files.index(self.squares[piece_id][1]) - 1])):

                if self.is_square_empty(self, self.squares[piece_id][0], rank_left) == True:

                    legal_moves.append([[self.squares[piece_id][0], self.squares[piece_id][1]],
                                        [self.squares[piece_id][0], rank_left]])
                else:
                    if self.is_enemy_in_square(self, self.squares[piece_id][0], rank_left,
                                               self.squares[piece_id][2]) == True:
                        legal_moves.append([[self.squares[piece_id][0], self.squares[piece_id][1]],
                                            [self.squares[piece_id][0], rank_left]])
                    break
        if self.squares[piece_id][2] == "r":
            for file_up in range(self.squares[piece_id][0] + 1, 9):
                if self.is_square_empty(self, file_up, self.squares[piece_id][1]) == True:
                    legal_moves.append([[self.squares[piece_id][0], self.squares[piece_id][1]],
                                        [file_up, self.squares[piece_id][1]]])
                else:
                    if self.is_enemy_in_square(self, file_up, self.squares[piece_id][1],
                                               self.squares[piece_id][2]) == True:
                        legal_moves.append([[self.squares[piece_id][0], self.squares[piece_id][1]],
                                            [file_up, self.squares[piece_id][1]]])
                    break

            for file_down in range(self.squares[piece_id][0] - 1, 0, -1):
                if self.is_square_empty(self, file_down, self.squares[piece_id][1]) == True:
                    legal_moves.append([[self.squares[piece_id][0], self.squares[piece_id][1]],
                                        [file_down, self.squares[piece_id][1]]])
                else:
                    if self.is_enemy_in_square(self, file_down, self.squares[piece_id][1],
                                               self.squares[piece_id][2]) == True:
                        legal_moves.append([[self.squares[piece_id][0], self.squares[piece_id][1]],
                                            [file_down, self.squares[piece_id][1]]])
                    break

            for rank_right in self.files[self.files.index(self.squares[piece_id][1].lower()) + 1:]:

                if self.is_square_empty(self, self.squares[piece_id][0], rank_right) == True:
                    legal_moves.append([[self.squares[piece_id][0], self.squares[piece_id][1]],
                                        [self.squares[piece_id][0], rank_right]])
                else:
                    if self.is_enemy_in_square(self, self.squares[piece_id][0], rank_right,
                                               self.squares[piece_id][2]) == True:
                        legal_moves.append([[self.squares[piece_id][0], self.squares[piece_id][1]],
                                            [self.squares[piece_id][0], rank_right]])
                    break

            for rank_left in list(reversed(self.files[:self.files.index(self.squares[piece_id][1]) - 1])):

                if self.is_square_empty(self, self.squares[piece_id][0], rank_left) == True:

                    legal_moves.append([[self.squares[piece_id][0], self.squares[piece_id][1]],
                                        [self.squares[piece_id][0], rank_left]])
                else:
                    if self.is_enemy_in_square(self, self.squares[piece_id][0], rank_left,
                                               self.squares[piece_id][2]) == True:
                        legal_moves.append([[self.squares[piece_id][0], self.squares[piece_id][1]],
                                            [self.squares[piece_id][0], rank_left]])
                    break
        if self.squares[piece_id][2] == "B":
            for rank in range(self.squares[piece_id][0]):
                return




        print(np.array(legal_moves))





if __name__ == "__main__":
    chessboard = ChessBoard
    chessboard.fill_board(chessboard)
    chessboard.import_game(chessboard, "rnbqkbnr/pppppppp/8/8/4r3/8/PPPPPPPP/RNBQKBNR")
    chessboard.show_chessboard(chessboard)

    chessboard.find_legal_moves(chessboard, 2, "h")
