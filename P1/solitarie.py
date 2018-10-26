"""
____________________________________________________________________________
IA project 1 - Peg Solitaire

Group 43:
Luis Oliveira 83500
Samuel Arleo 94284
_______________________________________________________________________________
"""

from search import *
import time

"""

Global variables

"""

# Number of nodes generated
gerados = 1                     # 1 because the root is not considered

# Number of nodes expanded
expandidos = 0

"""

Content TAI
Peg='O', Empty='_', Blocked='X'

"""

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

"""

Position TAI
Tuple(line,column)

"""
def make_pos(l,c):
    return (l,c)

def pos_l(pos):
    return pos[0]

def pos_c(pos):
    return pos[1]

"""

Move TAI
List[pos_i,pos_f]

"""

def make_move(i,f):
    return [i,f]

def move_initial(move):
    return move[0]

def move_final(move):
    return move[1]

"""

Auxiliary Move Function

"""
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
    
"""

Board TAI
List of Lists of content

"""

#Constructor not necessary

def board_dim(board):
    return (len(board),len(board[0]))

def get_board_line(board, line):
    return board[line]

def pos_content(board,position):
    return board[pos_l(position)][pos_c(position)]

def change_pos_content(board,position,content):
    board[pos_l(position)][pos_c(position)]=content
    
#returns a copy of a board
def board_cpy(board):
    board_cpy=[]
    for i in range(board_lines(board)):
        line_cpy=[]
        for j in range(board_cols(board)):
            line_cpy=line_cpy+[pos_content(board,make_pos(i,j))]
        board_cpy=board_cpy+[line_cpy]
    return board_cpy    
    
"""

Auxiliary Board Functions

"""

def board_lines(board):
    return board_dim(board)[0]

def board_cols(board):
    return board_dim(board)[1]

# Checks if "move" is a correct play in "board"
def can_move(board,move):

    initial_content = pos_content(board,move_initial(move))
    middle_content  = pos_content(board,move_middle(move))
    final_content   = pos_content(board,move_final(move))
    
    return is_peg(initial_content) and is_peg(middle_content) and is_empty(final_content)

#Returns all the moves that can be made INTO a position.
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

"""

Requested Functions

"""

#makes a move, initial board remains the same (makes a copy)       
def board_perform_move(board,move):
    if can_move(board,move):
        board_cp=board_cpy(board)
        change_pos_content(board_cp,move_initial(move),c_empty())
        change_pos_content(board_cp,move_middle(move),c_empty())
        change_pos_content(board_cp,move_final(move),c_peg())
        return board_cp
    return False

#returns a list with all the available moves in a board                                                                               
def board_moves(board):
    moves=[]
    for i in range(board_lines(board)):
        for j in range(board_cols(board)):
            pos = make_pos(i,j)
            moves = moves + position_moves(pos,board)
    return moves                                                             

"""

Problem Classes:

sol_state: A state in the search tree/graph
It stores the board and other helpful information
(number of pieces, available moves, number of isolated pieces,
and sum of all pieces to the center of mass (of the pieces)).

"""

class sol_state:

    def __init__(self, board):
        self.board = board
        self.pieces= board_pieces(board)
        self.moves=board_moves(board)
        self.isolated=isolated(board)
        self.distance=distance(board)
    
    #Defines tie-breaker for the Heuristics in the Priority Qeue 
    def __lt__(self, other):
        return self.pieces>=other.pieces


    def __repr__(self):
        b = "\n"
        for line in range(board_lines(self.board)):
            b = b + str(get_board_line(self.board,line)) + "\n"
        return b

"""
   
Game problem class

"""
class solitaire(Problem):    

    def __init__(self, board):
        self.initial=sol_state(board)

    # Returns all the possible actions from the given state
    def actions(self, state):
        global expandidos
        global gerados
        expandidos += 1
        gerados += len(state.moves)
        return state.moves

    # Returns the new state with the action performed to previous state
    def result(self, state, action):
        board = board_perform_move(state.board, action)
        return sol_state(board)

    # Goal is having only 1 piece left
    def goal_test(self, state):
        return state.pieces==1

    #Heuristic
    def h(self,node):
        return node.state.distance+node.state.isolated-len(node.state.moves)


"""
Returns the number of pieces in a board. This should only be called in the initial board, then remove 1 piece for each move made. 

This is both the goal test, and can be an Heuristic (not used)
"""
def board_pieces(board):
    pieces_number=0
    for i in range(board_lines(board)):
        for j in range(board_cols(board)):
            if is_peg(pos_content(board,make_pos(i,j))):
                pieces_number = pieces_number + 1
    return pieces_number   
    
"""

Heuristics

"""

#Heuristic that favors moving pieces toward center of mass
def distance(board):     
    distance=0
    center=center_of_mass(board)
    for i in range(board_lines(board)):
        for j in range(board_cols(board)):
            if is_peg(pos_content(board,make_pos(i,j))):
                distance=distance+abs(i-center[0])+abs(j-center[1])
    return distance

#Auxiliary Function
#Coordinates where the most amount of pieces is located. 
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

#Heuristic that favours leaving less isolated pieces
def isolated(board):  
    pieces=0
    for i in range(board_lines(board)):
        for j in range(board_cols(board)):
            if is_alone(board,make_pos(i,j)):
                pieces+=1
    return pieces

#Auxiliary Function
#Alone if pos has a piece, but no piece in adjent positions
def is_alone(board,pos):
    if not is_peg(pos_content(board,pos)):
        return False
    
    #not in upper border
    if pos_l(pos)>0:
        if is_peg(pos_content(board,make_pos(pos_l(pos)-1,pos_c(pos)))):
            return False
    
    #not in left border
    if pos_c(pos)>0:
        if is_peg(pos_content(board,make_pos(pos_l(pos),pos_c(pos)-1))):
            return False
    
    #not in lower border
    if pos_l(pos)<board_lines(board)-1:
        if is_peg(pos_content(board,make_pos(pos_l(pos)+1,pos_c(pos)))):
            return False 
    
    #not in right border
    if pos_c(pos)<board_cols(board)-1:
        if is_peg(pos_content(board,make_pos(pos_l(pos),pos_c(pos)+1))):
            return False
    return True  

#Heuristic that favours having less pieces at the edge of the board. 
#NOT USED
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


"""

TO DELETE
TESTING FUNCTIONS

"""


def boards(n):    
    O = c_peg()
    X = c_blocked()
    _ = c_empty()

    b0 =   [[_,_,_],
            [O,O,_],
            [O,O,_]]

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


#Prints time, moves, and states from 'S' search in board 'board'
def solve(n,S):
    global gerados, expandidos
    
    # Restarting global vars modified in the previous solve execution
    gerados = 1
    expandidos = 0

    game = solitaire(boards(n))
    print(game.initial)
    
    Problem=InstrumentedProblem(game)
    
    i_time=time.time()
    
    if S=='DFS':
        #DFS SEARCH
        result_dfs = depth_first_tree_search(Problem)
        dfs_time = time.time() - i_time
        if result_dfs:
            print("DFS:\n", dfs_time, '\n', result_dfs.solution(),'\n', result_dfs.path(),'\n')
        print("gerados {}, expandidos {}".format(gerados, expandidos))
        return
    
    if S=='Greedy':
        #GREEDY SEARCH
        result_gan = greedy_best_first_graph_search(Problem,Problem.h)
        gan_time = time.time() - i_time        
        if result_gan:
            print("GREEDY:\n", gan_time, '\n', result_gan.solution(),'\n', result_gan.path(),'\n')
        print("gerados {}, expandidos {}".format(gerados, expandidos))
        return

    if S=='A*':
        #ASTAR SEARCH
        result_astar = astar_search(Problem)
        astar_time = time.time() - i_time
        if result_astar:
            print("A*:\n", astar_time, '\n', result_astar.solution(),'\n', result_astar.path(),'\n')
        print("gerados {}, expandidos {}".format(gerados, expandidos))
        return

    
solve(4,"Greedy")

solve(4,"A*")