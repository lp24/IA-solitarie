"""
____________________________________________________________________________
IA project 2

Group 43:
Luis Oliveira 83500
Samuel Arleo 94284
_______________________________________________________________________________
"""


# Modules

import itertools
import numpy as np
import copy

# BN classes

class Node():
    def __init__(self, prob, parents = []):
        self.prob = prob
        self.parents = parents
    
    def computeProb(self, evid):

        parents = self.parents.copy()
        t_prob = get_prob(evid, self.prob, parents)
        f_prob = 1 - t_prob

        return [f_prob, t_prob]
    
class BN():
    def __init__(self, gra, prob):
        self.gra = gra
        self.prob = prob

    """ 
    Obtains the joint prob. (one of the entries of the joint prob.
    table using equation 14.2 (check pages 513 and 514 of the book)
    """
    def computeJointProb(self, evid):
        p = 1
        for i in range(len(self.prob)):
            if evid[i] == 1:
                p *= self.prob[i].computeProb(evid)[1]
            else:
                p *= self.prob[i].computeProb(evid)[0]
        return p
        
    """
    Computes the posterior prob. of a query variable using the evidency in evid.

    It sums up all the joint probabilities that result from changing the value of 
    each hidden variable (the ones denoted by "[]" in the evidence)

    Check book's page 523.
    """
    def computePostProb(self, evid):

        # Index in evid of the query variable (the one whose prob. is being 
        # calculated X in P(X|e)) (the one with -1 in the tuple)
        query_var = 0

        for i in range(0,len(evid)):
            if evid[i] == -1:
                query_var = i

        evidences = vars_combinations(list(evid))

        pos_evidences = evidences
        neg_evidences = copy.deepcopy(evidences) # Just need to copy one of them
        for i in range(0,len(evidences)):
            pos_evidences[i][query_var] = 1
            neg_evidences[i][query_var] = 0
            
        # Computes the joint prob. of each evidence given a negative and pos
        # query variable and all the combinations of the hidden variables. Check page 523
        pos_prob = sum(map(lambda x: self.computeJointProb(x),pos_evidences))
        neg_prob = sum(map(lambda x: self.computeJointProb(x),neg_evidences))

        # Normalizing the prob.
        pos_prob = pos_prob/(pos_prob + neg_prob)
        return pos_prob


# Additional functions

"""
Obtains the evidence tuples from combining the possible values of the hidden
variables. For instance, given evidence (0,-1,[]), returns [[0,-1,1],(0,-1,0)]

* Args:
    - evid (list): original evidency, i.e: [0,[],-1,[],1]
"""

def vars_combinations(evid):
    evidences = []

    # Indexes of unknown vars (those with "[]")
    unknown_vars = [i for i in range(0,len(evid)) if evid[i]==[]]
    
    # Combinations of values from unknown vars when each one is T or F
    combinations = list(itertools.product([0,1], repeat=len(unknown_vars)))

    # New evidence tuples with the combinations of hidden vars
    for c in combinations:
        i = 0
        new_evid = evid.copy()
        for v in unknown_vars:
            new_evid[v] = c[i]
            i += 1
        evidences.append(new_evid)

    return evidences

"""
Goes into the multidimensional array (node's posterior probs.) recursively 
and returns the probability in the node's posterior prob. table that matches
the evidence.

The prob array is structured in such a way that using the order in which each
parent appears in the parents list and their values in the evidence, the
probability can be obtained.

For example, in a variable with three parents, to get the entry TFT (101) of the
posterior prob. table, just index the prob. array as following: prob[1][0][1]

* Args:
    - evid: tuple with the boolean values of the variables
    - prob: float when the posterior prob. was found. List
        when it's still going into the list of probs
    - parents: List of parent variables whose value in the posterior prob
        table of the node has not been found yet.
"""

def get_prob(evid, prob, parents):

    # Stop the recursion when the list of parents is empty
    if not parents: 
        return prob

    # Value of the current parent varible in the evidence (0 or 1)
    p_value = evid[parents[0]] 

    # Taking out the parent because we know the list in which its
    # evidence value is
    parents.pop(0)

    return get_prob(evid, prob[p_value], parents)


if __name__ == "__main__":
    gra = [[],[],[0,1],[2],[2]]
    ev = (1,1,1,1,1)

    p1 = Node( np.array([.001]), gra[0] )                   # burglary
    print( "p1 false %.4e p1 true %.4e" % (p1.computeProb(ev)[0] , p1.computeProb(ev)[1])) 

    p2 = Node( np.array([.002]), gra[1] )                   # earthquake

    p3 = Node( np.array([[.001,.29],[.94,.95]]), gra[2] )   # alarm
    print( "p1 = 1, p2 = 1, p3 false %.4e p3 true %.4e" % (p3.computeProb(ev)[0] , p3.computeProb(ev)[1])) 

    p4 = Node( np.array([.05,.9]), gra[3] )                 # johncalls

    p5 = Node( np.array([.01,.7]), gra[4] )                 # marycalls

    prob = [p1,p2,p3,p4,p5]

    gra = [[],[],[0,1],[2],[2]]
    bn = BN(gra, prob)

    jp = []
    for e1 in [0,1]:
        for e2 in [0,1]:
            for e3 in [0,1]:
                for e4 in [0,1]:
                    for e5 in [0,1]:
                        jp.append(bn.computeJointProb((e1, e2, e3, e4, e5)))

    print("sum joint %.3f (1)" % sum(jp))

    ev = (-1,[],[],1,1)
    print("ev : ")
    print(ev)
    print( "post : %.4g (0.2842)" % bn.computePostProb(ev)  )

    ev = ([],-1,[],1,1)
    print("ev : ")
    print(ev)
    print( "post : %.3f (0.176)" % bn.computePostProb(ev)  )

    ev = ([],0,1,-1,[])
    print("ev : ")
    print(ev)
    print( "post : %.3f (0.900)" % bn.computePostProb(ev)  )