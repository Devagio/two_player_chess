import pygame
import pieces


IMAGE_SIZE = 60
PADDING = 10
SQUARE_SIZE = IMAGE_SIZE + 2 * PADDING

WHITE = (225, 225, 225)
REDDER_WHITE = (255, 200, 200)
GREENER_WHITE = (200, 255, 200)
DARK_WHITE = (255, 255, 255)
BLACK = (100, 100, 100)
REDDER_BLACK = (150, 100, 100)
GREENER_BLACK = (100, 150, 100)
DARK_BLACK = (0, 0, 0)

rank_dict = {
    1: 'a',
    2: 'b',
    3: 'c',
    4: 'd',
    5: 'e',
    6: 'f',
    7: 'g',
    8: 'h'
}


class Square:
    def __init__(self, file_num, rank_num):
        self.rank_num = rank_num
        self.file_num = file_num
        self.rank = str(rank_num)
        self.file = rank_dict[file_num]
        self.name = self.file + self.rank

        self.x = (file_num - 1) * SQUARE_SIZE
        self.y = (8 - rank_num) * SQUARE_SIZE

        self.colour = WHITE if (rank_num + file_num) % 2 else BLACK
        self.occupied = None

        self.current = False
        self.possible = False

    def occupy(self, piece):
        self.occupied = piece

    def unoccupy(self):
        self.occupied = None

    def make_current(self):
        self.current = True

    def remove_current(self):
        self.current = False

    def make_possible(self):
        self.possible = True

    def remove_possible(self):
        self.possible = False

    def draw(self, screen):
        if self.current:
            self.colour = REDDER_BLACK if self.colour == BLACK else REDDER_WHITE
        elif self.possible:
            self.colour = GREENER_BLACK if self.colour == BLACK else GREENER_WHITE

        pygame.draw.rect(screen, self.colour, (self.x, self.y, SQUARE_SIZE, SQUARE_SIZE))

        if self.colour == REDDER_BLACK or self.colour == GREENER_BLACK:
            self.colour = BLACK
        elif self.colour == REDDER_WHITE or self.colour == GREENER_WHITE:
            self.colour = WHITE

        if self.occupied:
            screen.blit(self.occupied.image, (self.x + PADDING, self.y+PADDING))


def make_board():
    board_array = [[] for _ in range(8)]
    for i in range(1, 9):
        for j in range(1, 9):
            board_array[i-1].append(Square(j, 9 - i))
    return board_array[::-1]


def classic_layout():
    all_pieces = {
        'wPa': pieces.Pawn('wPa', 1, 2),
        'wPb': pieces.Pawn('wPb', 2, 2),
        'wPc': pieces.Pawn('wPc', 3, 2),
        'wPd': pieces.Pawn('wPd', 4, 2),
        'wPe': pieces.Pawn('wPe', 5, 2),
        'wPf': pieces.Pawn('wPf', 6, 2),
        'wPg': pieces.Pawn('wPg', 7, 2),
        'wPh': pieces.Pawn('wPh', 8, 2),
        'bPa': pieces.Pawn('bPa', 1, 7),
        'bPb': pieces.Pawn('bPb', 2, 7),
        'bPc': pieces.Pawn('bPc', 3, 7),
        'bPd': pieces.Pawn('bPd', 4, 7),
        'bPe': pieces.Pawn('bPe', 5, 7),
        'bPf': pieces.Pawn('bPf', 6, 7),
        'bPg': pieces.Pawn('bPg', 7, 7),
        'bPh': pieces.Pawn('bPh', 8, 7),
        'wBq': pieces.Bishop('wBq', 3, 1),
        'wBk': pieces.Bishop('wBk', 6, 1),
        'wNq': pieces.Knight('wNq', 2, 1),
        'wNk': pieces.Knight('wNk', 7, 1),
        'wRq': pieces.Rook('wRq', 1, 1),
        'wRk': pieces.Rook('wRk', 8, 1),
        'wQq': pieces.Queen('wQq', 4, 1),
        'wKk': pieces.King('wKk', 5, 1),
        'bBq': pieces.Bishop('bBq', 3, 8),
        'bBk': pieces.Bishop('bBk', 6, 8),
        'bNq': pieces.Knight('bNq', 2, 8),
        'bNk': pieces.Knight('bNk', 7, 8),
        'bRq': pieces.Rook('bRq', 1, 8),
        'bRk': pieces.Rook('bRk', 8, 8),
        'bQq': pieces.Queen('bQq', 4, 8),
        'bKk': pieces.King('bKk', 5, 8),
    }
    return all_pieces


def place_pieces(all_pieces, board_array):
    for i in range(8):
        for j in range(8):
            board_array[i][j].unoccupy()

    for name in all_pieces:
        piece = all_pieces[name]
        board_array[piece.rank_num-1][piece.file_num-1].occupy(piece)

    return None


def draw_board(board_array, screen):
    for i in range(8):
        for j in range(8):
            board_array[i][j].draw(screen)
    pygame.display.update()


def draw_promotion(screen, colour):
    if colour == 'w':
        pygame.draw.rect(screen, DARK_BLACK, (3 * SQUARE_SIZE, 3 * SQUARE_SIZE, 2 * SQUARE_SIZE, 2 * SQUARE_SIZE))
        screen.blit(pygame.image.load('piece_images/wQ.png'), (3 * SQUARE_SIZE + PADDING, 3 * SQUARE_SIZE + PADDING))
        screen.blit(pygame.image.load('piece_images/wN.png'), (3 * SQUARE_SIZE + PADDING, 4 * SQUARE_SIZE + PADDING))
        screen.blit(pygame.image.load('piece_images/wR.png'), (4 * SQUARE_SIZE + PADDING, 3 * SQUARE_SIZE + PADDING))
        screen.blit(pygame.image.load('piece_images/wB.png'), (4 * SQUARE_SIZE + PADDING, 4 * SQUARE_SIZE + PADDING))
    else:
        pygame.draw.rect(screen, DARK_WHITE, (3 * SQUARE_SIZE, 3 * SQUARE_SIZE, 2 * SQUARE_SIZE, 2 * SQUARE_SIZE))
        screen.blit(pygame.image.load('piece_images/bQ.png'), (3 * SQUARE_SIZE + PADDING, 3 * SQUARE_SIZE + PADDING))
        screen.blit(pygame.image.load('piece_images/bN.png'), (3 * SQUARE_SIZE + PADDING, 4 * SQUARE_SIZE + PADDING))
        screen.blit(pygame.image.load('piece_images/bR.png'), (4 * SQUARE_SIZE + PADDING, 3 * SQUARE_SIZE + PADDING))
        screen.blit(pygame.image.load('piece_images/bB.png'), (4 * SQUARE_SIZE + PADDING, 4 * SQUARE_SIZE + PADDING))
    pygame.display.update()
