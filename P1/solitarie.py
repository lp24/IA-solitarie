"""
_______________________________________________________________________________
IA project 1
Luis Oliveira
Samuel Arleo 94284
_______________________________________________________________________________

"""

from search import Problem, Node, depth_first_tree_search
import time

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

# Return the coordinates of the position in the middle of the move
def move_middle(move):
    
    # Lines of the initial and final positions involved in the move
    l_initial = pos_l(move_initial(move))
    l_final =   pos_l(move_final(move))

    # Columns of the initial and final positions involved in the move
    c_initial = pos_c(move_initial(move))
    c_final =   pos_c(move_final(move))
    
    l = ( l_initial + l_final ) // 2
    c = ( c_initial + c_final ) // 2    
    return make_pos(l,c)
    

#board
#List of Lists of content

def board_dim(board):
    return (len(board),len(board[0]))

def board_lines(board):
    return board_dim(board)[0]

def board_cols(board):
    return board_dim(board)[1]

def get_board_line(board, line):
    return board[line]

def pos_content(board,position):
    return board[pos_l(position)][pos_c(position)]

def change_pos_content(board,position,content):
    board[pos_l(position)][pos_c(position)]=content

# Checks if "move" is a correct play in given board
# *!* check if move positions have the same row or column?
def can_move(board,move):
    
    # Getting the content of the board in the initial, middle and final
    # positions of the movement
    initial_content = pos_content(board,move_initial(move))
    middle_content  = pos_content(board,move_middle(move))
    final_content   = pos_content(board,move_final(move))
    
    return is_peg(initial_content) and is_peg(middle_content) and is_empty(final_content)

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
            pos = make_pos(i,j)
            content = pos_content(board, pos)
            moves = moves + position_moves(pos,board)
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

#returns the number of pieces in a board. This should only be called in the initial 
#board, then remove 1 piece for each move made
def board_pieces(board):
    pieces_number=0
    for i in range(board_lines(board)):
        for j in range(board_cols(board)):
            if is_peg(pos_content(board,make_pos(i,j))):
                pieces_number = pieces_number + 1
    return pieces_number                                                                   

# Checks if the game is finished (1 piece left)
def game_finished(board):
    return board_pieces(board) == 1

# Coordinates where the most amount of pieces is located (could be float). This 
# could be used as an heuristic to try to head the moves towards the sections with 
# more pieces. Give more priority to those who are far from the center of mass
# This might be too complex
def center_of_mass(board):

    x = 0           # Column coordinates of the CoM
    y = 0           # Row coordinates of the CoM
    n = 0           # Number of pieces
    
    for i in range(board_lines(board)):
        for j in range(board_cols(board)):
            if is_peg(pos_content(board,make_pos(i,j))):
                x += j
                y += i
                n += 1
    return (x/n, y/n)

class solitarie(Problem):
    
    """
    Game problem class
    """

    def __init__(self, board):
        Problem.__init__(self, board)

    # Returns all the possible actions from the given state
    def actions(self, state):
        return board_moves(state.board)

    # Returns the new state with the action performed to the board
    def result(self, state, action):
        new_board = board_perform_move(state.board, action)
        return sol_state(new_board)

    # Stop condition for the search alg. when there is one piece left on the board
    def goal_test(self, state):
        #return state.pieces == 1 
        return game_finished(state.board)

class sol_state:

    """
    A state in the search tree. It stores the current board produced 
    after all the actions performed before in the parent nodes
    """

    def __init__(self, board):
        self.board = board

    def __repr__(self):

        b = "\n"
        lines = board_lines(self.board)
        for f in range(0, lines):
            if f != lines - 1:
                b = b + str(get_board_line(self.board,f)) + "\n"
            else:
                b = b + str(get_board_line(self.board,f))
        return b

def solving_times(board):


    # Defining the initial state with the original board
    initial = sol_state(board)

    print(initial)

    print(center_of_mass(board))

    # Creating a solitarie Problem instance
    problem = solitarie(initial)

    # Delete when all searches are defined
    result_dfs = None
    astar_time = None
    gan_time = None

    dfs_prev_time = time.time()
    result_dfs = depth_first_tree_search(problem)
    dfs_time = time.time() - dfs_prev_time

    print(result_dfs)

    """
    result_gan = best_first_graph_search(problem, f)
    gan_time = time.time() - dfs_time

    result_astar = astar_search(problem)
    astar_time = time.time() - gan_time
    """

    return {"dfs_time":dfs_time, "astar_time":astar_time, "gan_time":gan_time}



if __name__ == "__main__":

    O = c_peg()
    X = c_blocked()
    _ = c_empty()

    b0 =   [[_,_,O],
            [O,O,O],
            [O,O,O]]

    b1 =   [[_,O,O,O,_],
            [O,_,O,_,O],
            [_,O,_,O,_],
            [O,_,O,_,_],
            [_,O,_,_,_]]

    b2 =   [[O,O,O,X],
            [O,O,O,O],
            [O,_,O,O],
            [O,O,O,O]]

    b3 =   [[O,O,O,X,X],
            [O,O,O,O,O],
            [O,_,O,_,O],
            [O,O,O,O,O]]

    b4 =   [[O,O,O,X,X,X],
            [O,_,O,O,O,O],
            [O,O,O,O,O,O],
            [O,O,O,O,O,O]]

    b2_times = solving_times(b2)
    
    print(b2_times)