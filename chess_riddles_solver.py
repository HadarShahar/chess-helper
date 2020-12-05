"""
    This script isn't related to the original chess helper program, 
    but it's another program that helps you in chess - 
    it solves chess riddles (mate in x puzzles).

    K king, Q queen, R rook, B bishop, N knight, P pawn

    For white:
    K, Q, R, B, N, P

    For black:
    k, q, r, b, n, p

"""
white_pieces = ['K', 'Q', 'R', 'B', 'N', 'P']
black_pieces = ['k', 'q', 'r', 'b', 'n', 'p']

THREAT = '*'
# board = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#          [' ', ' ', ' ', 'k', ' ', ' ', 'p', ' '],
#          [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'P'],
#          [' ', 'K', ' ', ' ', ' ', ' ', ' ', ' '],
#          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]

# https://www.chess.com/forum/view/more-puzzles/mate-in-3-puzzles

# https://www.chess.com/forum/view/more-puzzles/forced-mate-in-3
# board = [[' ', 'k', 'r', ' ', ' ', ' ', ' ', ' '],
#          ['p', 'p', 'N', ' ', ' ', 'p', 'p', 'r'],
#          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#          [' ', ' ', ' ', 'p', ' ', ' ', 'n', ' '],
#          [' ', ' ', ' ', 'b', 'b', ' ', ' ', ' '],
#          [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#          ['n', ' ', ' ', ' ', 'P', 'P', 'P', 'Q'],
#          [' ', ' ', ' ', ' ', 'R', ' ', 'K', ' ']]

# https://www.reddit.com/r/chess/comments/bn2gj0/from_a_game_this_morning_white_to_move_forced/
# board = [[' ', ' ', 'r', ' ', ' ', ' ', ' ', 'r'],
#          [' ', ' ', ' ', ' ', ' ', ' ', 'R', ' '],
#          ['p', ' ', ' ', ' ', ' ', 'p', ' ', ' '],
#          [' ', 'p', ' ', 'Q', 'q', 'k', 'p', ' '],
#          [' ', ' ', ' ', 'P', ' ', ' ', 'N', 'p'],
#          ['P', ' ', ' ', ' ', ' ', 'N', ' ', 'P'],
#          [' ', 'P', ' ', ' ', ' ', 'P', 'P', ' '],
#          [' ', ' ', ' ', ' ', ' ', ' ', 'K', ' ']]

board = [['k', ' ', 'n', 'r', 'r', 'b', ' ', ' '],
         ['p', 'R', 'R', ' ', ' ', ' ', 'p', ' '],
         ['B', 'p', ' ', ' ', ' ', ' ', ' ', 'p'],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', 'P', 'B', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', 'P', ' ', ' '],
         [' ', 'P', ' ', ' ', ' ', ' ', 'P', 'P'],
         [' ', 'K', ' ', ' ', ' ', ' ', ' ', ' ']]


possible_moves = []
is_check = False
last_boards = []
solution = []


def print_board(b):
    print('=' * 30)
    for i, row in enumerate(b):
        for j, piece in enumerate(row):
            if piece == ' ':
                print(' ', end=' ')
            else:
                print(piece, end=' ')
        print()
    print('=' * 30)
    # for row in b:
    #     print(row)


def mark_specific_threat(copy, piece, last_i, last_j, i, j):
    global possible_moves, is_check
    ret_val = False
    # if board[i][j] == ' ':
    #     copy[i][j] = THREAT
    #     ret_val = True
    # if (piece in white_pieces and board[i][j] == 'k') or \
    #         (piece in black_pieces and board[i][j] == 'K'):
    #     is_check = True
    # elif piece not in 'Pp':
    #     if (piece in white_pieces and board[i][j] not in white_pieces) or \
    #             (piece in black_pieces and board[i][j] not in black_pieces):
    #         possible_moves.append([piece, i, j])

    if (piece in white_pieces and board[i][j] == 'k') or \
            (piece in black_pieces and board[i][j] == 'K'):
        is_check = True
    else:
        if copy[i][j] not in 'Kk':
            copy[i][j] = THREAT
        if board[i][j] == ' ':
            ret_val = True
        if piece not in 'Pp':
            if (piece in white_pieces and board[i][j] not in white_pieces) or \
                    (piece in black_pieces and board[i][j] not in black_pieces):
                possible_moves.append([piece, last_i, last_j, i, j])
    return ret_val


def mark_rook_threats(copy, piece, i, j):
    for n in range(i - 1, -1, -1):
        if not mark_specific_threat(copy, piece, i, j, n, j):
            break
    for n in range(i + 1, 8):
        if not mark_specific_threat(copy, piece, i, j, n, j):
            break
    for n in range(j - 1, -1, -1):
        if not mark_specific_threat(copy, piece, i, j, i, n):
            break
    for n in range(j + 1, 8):
        if not mark_specific_threat(copy, piece, i, j, i, n):
            break


def mark_bishop_threats(copy, piece, i, j):
    i1 = i - 1
    j1 = j - 1
    while i1 >= 0 and j1 >= 0:
        if not mark_specific_threat(copy, piece, i, j, i1, j1):
            break
        i1 -= 1
        j1 -= 1
    i1 = i + 1
    j1 = j + 1
    while i1 < 8 and j1 < 8:
        if not mark_specific_threat(copy, piece, i, j, i1, j1):
            break
        i1 += 1
        j1 += 1
    i1 = i + 1
    j1 = j - 1
    while i1 < 8 and j1 >= 0:
        if not mark_specific_threat(copy, piece, i, j, i1, j1):
            break
        i1 += 1
        j1 -= 1
    i1 = i - 1
    j1 = j + 1
    while i1 >= 0 and j1 < 8:
        if not mark_specific_threat(copy, piece, i, j, i1, j1):
            break
        i1 -= 1
        j1 += 1


def mark_threats(pieces_set):
    global possible_moves, is_check
    possible_moves = []
    is_check = False
    pieces = pieces_set
    copy = [row[:] for row in board]
    for i, row in enumerate(board):
        for j, piece in enumerate(row):
            if piece == ' ':
                continue
            if piece == pieces[0]:
                # K / k
                if i > 0:
                    for n in range(-1, 2):
                        if 0 <= j + n < 8:
                            mark_specific_threat(
                                copy, pieces[0], i, j, i - 1, j + n)
                if i < 7:
                    for n in range(-1, 2):
                        if 0 <= j + n < 8:
                            mark_specific_threat(
                                copy, pieces[0], i, j, i + 1, j + n)
                if j > 0:
                    mark_specific_threat(copy, pieces[0], i, j, i, j - 1)
                if j < 7:
                    mark_specific_threat(copy, pieces[0], i, j, i, j + 1)

            elif piece == pieces[1]:
                # Q / q
                mark_rook_threats(copy, pieces[1], i, j)
                mark_bishop_threats(copy, pieces[1], i, j)
            elif piece == pieces[2]:
                # R / r
                mark_rook_threats(copy, pieces[2], i, j)
            elif piece == pieces[3]:
                # B / b
                mark_bishop_threats(copy, pieces[3], i, j)
            elif piece == pieces[4]:
                # N / n
                # top
                if i > 1:
                    if j > 0:
                        mark_specific_threat(
                            copy, pieces[4], i, j, i - 2, j - 1)
                    if j < 7:
                        mark_specific_threat(
                            copy, pieces[4], i, j, i - 2, j + 1)
                # sides
                if i > 0:
                    if j > 1:
                        mark_specific_threat(
                            copy, pieces[4], i, j, i - 1, j - 2)
                    if j < 6:
                        mark_specific_threat(
                            copy, pieces[4], i, j, i - 1, j + 2)
                # sides
                if i < 7:
                    if j > 1:
                        mark_specific_threat(
                            copy, pieces[4], i, j, i + 1, j - 2)
                    if j < 6:
                        mark_specific_threat(
                            copy, pieces[4], i, j, i + 1, j + 2)
                # bottom
                if i < 6:
                    if j > 0:
                        mark_specific_threat(
                            copy, pieces[4], i, j, i + 2, j - 1)
                    if j < 7:
                        mark_specific_threat(
                            copy, pieces[4], i, j, i + 2, j + 1)
            elif piece == pieces[5]:
                # P / p
                if piece == 'P':  # white pawn
                    if i > 0:
                        if j > 0:
                            mark_specific_threat(
                                copy, pieces[5], i, j, i - 1, j - 1)
                        if j < 7:
                            mark_specific_threat(
                                copy, pieces[5], i, j, i - 1, j + 1)
                        if board[i - 1][j] == ' ':
                            possible_moves.append([piece, i, j, i - 1, j])
                else:  # black pawn
                    if i < 7:
                        if j > 0:
                            mark_specific_threat(
                                copy, pieces[5], i, j, i + 1, j - 1)
                        if j < 7:
                            mark_specific_threat(
                                copy, pieces[5], i, j, i + 1, j + 1)
                        if board[i + 1][j] == ' ':
                            possible_moves.append([piece, i, j, i + 1, j])
    return copy


def execute_move(move):
    copy = [row[:] for row in board]
    last_boards.append(copy)
    piece, last_i, last_j, i, j = move
    board[last_i][last_j] = ' '
    board[i][j] = piece


# def undo_move(move):
#     piece, last_i, last_j, i, j = move
#     board[i][j] = ' '
#     board[last_i][last_j] = piece
def undo_move():
    global board
    copy = last_boards.pop()
    board = [row[:] for row in copy]


def remove_forbidden_white_moves(white_poss_moves):
    del_white_moves = []
    for move in white_poss_moves:
        # piece, last_i, last_j, i, j = move
        # if piece == 'K':
        #     if black_threats[i][j] == THREAT:
        #         del_white_moves.append(move)
        #         continue

        execute_move(move)
        black_threats = mark_threats(black_pieces)
        check_for_white = is_check
        if check_for_white:
            del_white_moves.append(move)
        undo_move()

    for move in del_white_moves:
        white_poss_moves.remove(move)


def remove_forbidden_black_moves(black_poss_moves):
    del_black_moves = []
    for move in black_poss_moves:
        # piece, last_i, last_j, i, j = move
        # if piece == 'k':
        #     if white_threats[i][j] == THREAT:
        #         del_black_moves.append(move)
        #         continue

        execute_move(move)
        white_threats = mark_threats(white_pieces)
        check_for_black = is_check
        if check_for_black:
            del_black_moves.append(move)
        undo_move()

    for move in del_black_moves:
        black_poss_moves.remove(move)


def solve(moves_num):
    mark_threats(white_pieces)
    white_poss_moves = [move[:] for move in possible_moves]
    check_for_black = is_check
    remove_forbidden_white_moves(white_poss_moves)

    # check for mate
    if moves_num == 0:
        if check_for_black:
            mark_threats(black_pieces)
            black_poss_moves = [move[:] for move in possible_moves]
            remove_forbidden_black_moves(black_poss_moves)
            if len(black_poss_moves) == 0:
                return True
        return False

    for white_move in white_poss_moves:
        execute_move(white_move)

        mark_threats(black_pieces)
        black_poss_moves = [move[:] for move in possible_moves]
        remove_forbidden_black_moves(black_poss_moves)

        if len(black_poss_moves) == 0:
            if solve(moves_num - 1):
                return True

        # for black_move in black_poss_moves:
        #     execute_move(black_move)
        if len(black_poss_moves) == 1:  # if it's a forced mate
            execute_move(black_poss_moves[0])
            if solve(moves_num - 1):
                return True
            undo_move()
        undo_move()


def main():
    white_threats = mark_threats(white_pieces)
    white_poss_moves = [move[:] for move in possible_moves]
    check_for_black = is_check
    # print_board(white_threats)

    black_threats = mark_threats(black_pieces)
    black_poss_moves = [move[:] for move in possible_moves]
    check_for_white = is_check
    # print_board(black_threats)

    remove_forbidden_white_moves(white_poss_moves)
    remove_forbidden_black_moves(black_poss_moves)

    print('white_poss_moves: ', len(white_poss_moves), white_poss_moves)
    print('check_for_white: ', check_for_white)
    print('black_poss_moves: ', len(black_poss_moves), black_poss_moves)
    print('check_for_black: ', check_for_black)

    solve(2)

    for b in last_boards:
        print_board(b)
    print_board(board)

    # TODO solve pawns problems - pawn can eat a piece!!!!!!!!!!!!!!!!
    # TODO remove all threats arrs
    # TODO save last moves and not boards


if __name__ == '__main__':
    main()
