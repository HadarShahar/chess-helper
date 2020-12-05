from selenium import webdriver
import chess
import chess.engine
# from stockfish import Stockfish
from secrets import USERNAME, PASSWORD

CHESS_ANALYSIS_URL = "https://www.chess.com/analysis"
CHESS_LOGIN_URL = "https://www.chess.com/login_and_go?returnUrl=https%3A%2F%2Fwww.chess.com%2F"
CHROME_DRIVER_PATH = "chromedriver"

ANALYSIS_DIV_CLASS = "board v-board rounded"
ONLINE_DIV_CLASS = "board v-board chessboard-component"
MARKED_DIV_COLOR = "cyan"

STOCKFISH_PATH = "stockfish-11-win\Windows\stockfish_20011801_x64_modern.exe"
ENGINE_TIME_LIMIT = 0.5
# ENGINE_DEPTH_LIMIT = 20
online_game = True


def login(driver):
    driver.get(CHESS_LOGIN_URL)
    driver.find_element_by_id("username").send_keys(USERNAME)
    driver.find_element_by_id("password").send_keys(PASSWORD)


def find_pieces(driver, board):
    """
    finds all the pieces on the board in the website and
    marks them in the board object

    For example:
        piece_class = 'piece square-0101'
        piece_img_url = 'url("https://images.chesscomfiles.com/chess-themes/pieces/neo/150/wr.png")'

        piece_x, piece_y = 1, 1
        piece_name = 'wr'

        square_name = 'a1'
        square_num = 0
    """
    pieces_div = driver.find_element_by_class_name("pieces")
    pieces = pieces_div.find_elements_by_css_selector(
        "*")  # find all the elements inside the pieces_div
    for piece in pieces:
        piece_class = piece.get_attribute("class")
        piece_img_url = piece.value_of_css_property("background-image")
        piece_pos = piece_class.split('-')[1]

        piece_x, piece_y = int(piece_pos[:2]), int(
            piece_pos[2:])  # starts at 1,1
        piece_name = piece_img_url.split('/')[-1].split('.png')[0]

        piece_color = chess.WHITE if piece_name[0] == 'w' else chess.BLACK
        piece_type = chess.PIECE_SYMBOLS.index(piece_name[1])

        square_name = chess.FILE_NAMES[piece_x-1] + \
            str(piece_y)  # chess.FILE_NAMES starts at 0
        square_num = chess.SQUARE_NAMES.index(square_name)

        board.set_piece_at(square_num, chess.Piece(piece_type, piece_color))
        # print(piece_name, (piece_x, piece_y))


def main():
    driver = webdriver.Chrome(CHROME_DRIVER_PATH)
    if online_game:
        login(driver)
    else:
        driver.get(CHESS_ANALYSIS_URL)

    engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
    # stockfish = Stockfish(STOCKFISH_PATH)
    current_color = 'w'
    while True:
        try:
            board = chess.Board()
            board.clear()

            color = input(
                f"Enter your color [w/b] or press 'Enter' to continue as {current_color}...")
            if color in ['w', 'b']:
                current_color = color
            if current_color == 'w':
                board.turn = chess.WHITE
            elif current_color == 'b':
                board.turn = chess.BLACK

            find_pieces(driver, board)
            print(board)

            # fen = board.fen()
            # if current_color == 'b':
            #     # flip the colors on the board,
            #     # because get_best_move() returns the best move for white
            #     new_fen = ''
            #     for char in fen:
            #         if char.isalpha():
            #             char = char.upper() if char.islower() else char.lower()
            #         new_fen += char
            #     fen = new_fen
            # stockfish.set_fen_position(fen)
            # best_move = stockfish.get_best_move()
            # print(best_move)

            result = engine.play(
                board, chess.engine.Limit(time=ENGINE_TIME_LIMIT))
            # result = engine.play(board, chess.engine.Limit(depth=ENGINE_DEPTH_LIMIT))

            best_move = str(result.move)
            print(best_move)
            for square in [best_move[:2], best_move[2:]]:
                square_x = chess.FILE_NAMES.index(square[0]) + 1
                square_y = square[1]

                # <div class="square square-0502 marked-square" style="background-color: cyan;"></div>

                execu = f"""
                let parentDiv = document.getElementsByClassName("{ONLINE_DIV_CLASS if online_game else ANALYSIS_DIV_CLASS}")[0];
                let markedDiv = document.createElement("div");
                markedDiv.style.backgroundColor = "{MARKED_DIV_COLOR}";
                markedDiv.setAttribute('class', 'square square-0{square_x}0{square_y} marked-square');
                parentDiv.appendChild(markedDiv);
                """
                driver.execute_script(execu)
        except Exception as e:
            print(e)

        print('=' * 70)
    # engine.quit()


if __name__ == '__main__':
    main()
