import networkx as nx
from collections import defaultdict

"""
we should first have a action set, which contains 5 states, which is stay, notrh, south, east, west

"""
NORTH = lambda st: (st[0], st[1] - 1)
SOUTH = lambda st: (st[0], st[1] + 1)
EAST = lambda st: (st[0] + 1, st[1])
WEST = lambda st: (st[0] - 1, st[1])
STAY = lambda st: (st[0],st[1])
FOUR_CONNECTED= [NORTH,SOUTH,EAST,WEST,STAY]


def safetyGame_solver(g, W):
    """
    :param g:  graph g   (prefer using DiGraph because some of the functions can not be used in MultiDiGraph)
    :param W:  Winning set W, prefer use the initial winning set
    :return:
    """
    ##Predecessor_temp = set()
    W_temp = getPre_v2(g,W)
    W_temp = W.intersection(W_temp)
    while(setCompare(W,W_temp) != True):
        # print("W_temp:", W_temp)
        W = W_temp
        W_temp = getPre_v2(g,W)
        W_temp = W.intersection(W_temp)
    return W

def reachabilityGame_solver(g, W):
    """

    :param g: graph g
    :param W: initial set
    :return: the final set reachability set

    """
    W_temp = getPre_v2(g, W)
    W_temp = W.union(W_temp)
    while (setCompare(W, W_temp) != True):
        W = W_temp
        W_temp= getPre_v2(g, W)
        W_temp = W.union(W_temp)
    return W

def setCompare(W,W_temp):
    """
    :param W: the first set
    :param W_temp:  the second set
    :return: True means the two sets are the same, false means the two sets are different
    """
    if(len(W) != len(W_temp)):
        return False
    for item in W:
        if item not in W_temp:
            return False
    return True

def transit(node, action_r):
    """
    :param node: the start node in the form of (node_r, node_e)
    :param action_r: the action that the robot take
    :return: a set of nodes that can reach from the starting node and the robot taking the action_r
    """
    node_r = node[0]
    node_e = node[1]
    node_r = action_r(node_r)
    result_set = set()
    for action_e in action:
        node_e_temp = node_e
        node_e_temp = action_e(node_e_temp)
        if 0 <= node_e_temp[0] < 2 and 0 <= node_e_temp[1] < 2:
            result_set.add((node_r,node_e_temp))
    return result_set


def getPre_v2(g,W):
    W_temp = set()
    for node in W:
        node_r = node[0]
        node_e = node[1]
        #print("node:", node)
        judge = -1
        for action_r in FOUR_CONNECTED:
            node_r_temp = node_r
            node_r_temp = action_r(node_r_temp)
            if 0 <= node_r_temp[0] < 2 and 0 <= node_r_temp[1] < 2:
                if (transit(node, action_r).issubset(W)):
                    #print("transit_set", transit(node, action_r))
                    judge = 1
                    break
        if (judge == 1):
            W_temp.add(node)
    #W_temp = W.intersect(W_temp)
    return W_temp