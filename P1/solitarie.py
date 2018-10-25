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

    def __lt__(self, other):
        return True

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
        self.initial = sol_state(board,board_pieces(board))
        self.dimensions = board_dim(board)

    # Returns all the possible actions from the given state
    def actions(self, state):
        return board_moves(state.board)

    # Returns the new state with the action performed to the board
    def result(self, state, action):
        board = board_perform_move(state.board, action)
        pieces = state.pieces-1
        return sol_state(board,pieces)

    # Stop condition for the search alg. when there is one piece left on the board
    def goal_test(self, state):
        return state.pieces==1

    def h(self,node):
        return node.state.pieces

    # Priority to moves that take pieces out of the corners
    def h0(self, node):
        
        if node.parent is None:
            return 0

        move = node.action

        # Initial position of the move
        l_initial = pos_l(move_initial(move))
        c_initial = pos_c(move_initial(move))

        # Dimensions of the board
        rows = self.dimensions[0] - 1
        cols = self.dimensions[1] - 1

        # Bounds of the board
        bounds = [(0,0), (0,cols), (rows,0), (rows,cols)]

        if (l_initial,c_initial) in bounds:
            return 0
        return 1

    # Priority to moves that don't place pieces to the borders of the board
    def h1(self, node):

        if node.parent is None:
            return 0

        move = node.action

        # Initial position of the move
        l_final = pos_l(move_final(move))
        c_final = pos_c(move_final(move))

        # Vertical and horizontal limits of the board
        l_borders = [0, self.dimensions[0]-1]
        c_borders = [0, self.dimensions[1]-1]
        #print("l_final,c_final",l_final,c_final)
        #print("l_borders, c_borders",l_borders, c_borders)
        if l_final in l_borders or c_final in c_borders:
            #print(1)
            return 1
        #print(0)
        return 0


    # Priority to moves that don't place pieces to the borders of the board
    # (higher h(n) for corners)
    def h2(self, node):

        if node.parent is None:
            return 0

        move = node.action

        # Initial position of the move
        l_final = pos_l(move_final(move))
        c_final = pos_c(move_final(move))

        # Vertical and horizontal limits of the board
        l_borders = [0, self.dimensions[0]-1]
        c_borders = [0, self.dimensions[1]-1]
        #print("l_final,c_final",l_final,c_final)
        #print("l_borders, c_borders",l_borders, c_borders)
        if l_final in l_borders and c_final in c_borders:
            return 2

        elif l_final in l_borders or c_final in c_borders:
            #print(1)
            return 1
        #print(0)
        return 0

def search_results(board,S):

    # Defining the initial state with the original board
    game = solitaire(board)
    print(game.initial)
    
    Problem=InstrumentedProblem(game)

    # Heuristic function to be used in Greedy and A*
    h = Problem.h2
    
    i_time=time.time()
    
    if S=='DFS':
        #DFS SEARCH
        result_dfs = depth_first_tree_search(Problem)
        dfs_time = time.time() - i_time
        print("DFS:\n", "Time", dfs_time)
        #if result_dfs is not None:
            #print(result_dfs.solution(),'\n', result_dfs.path(),'\n')
        #return
    
    if S=='Greedy':
        #GREEDY SEARCH
        result_gan = greedy_best_first_graph_search(Problem,h)
        gan_time = time.time() - i_time        
        print("GREEDY:\n", "Time", gan_time)
        #if result_gan is not None:
            #print(result_gan.solution(),'\n', result_gan.path(),'\n')
        #return

    if S=='A*':
        result_astar = astar_search(Problem, h)
        astar_time = time.time() - i_time
        print("A*:\n", "Time", astar_time)
        #if result_astar is not None:
            #print(result_astar.solution(),'\n', result_astar.path(),'\n')
        #return

def boards(n):    
    O = c_peg()
    X = c_blocked()
    _ = c_empty()

    b0 =   [[_,_,O],
            [O,_,O],
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
 
def solve(b,S):
    board=boards(b)
    search_results(board,S)
    print ('DONE')
    
    

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

solve(2, "DFS")
solve(2, "Greedy")
solve(2, "A*")


"""
- More weight to the moves that don-t put pieces on the corners and borders (
this might be the center empty, making hard to find a solution)
* Compute the actual borders of the board (including X spaces that modify the
actual board borders)
- Priority to moves in just one direction (to gather more pieces on that side)
- Priority to moves that start in a border and don't end in a border
"""