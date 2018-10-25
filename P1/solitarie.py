"""
______________________________________________________________________________
IA project 1
Luis Oliveira 83500
Samuel Arleo 94284
_______________________________________________________________________________
"""

from search import *
import time

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

# Return the coordinates of the position in the middle of the move
def move_middle(move):
    
    # intial posion
    l_initial = pos_l(move_initial(move))
    c_initial = pos_c(move_initial(move))
    
    # final position
    l_final =   pos_l(move_final(move))    
    c_final =   pos_c(move_final(move))
    
    #middle position    
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
def can_move(board,move):

    initial_content = pos_content(board,move_initial(move))
    middle_content  = pos_content(board,move_middle(move))
    final_content   = pos_content(board,move_final(move))
    
    return is_peg(initial_content) and is_peg(middle_content) and is_empty(final_content)

#returns all the moves that can be made INTO the position.
def position_moves(pos,board):
    moves=[]
    if not is_empty(pos_content(board,pos)):
        return moves

    #not in left border, checks move from two columns left
    if pos_c(pos)>=2:
        i_pos=make_pos(pos_l(pos),pos_c(pos)-2)
        m=make_move(i_pos,pos)
        if can_move(board,m):
            moves=moves+[m]
            
    #not in upper border, checks move from two lines up
    if pos_l(pos)>=2:
        i_pos=make_pos(pos_l(pos)-2,pos_c(pos))
        m=make_move(i_pos,pos)
        if can_move(board,m):
            moves=moves+[m]
            
    #not in right border, checks move from two columns right
    if pos_c(pos)<=board_cols(board)-3:
        i_pos=make_pos(pos_l(pos),pos_c(pos)+2)
        m=make_move(i_pos,pos)
        if can_move(board,m):
            moves=moves+[m]
            
    #not in lower border, checks move from two lines down      
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
    if can_move(board,move):
        board_cp=board_cpy(board)
        change_pos_content(board_cp,move_initial(move),c_empty())
        change_pos_content(board_cp,move_middle(move),c_empty())
        change_pos_content(board_cp,move_final(move),c_peg())
        return board_cp
    return False

#returns the number of pieces in a board. This should only be called in the initial 
#board, then remove 1 piece for each move made
def board_pieces(board):
    pieces_number=0
    for i in range(board_lines(board)):
        for j in range(board_cols(board)):
            if is_peg(pos_content(board,make_pos(i,j))):
                pieces_number = pieces_number + 1
    return pieces_number                                                                   


class sol_state:

    """
    A state in the search tree. It stores the current board produced 
    after all the actions performed before in the parent nodes
    """
    def __init__(self, board, pieces):
        self.board = board
        self.pieces= pieces
        self.corners=corner_pieces(board)
        self.moves=board_moves(board)
        self.isolated=isolated(board)
        self.distance=distance(board)
        
    def __lt__(self, other):
        return self.pieces<=other.pieces

    def __repr__(self):
        b = "\n"
        for line in range(board_lines(self.board)):
            b = b + str(get_board_line(self.board,line)) + "\n"
        return b

class solitaire(Problem):    
    """
    Game problem class
    """
    def __init__(self, board):
        self.initial=sol_state(board,board_pieces(board))

    # Returns all the possible actions from the given state
    def actions(self, state):
        return state.moves

    # Returns the new state with the action performed to the board
    def result(self, state, action):
        board = board_perform_move(state.board, action)
        pieces = state.pieces-1
        return sol_state(board,pieces)

    # Stop condition for the search alg. when there is one piece left on the board
    def goal_test(self, state):
        return state.pieces==1

    def h(self,node):
        return node.state.pieces*node.state.distance*node.state.isolated*node.state.corners/(len(node.state.moves)+1)

#Prints time, moves, and states from 'S' search in board 'board'
def solve(n,S):
    
    game = solitaire(boards(n))
    print(game.initial)
    
    Problem=InstrumentedProblem(game)
    
    i_time=time.time()
    
    if S=='DFS':
        #DFS SEARCH
        result_dfs = depth_first_tree_search(Problem)
        dfs_time = time.time() - i_time
        print("DFS:\n", dfs_time, '\n', result_dfs.solution(),'\n', result_dfs.path(),'\n')
        return
    
    if S=='Greedy':
        #GREEDY SEARCH
        result_gan = greedy_best_first_graph_search(Problem,Problem.h)
        gan_time = time.time() - i_time        
        print("GREEDY:\n", gan_time, '\n', result_gan.solution(),'\n', result_gan.path(),'\n')
        return

    if S=='A*':
        #ASTAR SEARCH
        result_astar = astar_search(Problem)
        astar_time = time.time() - i_time
        print("A*:\n", astar_time, '\n', result_astar.solution(),'\n', result_astar.path(),'\n')
        return

def boards(n):    
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
    
    switch={0:b0,1:b1,2:b2,3:b3,4:b4}   
    return switch[n]
    

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
    return (int(round(x/n)), int(round(y/n)))

def distance(board):
    distance=0
    center=center_of_mass(board)
    for i in range(board_lines(board)):
        for j in range(board_cols(board)):
            if is_peg(pos_content(board,make_pos(i,j))):
                distance=distance+i-center[0]+j-center[1]
    return distance
            

#number of pieces at the edge of the board, not counting 'X'. corners count twice. 
def corner_pieces(board):
    pieces=0
    lines=board_lines(board)
    cols=board_cols(board)
    for i in range(cols):
        if is_peg(pos_content(board,make_pos(0,i))):
            pieces+=1
        if is_peg(pos_content(board,make_pos(lines-1,i))):
            pieces+=1
    for i in range(lines):
        if is_peg(pos_content(board,make_pos(i,0))):
            pieces+=1
        if is_peg(pos_content(board,make_pos(i,cols-1))):
            pieces+=1        
    return pieces


def is_alone(board,pos):
    if not is_peg(pos_content(board,pos)):
        return False            
    if pos_l(pos)>0:
        if is_peg(pos_content(board,make_pos(pos_l(pos)-1,pos_c(pos)))):
            return False
    if pos_c(pos)>0:
        if is_peg(pos_content(board,make_pos(pos_l(pos),pos_c(pos)-1))):
            return False
    if pos_l(pos)<board_lines(board)-1:
        if is_peg(pos_content(board,make_pos(pos_l(pos)+1,pos_c(pos)))):
            return False   
    if pos_c(pos)<board_cols(board)-1:
        if is_peg(pos_content(board,make_pos(pos_l(pos),pos_c(pos)+1))):
            return False
    return True

def isolated(board):
    pieces=0
    for i in range(board_lines(board)):
        for j in range(board_cols(board)):
            if is_alone(board,make_pos(i,j)):
                pieces+=1
    return pieces
            