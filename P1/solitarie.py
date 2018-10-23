#content

def c_peg():
    return "O"

def c_empty():
    return "_"

def c_blocked():
    return "X"

def is_empty(e):
    return e==c_empty()

def is_peg(e):
    return e==c_peg()

def is_blocked(e):
    return e==c_blocked()

#position
#Tuple(line,column)

def make_pos(l,c):
    return (l,c)

def pos_l(pos):
    return pos[0]

def pos_c(pos):
    return pos[1]

#move
#List[pos_i,pos_f]

def make_move(i,f):
    return [i,f]

def move_initial(move):
    return move[0]

def move_final(move):
    return move[1]

def move_middle(move):
    l=(pos_l(move_initial(move))+pos_l(move_final(move)))//2
    c=(pos_c(move_initial(move))+pos_c(move_final(move)))//2    
    return make_pos(l,c)
    

#board
#List of Lists of content

#Board Operations
def board_dim(board):
    return (len(board),len(board[0]))

def board_lines(board):
    return board_dim(board)[0]

def board_cols(board):
    return board_dim(board)[1]

def pos_content(board,position):
    return board[pos_l(position)][pos_c(position)]

def change_pos_content(board,position,content):
    board[pos_l(position)][pos_c(position)]=content

#can move if inicial position is a piece, middle pos piece, last pos empty
def can_move(board,move):
    return is_peg(pos_content(board,move_initial(move))) and is_empty(pos_content(board,move_final(move))) and is_peg(pos_content(board,move_middle(move)))

#returns all the moves that can be made INTO the position.
#to get all the moves that can be made FROM the position, switch pos and i_pos in lines 'm=make_move()'
def position_moves(pos,board):
    moves=[]
    #not in left border
    if pos_c(pos)>=2:
        i_pos=make_pos(pos_l(pos),pos_c(pos)-2)
        m=make_move(i_pos,pos)
        if can_move(board,m):
            moves=moves+[m]
            
    #not in upper border
    if pos_l(pos)>=2:
        i_pos=make_pos(pos_l(pos)-2,pos_c(pos))
        m=make_move(i_pos,pos)
        if can_move(board,m):
            moves=moves+[m]
            
    #not in right border
    if pos_c(pos)<=board_cols(board)-3:
        i_pos=make_pos(pos_l(pos),pos_c(pos)+2)
        m=make_move(i_pos,pos)
        if can_move(board,m):
            moves=moves+[m]
            
    #not in lower border        
    if pos_l(pos)<=board_lines(board)-3:
        i_pos=make_pos(pos_l(pos)+2,pos_c(pos))
        m=make_move(i_pos,pos)
        if can_move(board,m):
            moves=moves+[m]
            
    return moves                                                                          

#returns a list with all the available moves in a board                                                                                  
def board_moves(board):
    moves=[]
    for i in range(board_lines(board)):
        for j in range(board_cols(board)):
            moves=moves+position_moves(make_pos(i,j),board)
    return moves

#returns a copy of a board
def board_cpy(board):
    board_cpy=[]
    for i in range(board_lines(board)):
        line_cpy=[]
        for j in range(board_cols(board)):
            line_cpy=line_cpy+[pos_content(board,make_pos(i,j))]
        board_cpy=board_cpy+[line_cpy]
    return board_cpy

#makes a move, initial board remains the same (makes a copy)        
def board_perform_move(board,move):
    if not can_move(board,move):
        return False
    board_cp=board_cpy(board)
    change_pos_content(board_cp,move_initial(move),c_empty())
    change_pos_content(board_cp,move_middle(move),c_empty())
    change_pos_content(board_cp,move_final(move),c_peg())
    return board_cp

#returns the number of pieces in a board. This should only be called in the initial board, then remove 1 piece for each move made
def board_pieces(board):
    pieces_number=0
    for i in range(board_lines(board)):
        for j in range(board_cols(board)):
            if is_peg(pos_content(board,make_pos(i,j))):
                pieces_number+=1
    return pieces_number
                                                                                  
