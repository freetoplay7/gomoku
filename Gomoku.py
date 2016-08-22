"""Gomoku board game
Author: Jiaxi Kang
"""

def is_empty(board):
    for i in range(len(board)):
      for j in range(len(board[0])):
        if board[i][j] != " ":
          return False
    return True
    

def is_bounded(board, y_end, x_end, length, d_y, d_x):
    """Determines whether a sequence of pieces are bounded on both sides, one side,
    or none"""
    
    bound_end_y = y_end + d_y
    bound_end_x = x_end + d_x
    bound_beg_y = y_end - length * d_y
    bound_beg_x = x_end - length * d_x
  
    open_range = range(0, 8)
    
    if bound_end_y in open_range and bound_end_x in open_range and bound_beg_y\
    in open_range and bound_beg_x in open_range:
      
      bound_end = board[bound_end_y][bound_end_x]
      bound_beg = board[bound_beg_y][bound_beg_x]
      
      if bound_end == " " and bound_beg == " ":
        bound = "OPEN"
      elif (bound_end == " ") ^ (bound_beg == " "):
        bound = "SEMIOPEN"
      else:
        bound = "CLOSED"
    
    else:
        if bound_end_y in open_range and bound_end_x in open_range:
            bound_end = board[bound_end_y][bound_end_x] 
            
            if bound_end == " ":
                bound = "SEMIOPEN"
            else:
                bound = "CLOSED"
        
        elif bound_beg_y in open_range and bound_beg_x in open_range:
            bound_beg = board[bound_beg_y][bound_beg_x] 
            
            if bound_beg == " ":
                bound = "SEMIOPEN"
            else:
                bound = "CLOSED"
    
        else:
            bound = "CLOSED"
            
    return bound
    
    
def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count, semi_open_seq_count = 0, 0
    
    y = y_start
    x = x_start
    
    len = 0
    while x in range(8) and y in range(8):
      if board[y][x] == col:
        
        while (y + len * d_y < 8) and (x + len * d_x < 8):
          if board[y + len * d_y][x + len * d_x] == col:
            len += 1
          else:
            break
        
        if len == length:
          y_end = y + (length-1) * d_y
          x_end = x + (length-1) * d_x
          if is_bounded(board, y_end, x_end, length, d_y, d_x) == "OPEN":
            open_seq_count += 1
          if is_bounded(board, y_end, x_end, length, d_y, d_x) == "SEMIOPEN":
            semi_open_seq_count += 1
      
      if len == 0:
        x += d_x
        y += d_y
      else:
        y += len * d_y
        x += len * d_x
      len = 0

    return open_seq_count, semi_open_seq_count
    
def detect_rows(board, col, length):
    """Determines the number of open or semi-open sequences on the board for a particular
    player"""
    
    open_seq_count, semi_open_seq_count = 0, 0
    
    for i in range(8):
        y_start = i
        x_start = 0
        open_seq_count += detect_row(board, col, y_start, x_start, length, 0, 1)[0]
        semi_open_seq_count += detect_row(board, col, y_start, x_start, length, 0, 1)[1]
        
    for i in range(8):
        y_start = 0
        x_start = i
        open_seq_count += detect_row(board, col, y_start, x_start, length, 1, 0)[0]
        semi_open_seq_count += detect_row(board, col, y_start, x_start, length, 1, 0)[1] 
    
    for i in range(8):
        y_start = 7 - i
        x_start = 0
        open_seq_count += detect_row(board, col, y_start, x_start, length, 1, 1)[0]
        semi_open_seq_count += detect_row(board, col, y_start, x_start, length, 1, 1)[1] 
    
    for i in range(7):
        y_start = 0
        x_start = i + 1
        open_seq_count += detect_row(board, col, y_start, x_start, length, 1, 1)[0]
        semi_open_seq_count += detect_row(board, col, y_start, x_start, length, 1, 1)[1] 
        
    for i in range(8):
        y_start = i
        x_start = 7
        open_seq_count += detect_row(board, col, y_start, x_start, length, 1, -1)[0]
        semi_open_seq_count += detect_row(board, col, y_start, x_start, length, 1, -1)[1] 
    
    for i in range(7):
        y_start = 0
        x_start = 6 - i
        open_seq_count += detect_row(board, col, y_start, x_start, length, 1, -1)[0]
        semi_open_seq_count += detect_row(board, col, y_start, x_start, length, 1, -1)[1] 
          
    return open_seq_count, semi_open_seq_count
    
    
    
def search_max(board):
    """Determines the best possible position for a computer to place their piece on the board"""
    
    max_score = -1000000
    
    for i in range(8):
        for j in range(8):
            if board[i][j] == " ":
                board[i][j] = "b"
                max_score = max(score(board), max_score)
                board[i][j] = " "
    
    for i in range(8):
        for j in range(8):
            if board[i][j] == " ":
                board[i][j] = "b"
                if score(board) == max_score:
                    move_y = i
                    move_x = j
                board[i][j] = " "
                
    
    return move_y, move_x
    
def score(board):
    MAX_SCORE = 100000
    
    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}
    
    for i in range(2, 7):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)
        
    
    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE
    
    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE
        
    return (-10000 * (open_w[4] + semi_open_w[4])+ 
            500  * open_b[4]                     + 
            50   * semi_open_b[4]                + 
            -100  * open_w[3]                    + 
            -30   * semi_open_w[3]               + 
            50   * open_b[3]                     + 
            10   * semi_open_b[3]                +  
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])

    
def is_win(board):
    status = "Continue playing"
    
    for i in range(8): #checking rows
        for j in range(4):
            if board[i][j] == "b" and board[i][j+1] == "b" and board[i][j+2] ==\
            "b"and board[i][j+3] == "b" and board[i][j+4] == "b":
                status = "Black won"
            
            if board[i][j] == "w" and board[i][j+1] == "w" and board[i][j+2] ==\
            "w"and board[i][j+3] == "w" and board[i][j+4] == "w":
                status = "White won"
    
    for i in range(4):
        for j in range(8):
            if board[i][j] == "b" and board[i+1][j] == "b" and board[i+2][j] ==\
            "b"and board[i+3][j] == "b" and board[i+4][j] == "b":
                status = "Black won"
            
            if board[i][j] == "w" and board[i+1][j] == "w" and board[i+2][j] ==\
            "w"and board[i+3][j] == "w" and board[i+4][j] == "w":
                status = "White won"
    
    for i in range(4):
        for j in range(4):
            if board[i][7-j] == "b" and board[i+1][6-j] == "b" and board[i+2][5-j] ==\
            "b"and board[i+3][4-j] == "b" and board[i+4][3-j] == "b":
                status = "Black won"
            
            if board[i][7-j] == "w" and board[i+1][6-j] == "w" and board[i+2][5-j] ==\
            "w"and board[i+3][4-j] == "w" and board[i+4][3-j] == "w":
                status = "White won" 
    
    
            
    return status
    
def print_board(board):
    
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"
    
    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1]) 
    
        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"
    
    print(s)
    
    

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board
                


def analysis(board):
    """Prints out the sequences that each player currently has"""
    
    for c, full_name in [["w", "White"], ["b", "Black"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))
        
    
    
def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    
    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)
            
        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
            
            
        
        
        
        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
            
            
def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col        
        y += d_y
        x += d_x


            
if __name__ == '__main__':
    print(play_gomoku(8))
    
