import pygame


game_so_far = []
reversed_dict = {
    'a': 1,
    'b': 2,
    'c': 3,
    'd': 4,
    'e': 5,
    'f': 6,
    'g': 7,
    'h': 8
}


def find_king(board, colour):
    for i in range(8):
        for j in range(8):
            if board[i][j].occupied:
                if board[i][j].occupied.name == colour + "Kk":
                    return j+1, i+1


def check(board, colour, from_move, to_move, move_nothing=False):
    answer = True
    anti_colour = 'w' if colour == 'b' else 'b'

    temp_piece = board[to_move[1] - 1][to_move[0] - 1].occupied
    if not move_nothing:
        board[to_move[1]-1][to_move[0]-1].occupy(board[from_move[1]-1][from_move[0]-1].occupied)
        board[from_move[1]-1][from_move[0]-1].unoccupy()

    king_file, king_rank = find_king(board, colour)

    knight_check = [
        (king_file + 2, king_rank + 1),
        (king_file + 2, king_rank - 1),
        (king_file - 2, king_rank + 1),
        (king_file - 2, king_rank - 1),
        (king_file + 1, king_rank + 2),
        (king_file + 1, king_rank - 2),
        (king_file - 1, king_rank + 2),
        (king_file - 1, king_rank - 2)
    ]

    for pos in knight_check:
        if min(pos) > 0 and max(pos) < 9:
            if board[pos[1]-1][pos[0]-1].occupied:
                if board[pos[1] - 1][pos[0] - 1].occupied.name[:2] == (anti_colour + "N"):
                    answer = False

    k = 1
    while king_rank + k < 9 and king_file + k < 9:
        if board[king_rank + k - 1][king_file + k - 1].occupied:
            if board[king_rank + k - 1][king_file + k - 1].occupied.name[0] == anti_colour and \
                    board[king_rank + k - 1][king_file + k - 1].occupied.name[1] in "QB":
                answer = False
            break
        k = k + 1

    k = 1
    while king_rank - k > 0 and king_file + k < 9:
        if board[king_rank - k - 1][king_file + k - 1].occupied:
            if board[king_rank - k - 1][king_file + k - 1].occupied.name[0] == anti_colour and \
                    board[king_rank - k - 1][king_file + k - 1].occupied.name[1] in "QB":
                answer = False
            break
        k = k + 1

    k = 1
    while king_rank + k < 9 and king_file - k > 0:
        if board[king_rank + k - 1][king_file - k - 1].occupied:
            if board[king_rank + k - 1][king_file - k - 1].occupied.name[0] == anti_colour and \
                    board[king_rank + k - 1][king_file - k - 1].occupied.name[1] in "QB":
                answer = False
            break
        k = k + 1

    k = 1
    while king_rank - k > 0 and king_file - k > 0:
        if board[king_rank - k - 1][king_file - k - 1].occupied:
            if board[king_rank - k - 1][king_file - k - 1].occupied.name[0] == anti_colour and \
                    board[king_rank - k - 1][king_file - k - 1].occupied.name[1] in "QB":
                answer = False
            break
        k = k + 1

    k = 1
    while king_rank + k < 9:
        if board[king_rank + k - 1][king_file - 1].occupied:
            if board[king_rank + k - 1][king_file - 1].occupied.name[0] == anti_colour and \
                    board[king_rank + k - 1][king_file - 1].occupied.name[1] in "QR":
                answer = False
            break
        k = k + 1

    k = 1
    while king_rank - k > 0:
        if board[king_rank - k - 1][king_file - 1].occupied:
            if board[king_rank - k - 1][king_file - 1].occupied.name[0] == anti_colour and \
                    board[king_rank - k - 1][king_file - 1].occupied.name[1] in "QR":
                answer = False
            break
        k = k + 1

    k = 1
    while king_file + k < 9:
        if board[king_rank - 1][king_file + k - 1].occupied:
            if board[king_rank - 1][king_file + k - 1].occupied.name[0] == anti_colour and \
                    board[king_rank - 1][king_file + k - 1].occupied.name[1] in "QR":
                answer = False
            break
        k = k + 1

    k = 1
    while king_file - k > 0:
        if board[king_rank - 1][king_file - k - 1].occupied:
            if board[king_rank - 1][king_file - k - 1].occupied.name[0] == anti_colour and \
                    board[king_rank - 1][king_file - k - 1].occupied.name[1] in "QR":
                answer = False
            break
        k = k + 1

    if colour == 'w':
        if king_rank < 8:
            if king_file > 1 and board[king_rank][king_file-2].occupied:
                if board[king_rank][king_file - 2].occupied.name[:2] == 'bP':
                    answer = False
            if king_file < 8 and board[king_rank][king_file].occupied:
                if board[king_rank][king_file].occupied.name[:2] == 'bP':
                    answer = False

    if colour == 'b':
        if king_rank > 1:
            if king_file > 1 and board[king_rank-2][king_file-2].occupied:
                if board[king_rank-2][king_file - 2].occupied.name[:2] == 'wP':
                    answer = False
            if king_file < 8 and board[king_rank-2][king_file].occupied:
                if board[king_rank-2][king_file].occupied.name[:2] == 'wP':
                    answer = False

    if not move_nothing:
        board[from_move[1] - 1][from_move[0] - 1].occupy(board[to_move[1] - 1][to_move[0] - 1].occupied)
        board[to_move[1] - 1][to_move[0] - 1].occupy(temp_piece)

    return answer


class Pawn:
    def __init__(self, name, file_num, rank_num):
        self.colour = name[0]
        self.name = name
        self.file_num = file_num
        self.rank_num = rank_num
        self.image = pygame.image.load('piece_images/' + self.colour + 'P.png')

    def moves(self, board):
        final = []

        if self.colour == 'w':
            if self.rank_num < 8 and board[self.rank_num][self.file_num-1].occupied is None:
                final.append((self.file_num, self.rank_num + 1))
            if self.rank_num == 2 and board[2][self.file_num-1].occupied is None and \
                    board[3][self.file_num-1].occupied is None:
                final.append((self.file_num, 4))
            if self.rank_num < 8 and self.file_num < 8 and board[self.rank_num][self.file_num].occupied:
                if board[self.rank_num][self.file_num].occupied.colour != self.colour:
                    final.append((self.file_num + 1, self.rank_num + 1))
            if self.rank_num < 8 and self.file_num > 1 and board[self.rank_num][self.file_num-2].occupied:
                if board[self.rank_num][self.file_num-2].occupied.colour != self.colour:
                    final.append((self.file_num - 1, self.rank_num + 1))
            if self.rank_num == 5:
                prev_move = game_so_far[-1].split(" ")
                if prev_move[1][1] == 'P' and prev_move[2][1] == '7' and prev_move[3][1] == '5':
                    prev_pawn_file = reversed_dict[prev_move[1][2]]
                    if abs(prev_pawn_file - self.file_num) == 1:
                        final.append((prev_pawn_file, self.rank_num + 1))

        else:
            if self.rank_num > 1 and board[self.rank_num-2][self.file_num-1].occupied is None:
                final.append((self.file_num, self.rank_num - 1))
            if self.rank_num == 7 and board[5][self.file_num-1].occupied is None and \
                    board[4][self.file_num-1].occupied is None:
                final.append((self.file_num, 5))
            if self.rank_num > 1 and self.file_num < 8 and board[self.rank_num-2][self.file_num].occupied:
                if board[self.rank_num-2][self.file_num].occupied.colour != self.colour:
                    final.append((self.file_num + 1, self.rank_num - 1))
            if self.rank_num > 1 and self.file_num > 1 and board[self.rank_num-2][self.file_num-2].occupied:
                if board[self.rank_num-2][self.file_num-2].occupied.colour != self.colour:
                    final.append((self.file_num - 1, self.rank_num - 1))
            if self.rank_num == 4:
                prev_move = game_so_far[-1].split(" ")
                if prev_move[1][1] == 'P' and prev_move[2][1] == '2' and prev_move[3][1] == '4':
                    prev_pawn_file = reversed_dict[prev_move[1][2]]
                    if abs(prev_pawn_file - self.file_num) == 1:
                        final.append((prev_pawn_file, self.rank_num - 1))

        check_filtered = []

        for move in final:
            if check(board, self.colour, (self.file_num, self.rank_num), move):
                check_filtered.append(move)

        return check_filtered

    def change_pos(self, new_file_num, new_rank_num):
        self.file_num = new_file_num
        self.rank_num = new_rank_num


class Bishop:
    def __init__(self, name, file_num, rank_num):
        self.colour = name[0]
        self.name = name
        self.file_num = file_num
        self.rank_num = rank_num
        self.image = pygame.image.load('piece_images/' + self.colour + 'B.png')

    def moves(self, board):
        final = []

        k = 1
        while self.rank_num + k < 9 and self.file_num + k < 9:
            if board[self.rank_num+k-1][self.file_num+k-1].occupied is None:
                final.append((self.file_num + k, self.rank_num + k))
            elif board[self.rank_num+k-1][self.file_num+k-1].occupied.colour != self.colour:
                final.append((self.file_num + k, self.rank_num + k))
                break
            else:
                break
            k = k + 1

        k = 1
        while self.rank_num + k < 9 and self.file_num - k > 0:
            if board[self.rank_num+k-1][self.file_num-k-1].occupied is None:
                final.append((self.file_num - k, self.rank_num + k))
            elif board[self.rank_num+k-1][self.file_num-k-1].occupied.colour != self.colour:
                final.append((self.file_num - k, self.rank_num + k))
                break
            else:
                break
            k = k + 1

        k = 1
        while self.rank_num - k > 0 and self.file_num + k < 9:
            if board[self.rank_num-k-1][self.file_num+k-1].occupied is None:
                final.append((self.file_num + k, self.rank_num - k))
            elif board[self.rank_num-k-1][self.file_num+k-1].occupied.colour != self.colour:
                final.append((self.file_num + k, self.rank_num - k))
                break
            else:
                break
            k = k + 1

        k = 1
        while self.rank_num - k > 0 and self.file_num - k > 0:
            if board[self.rank_num-k-1][self.file_num-k-1].occupied is None:
                final.append((self.file_num - k, self.rank_num - k))
            elif board[self.rank_num-k-1][self.file_num-k-1].occupied.colour != self.colour:
                final.append((self.file_num - k, self.rank_num - k))
                break
            else:
                break
            k = k + 1

        check_filtered = []

        for move in final:
            if check(board, self.colour, (self.file_num, self.rank_num), move):
                check_filtered.append(move)

        return check_filtered

    def change_pos(self, new_file_num, new_rank_num):
        self.file_num = new_file_num
        self.rank_num = new_rank_num


class Knight:
    def __init__(self, name, file_num, rank_num):
        self.colour = name[0]
        self.name = name
        self.file_num = file_num
        self.rank_num = rank_num
        self.image = pygame.image.load('piece_images/' + self.colour + 'N.png')

    def moves(self, board):
        possible_moves = [
            (self.file_num + 2, self.rank_num + 1),
            (self.file_num + 2, self.rank_num - 1),
            (self.file_num - 2, self.rank_num + 1),
            (self.file_num - 2, self.rank_num - 1),
            (self.file_num + 1, self.rank_num + 2),
            (self.file_num + 1, self.rank_num - 2),
            (self.file_num - 1, self.rank_num + 2),
            (self.file_num - 1, self.rank_num - 2)
        ]

        final = []

        for move in possible_moves:
            if min(move) > 0 and max(move) < 9:
                if board[move[1]-1][move[0]-1].occupied is None or \
                        board[move[1]-1][move[0]-1].occupied.colour != self.colour:
                    final.append(move)

        check_filtered = []

        for move in final:
            if check(board, self.colour, (self.file_num, self.rank_num), move):
                check_filtered.append(move)

        return check_filtered

    def change_pos(self, new_file_num, new_rank_num):
        self.file_num = new_file_num
        self.rank_num = new_rank_num


class Rook:
    def __init__(self, name, file_num, rank_num):
        self.colour = name[0]
        self.name = name
        self.file_num = file_num
        self.rank_num = rank_num
        self.moved = False
        self.image = pygame.image.load('piece_images/' + self.colour + 'R.png')

    def moves(self, board):
        final = []

        k = 1
        while self.rank_num + k < 9:
            if board[self.rank_num+k-1][self.file_num-1].occupied is None:
                final.append((self.file_num, self.rank_num + k))
            elif board[self.rank_num+k-1][self.file_num-1].occupied.colour != self.colour:
                final.append((self.file_num, self.rank_num + k))
                break
            else:
                break
            k = k + 1

        k = 1
        while self.rank_num - k > 0:
            if board[self.rank_num - k - 1][self.file_num - 1].occupied is None:
                final.append((self.file_num, self.rank_num - k))
            elif board[self.rank_num - k - 1][self.file_num - 1].occupied.colour != self.colour:
                final.append((self.file_num, self.rank_num - k))
                break
            else:
                break
            k = k + 1

        k = 1
        while self.file_num + k < 9:
            if board[self.rank_num - 1][self.file_num + k - 1].occupied is None:
                final.append((self.file_num + k, self.rank_num))
            elif board[self.rank_num - 1][self.file_num + k - 1].occupied.colour != self.colour:
                final.append((self.file_num + k, self.rank_num))
                break
            else:
                break
            k = k + 1

        k = 1
        while self.file_num + k > 0:
            if board[self.rank_num - 1][self.file_num - k - 1].occupied is None:
                final.append((self.file_num - k, self.rank_num))
            elif board[self.rank_num - 1][self.file_num - k - 1].occupied.colour != self.colour:
                final.append((self.file_num - k, self.rank_num))
                break
            else:
                break
            k = k + 1

        check_filtered = []

        for move in final:
            if check(board, self.colour, (self.file_num, self.rank_num), move):
                check_filtered.append(move)

        return check_filtered

    def change_pos(self, new_file_num, new_rank_num):
        self.file_num = new_file_num
        self.rank_num = new_rank_num
        self.moved = True


class Queen:
    def __init__(self, name, file_num, rank_num):
        self.colour = name[0]
        self.name = name
        self.file_num = file_num
        self.rank_num = rank_num
        self.image = pygame.image.load('piece_images/' + self.colour + 'Q.png')

    def moves(self, board):
        final = []

        k = 1
        while self.rank_num + k < 9 and self.file_num + k < 9:
            if board[self.rank_num+k-1][self.file_num+k-1].occupied is None:
                final.append((self.file_num + k, self.rank_num + k))
            elif board[self.rank_num+k-1][self.file_num+k-1].occupied.colour != self.colour:
                final.append((self.file_num + k, self.rank_num + k))
                break
            else:
                break
            k = k + 1

        k = 1
        while self.rank_num + k < 9 and self.file_num - k > 0:
            if board[self.rank_num+k-1][self.file_num-k-1].occupied is None:
                final.append((self.file_num - k, self.rank_num + k))
            elif board[self.rank_num+k-1][self.file_num-k-1].occupied.colour != self.colour:
                final.append((self.file_num - k, self.rank_num + k))
                break
            else:
                break
            k = k + 1

        k = 1
        while self.rank_num - k > 0 and self.file_num + k < 9:
            if board[self.rank_num-k-1][self.file_num+k-1].occupied is None:
                final.append((self.file_num + k, self.rank_num - k))
            elif board[self.rank_num-k-1][self.file_num+k-1].occupied.colour != self.colour:
                final.append((self.file_num + k, self.rank_num - k))
                break
            else:
                break
            k = k + 1

        k = 1
        while self.rank_num - k > 0 and self.file_num - k > 0:
            if board[self.rank_num-k-1][self.file_num-k-1].occupied is None:
                final.append((self.file_num - k, self.rank_num - k))
            elif board[self.rank_num-k-1][self.file_num-k-1].occupied.colour != self.colour:
                final.append((self.file_num - k, self.rank_num - k))
                break
            else:
                break
            k = k + 1

        k = 1
        while self.rank_num + k < 9:
            if board[self.rank_num + k - 1][self.file_num - 1].occupied is None:
                final.append((self.file_num, self.rank_num + k))
            elif board[self.rank_num + k - 1][self.file_num - 1].occupied.colour != self.colour:
                final.append((self.file_num, self.rank_num + k))
                break
            else:
                break
            k = k + 1

        k = 1
        while self.rank_num - k > 0:
            if board[self.rank_num - k - 1][self.file_num - 1].occupied is None:
                final.append((self.file_num, self.rank_num - k))
            elif board[self.rank_num - k - 1][self.file_num - 1].occupied.colour != self.colour:
                final.append((self.file_num, self.rank_num - k))
                break
            else:
                break
            k = k + 1

        k = 1
        while self.file_num + k < 9:
            if board[self.rank_num - 1][self.file_num + k - 1].occupied is None:
                final.append((self.file_num + k, self.rank_num))
            elif board[self.rank_num - 1][self.file_num + k - 1].occupied.colour != self.colour:
                final.append((self.file_num + k, self.rank_num))
                break
            else:
                break
            k = k + 1

        k = 1
        while self.file_num + k > 0:
            if board[self.rank_num - 1][self.file_num - k - 1].occupied is None:
                final.append((self.file_num - k, self.rank_num))
            elif board[self.rank_num - 1][self.file_num - k - 1].occupied.colour != self.colour:
                final.append((self.file_num - k, self.rank_num))
                break
            else:
                break
            k = k + 1

        check_filtered = []

        for move in final:
            if check(board, self.colour, (self.file_num, self.rank_num), move):
                check_filtered.append(move)

        return check_filtered

    def change_pos(self, new_file_num, new_rank_num):
        self.file_num = new_file_num
        self.rank_num = new_rank_num


class King:
    def __init__(self, name, file_num, rank_num):
        self.colour = name[0]
        self.name = name
        self.file_num = file_num
        self.rank_num = rank_num
        self.moved = False
        self.image = pygame.image.load('piece_images/' + self.colour + 'K.png')

    def moves(self, board):
        possible_moves = [
            (self.file_num + 1, self.rank_num),
            (self.file_num + 1, self.rank_num - 1),
            (self.file_num + 1, self.rank_num + 1),
            (self.file_num, self.rank_num - 1),
            (self.file_num, self.rank_num + 1),
            (self.file_num - 1, self.rank_num - 1),
            (self.file_num - 1, self.rank_num + 1),
            (self.file_num - 1, self.rank_num)
        ]

        final = []

        for move in possible_moves:
            if min(move) > 0 and max(move) < 9:
                if board[move[1]-1][move[0]-1].occupied is None or \
                        board[move[1]-1][move[0]-1].occupied.colour != self.colour:
                    final.append(move)

        if not self.moved:
            if board[self.rank_num-1][self.file_num].occupied is None and \
                    board[self.rank_num-1][self.file_num+1].occupied is None and \
                    board[self.rank_num-1][self.file_num+2].occupied and \
                    board[self.rank_num-1][self.file_num+2].occupied.name[1] == 'R' and \
                    not board[self.rank_num-1][self.file_num+2].occupied.moved:

                    if check(board, self.colour, (5, 5), (5, 5), True):
                        board[self.rank_num-1][self.file_num].occupy(board[self.rank_num-1][self.file_num-1].occupied)
                        board[self.rank_num - 1][self.file_num - 1].unoccupy()
                        if check(board, self.colour, (5, 5), (5, 5), True):
                            final.append((self.file_num + 2, self.rank_num))
                        board[self.rank_num-1][self.file_num-1].occupy(board[self.rank_num-1][self.file_num].occupied)
                        board[self.rank_num-1][self.file_num].unoccupy()

            if board[self.rank_num-1][self.file_num-2].occupied is None and \
                    board[self.rank_num-1][self.file_num-3].occupied is None and \
                    board[self.rank_num-1][self.file_num-4].occupied is None and \
                    board[self.rank_num-1][self.file_num-5].occupied and \
                    board[self.rank_num-1][self.file_num-5].occupied.name[1] == 'R' and \
                    not board[self.rank_num-1][self.file_num-5].occupied.moved:

                    if check(board, self.colour, (5, 5), (5, 5), True):
                        board[self.rank_num-1][self.file_num-2].occupy(board[self.rank_num-1][self.file_num-1].occupied)
                        board[self.rank_num-1][self.file_num-1].unoccupy()
                        if check(board, self.colour, (5, 5), (5, 5), True):
                            final.append((self.file_num-2, self.rank_num))
                        board[self.rank_num-1][self.file_num-1].occupy(board[self.rank_num-1][self.file_num-2].occupied)
                        board[self.rank_num-1][self.file_num-2].unoccupy()

        check_filtered = []

        for move in final:
            if check(board, self.colour, (self.file_num, self.rank_num), move):
                anti_colour = 'w' if self.colour == 'b' else 'b'
                file_opp, rank_opp = find_king(board, anti_colour)
                if abs(file_opp - move[0]) > 1 or abs(rank_opp - move[1]) > 1:
                    check_filtered.append(move)

        return check_filtered

    def change_pos(self, new_file_num, new_rank_num):
        self.file_num = new_file_num
        self.rank_num = new_rank_num
        self.moved = True
