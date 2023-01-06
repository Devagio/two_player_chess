import pygame
import board
import asyncio

async def main():
    WIDTH = 8 * board.SQUARE_SIZE
    HEIGHT = 9 * board.SQUARE_SIZE
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess")
    pygame.font.init()


    board_array = board.make_board()
    all_pieces = board.classic_layout()
    board.place_pieces(all_pieces, board_array)


    font = pygame.font.Font("freesansbold.ttf", int(board.SQUARE_SIZE / 3))
    current_file_num, current_rank_num = 0, 0
    moves = []
    current_move = ""
    move_num = 1
    turn = 'w'
    promotion = False
    prom_rank = 0
    prom_file = 0
    fifty_counter = 0

    run = True
    mate = False
    check = False
    draw_game = False       # 3 fold repetition not implemented since players can mutually agree to continue
    while run:
        if not promotion:
            board.draw_board(board_array, SCREEN)

            message_text = ""
            if not mate and not check:
                if turn == 'w':
                    message_text = "White to move"
                else:
                    message_text = "Black to move"
            elif not mate:
                if turn == 'w':
                    message_text = "CHECK! White to move"
                else:
                    message_text = "CHECK! Black to move"
            elif not check:
                message_text = "STALEMATE! It is a draw"
            else:
                if turn == 'w':
                    message_text = "CHECKMATE! Black is the Winner!"
                else:
                    message_text = "CHECKMATE! White is the Winner!"

            if len(all_pieces) == 2:
                draw_game = True
                message_text = "Draw by insufficient material"

            if fifty_counter == 50:
                draw_game = True
                message_text = "Draw by 50-move rule"

            pygame.draw.rect(SCREEN, board.DARK_BLACK, (0, 8 * board.SQUARE_SIZE, 8 * board.SQUARE_SIZE, board.SQUARE_SIZE))
            message_render = font.render(message_text, True, (255, 255, 255))
            SCREEN.blit(message_render, (board.SQUARE_SIZE, 8.4 * board.SQUARE_SIZE))
            pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if promotion:
            pawn_name = board_array[prom_rank - 1][prom_file - 1].occupied.name

            board.draw_promotion(SCREEN, turn)
            if pygame.mouse.get_pressed()[0]:
                another_pos = pygame.mouse.get_pos()
                if 3 * board.SQUARE_SIZE < another_pos[0] < 4 * board.SQUARE_SIZE and \
                        3 * board.SQUARE_SIZE < another_pos[1] < 4 * board.SQUARE_SIZE:
                    board_array[prom_rank - 1][prom_file - 1].unoccupy()
                    all_pieces.pop(pawn_name)
                    new_name = pawn_name[0] + 'Q' + pawn_name[2]
                    all_pieces[new_name] = board.pieces.Queen(new_name, prom_file, prom_rank)
                    board_array[prom_rank - 1][prom_file - 1].occupy(all_pieces[new_name])
                    promotion = False
                    turn = 'b' if turn == 'w' else 'w'
                    board.pieces.game_so_far.append(current_move + " =" + new_name)
                    move_num = move_num + 1 if turn == 'w' else move_num
                    current_move = ""

                elif 3 * board.SQUARE_SIZE < another_pos[0] < 4 * board.SQUARE_SIZE < another_pos[1] \
                        < 5 * board.SQUARE_SIZE:
                    board_array[prom_rank - 1][prom_file - 1].unoccupy()
                    all_pieces.pop(pawn_name)
                    new_name = pawn_name[0] + 'N' + pawn_name[2]
                    all_pieces[new_name] = board.pieces.Knight(new_name, prom_file, prom_rank)
                    board_array[prom_rank - 1][prom_file - 1].occupy(all_pieces[new_name])
                    promotion = False
                    turn = 'b' if turn == 'w' else 'w'
                    board.pieces.game_so_far.append(current_move + " =" + new_name)
                    move_num = move_num + 1 if turn == 'w' else move_num
                    current_move = ""

                elif 3 * board.SQUARE_SIZE < another_pos[1] < 4 * board.SQUARE_SIZE < another_pos[0] \
                        < 5 * board.SQUARE_SIZE:
                    board_array[prom_rank - 1][prom_file - 1].unoccupy()
                    all_pieces.pop(pawn_name)
                    new_name = pawn_name[0] + 'R' + pawn_name[2]
                    all_pieces[new_name] = board.pieces.Rook(new_name, prom_file, prom_rank)
                    board_array[prom_rank - 1][prom_file - 1].occupy(all_pieces[new_name])
                    promotion = False
                    turn = 'b' if turn == 'w' else 'w'
                    board.pieces.game_so_far.append(current_move + " =" + new_name)
                    move_num = move_num + 1 if turn == 'w' else move_num
                    current_move = ""

                elif 4 * board.SQUARE_SIZE < another_pos[0] < 5 * board.SQUARE_SIZE and \
                        4 * board.SQUARE_SIZE < another_pos[1] < 5 * board.SQUARE_SIZE:
                    board_array[prom_rank - 1][prom_file - 1].unoccupy()
                    all_pieces.pop(pawn_name)
                    new_name = pawn_name[0] + 'B' + pawn_name[2]
                    all_pieces[new_name] = board.pieces.Bishop(new_name, prom_file, prom_rank)
                    board_array[prom_rank - 1][prom_file - 1].occupy(all_pieces[new_name])
                    promotion = False
                    turn = 'b' if turn == 'w' else 'w'
                    board.pieces.game_so_far.append(current_move + " =" + new_name)
                    move_num = move_num + 1 if turn == 'w' else move_num
                    current_move = ""

                continue

            else:
                continue

        all_possible_moves = []
        for piece_name in all_pieces:
            if piece_name[0] == turn:
                all_possible_moves = all_possible_moves + all_pieces[piece_name].moves(board_array)
        if len(all_possible_moves) == 0:
            mate = True

        all_other_moves = []
        for piece_name in all_pieces:
            if piece_name[0] != turn:
                all_other_moves = all_other_moves + all_pieces[piece_name].moves(board_array)
        king_square = board.pieces.find_king(board_array, turn)
        check = True if king_square in all_other_moves else False

        if pygame.mouse.get_pressed()[0] and not draw_game and not mate:
            pos = pygame.mouse.get_pos()
            new_file_num, new_rank_num = 1 + pos[0] // board.SQUARE_SIZE, 8 - pos[1] // board.SQUARE_SIZE

            if board_array[new_rank_num - 1][new_file_num - 1].possible:
                fifty_counter = fifty_counter + 0.5

                # en-passant:
                if board_array[current_rank_num-1][current_file_num-1].occupied.name[1] == 'P' and \
                        abs(current_file_num - new_file_num) == 1 and \
                        board_array[new_rank_num-1][new_file_num-1].occupied is None:
                    all_pieces.pop(board_array[current_rank_num-1][new_file_num-1].occupied.name)
                    board_array[current_rank_num - 1][new_file_num - 1].unoccupy()

                # castling:
                if board_array[current_rank_num-1][current_file_num-1].occupied.name[1] == 'K' and \
                        abs(current_file_num - new_file_num) == 2:
                    old_rook_file = 8 if new_file_num > current_file_num else 1
                    new_rook_file = 6 if new_file_num > current_file_num else 4
                    board_array[current_rank_num - 1][old_rook_file - 1].\
                        occupied.change_pos(new_rook_file, new_rank_num)
                    board_array[new_rank_num-1][new_rook_file-1].\
                        occupy(board_array[current_rank_num-1][old_rook_file-1].occupied)
                    board_array[current_rank_num-1][old_rook_file-1].unoccupy()

                if board_array[current_rank_num - 1][current_file_num - 1].occupied.name[1] == 'P':
                    fifty_counter = 0
                current_move = current_move + str(move_num) + ". " + board_array[current_rank_num-1][current_file_num-1].\
                    occupied.name + " " + board.rank_dict[current_file_num] + str(current_rank_num)
                board_array[current_rank_num - 1][current_file_num - 1].occupied.change_pos(new_file_num, new_rank_num)
                if board_array[new_rank_num-1][new_file_num-1].occupied:
                    fifty_counter = 0
                    current_move = current_move + " x" + board_array[new_rank_num-1][new_file_num-1].occupied.name
                    all_pieces.pop(board_array[new_rank_num - 1][new_file_num - 1].occupied.name)
                board_array[new_rank_num - 1][new_file_num - 1].\
                    occupy(board_array[current_rank_num - 1][current_file_num - 1].occupied)
                board_array[current_rank_num - 1][current_file_num - 1].unoccupy()
                current_move = current_move + " " + board.rank_dict[new_file_num] + str(new_rank_num)

                board_array[current_rank_num - 1][current_file_num - 1].remove_current()
                for sq in moves:
                    board_array[sq[1] - 1][sq[0] - 1].remove_possible()

                for pot_prom_file in range(1, 9):
                    for pot_prom_rank in [1, 8]:
                        if board_array[pot_prom_rank - 1][pot_prom_file - 1].occupied:
                            if board_array[pot_prom_rank - 1][pot_prom_file - 1].occupied.name[1] == 'P':
                                prom_file, prom_rank = pot_prom_file, pot_prom_rank
                                promotion = True

                if not promotion:
                    turn = 'b' if turn == 'w' else 'w'
                    board.pieces.game_so_far.append(current_move)
                    move_num = move_num + 1 if turn == 'w' else move_num
                    current_move = ""
                continue

            board_array[current_rank_num - 1][current_file_num - 1].remove_current()
            for sq in moves:
                board_array[sq[1] - 1][sq[0] - 1].remove_possible()

            current_file_num, current_rank_num = new_file_num, new_rank_num

            if board_array[current_rank_num-1][current_file_num-1].occupied and \
                    board_array[current_rank_num-1][current_file_num-1].occupied.colour == turn:
                board_array[current_rank_num-1][current_file_num-1].make_current()
                moves = board_array[current_rank_num - 1][current_file_num - 1].occupied.moves(board_array)
                for sq in moves:
                    board_array[sq[1]-1][sq[0]-1].make_possible()
    
        await asyncio.sleep(0)

asyncio.run(main())
