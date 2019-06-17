import networkx as nx
from collections import defaultdict
import pickle

"""
we should first have a action set, which contains 5 states, which is notrh, south, east, west

"""
# NORTH = lambda st: (st[0], st[1] - 1)
# SOUTH = lambda st: (st[0], st[1] + 1)
# EAST = lambda st: (st[0] + 1, st[1])
# WEST = lambda st: (st[0] - 1, st[1])
# STAY = lambda st: (st[0],st[1])
# action= [NORTH,SOUTH,EAST,WEST,STAY]

policy = {}
successor = {}

class Node:
    def __init__(self, id):
        self.id = id

def checkDistSet(set, r):
    for node in set:
        if checkDist(node,r) == False:
            return False
    return True

def checkDist(node, r):
    if (abs(node[0][0]-node[1][0]) + abs(node[0][1] - node[1][1])) <= r:
        return False
    return True

def transfer(g, start, action):
    tempset = set()
    for dst in g[start]:
        for label in g[start][dst]:
            action_temp = g[start][dst][label]["action"]
            if action == action_temp:
                tempset.add(dst)
    return tempset

def safety_game_solver(g, W, robotConn, envConn):
    """
    :param g: graph g
    :param W: the safety region
    :return: final region
    """
    i = 0
    filename = "./stochstic/record_safety/step" + str(i) + ".txt"
    picklename = "./stochastic/record_safety/Dict" + str(i) + ".pkl"
    W_temp = getPre_safety(g, W, robotConn, envConn, filename)
    W_temp = W.intersection(W_temp)
    while (setCompare(W, W_temp) != True):
        i += 1
        filename = "./stochastic/record_safety/step" + str(i) + ".txt"
        picklename = "./stochastic/record_safety/Dict" + str(i) + ".pkl"
        W = W_temp
        W_temp = getPre_safety(g, W, robotConn, envConn, filename)
        W_temp = W.intersection(W_temp)
    return W

def reachability_game_solver(g, W, robotConn, envConn):
    """
    :param g: graph g
    :param W: the reachability region
    :return: final region
    """
    i = 0
    filename = "./stochastic/record_reachability/step" + str(i) + ".txt"
    picklename = "./stochastic/record_reachability/Dict" + str(i) + ".pkl"
    W_formal = W
    W_temp = getPre_reachability(g, W, robotConn, envConn, filename)
    W = W.union(W_temp)
    while (setCompare(W,W_formal) != True):
        i += 1
        filename = "./stochastic/record_reachability/step" + str(i) + ".txt"
        picklename = "./stochastic/record_reachability/Dict" + str(i) + ".pkl"
        W_formal = W
        W_temp = getPre_reachability(g, W, robotConn, envConn, filename)
        W = W.union(W_temp)
    policyfilename = "almostSureWinningPolicy.pkl"
    pickfile = open(policyfilename, "wb")
    pickle.dump(policy, pickfile)
    pickfile.close()
    return W

def reachability_game_solver_outer_ASW(g, Y, X, robotConn, envConn):
    outer_index = 0
    Y_temp = reachability_game_solver_inner_ASW(g, Y, X, robotConn, envConn, outer_index)
    while setCompare(Y_temp, Y) != True:
        outer_index += 1
        Y = Y_temp
        Y_temp = reachability_game_solver_inner_ASW(g, Y, X, robotConn, envConn, outer_index)
    return Y

def reachability_game_solver_inner_ASW(g, Y, X, robotConn, envConn, outer_index):     ##inner start X = B
    inner_index = 0
    filename = "./stoachastic/record_reachability_ASW/outer" + str(outer_index) + "Inner" + str(inner_index) +".txt"
    setrecord = "./stochastic/record_reachability_ASW/Set_Outer" + str(outer_index) + "Inner" + str(inner_index) + ".txt"
    picklename = "./stochastic/record_reachability_ASW/Dict_Outer" + str(outer_index) + "Inner" + str(inner_index) + ".pkl"
    setrecorder = open(setrecord, "w")
    setrecorder.write("The node in Y is: \n")
    for node in Y:
        setrecorder.write(node.id + "       ")
    setrecorder.write("\n\n")
    setrecorder.write("The node in X is: \n")
    for node in X:
        setrecorder.write(node.id + "       ")
    setrecorder.write("\n End")
    setrecorder.close()
    X_temp = getPre_reachability_ASW(g, Y, X, robotConn, envConn, filename)
    while setCompare(X_temp,X) != True:
        inner_index += 1
        filename = "./stochastic/record_reachability_ASW/outer" + str(outer_index) + "Inner" + str(inner_index) + ".txt"
        setrecord = "./stochastic/record_reachability_ASW/Set_Outer" + str(outer_index) + "Inner" + str(inner_index) + ".txt"
        picklename = "./stochastic/record_reachability_ASW/Dict_Outer" + str(outer_index) + "Inner" + str(inner_index) + ".pkl"
        X = X_temp
        setrecorder = open(setrecord, "w")
        setrecorder.write("The node in Y is: \n")
        for node in Y:
            setrecorder.write(node.id + "       ")
        setrecorder.write("\n\n")
        setrecorder.write("The node in X is: \n")
        for node in X:
            setrecorder.write(node.id + "       ")
        setrecorder.write("\n End")
        setrecorder.close()
        X_temp = getPre_reachability_ASW(g, Y, X, robotConn, envConn, filename)
    return X

def setCompare(W,W_temp):
    """
    :param W: the first set
    :param W_temp:  the second set
    :return: true means the two sets are the same, false means the two sets are different
    """
    if(len(W) != len(W_temp)):
        return False
    for item in W:
        if item not in W_temp:
            return False
    return True

def getPre_safety(g, W, robotConn, envConn, filename):
    """
    :param g: graph g
    :param W: the safety region
    :param robotConn: robot connecting
    :param envConn environment connecting
    :return: the predecessor of W
    """
    # graphDict = GetDict(g, W)
    W_temp = set()
    file = open(filename, "w")
    for node in W:
        nodeDict = GetDict_node(g,node)
        for action_e in envConn:
            flag = check_in_W_safety(W, action_e, robotConn, nodeDict, node)
            if flag == True:
                file.write("node is: " + str(node) + "  the action can remain in set is: " + str(action_r) + "\n")
                W_temp.add(node)
                break
    file.close()
    return W_temp

def getPre_reachability(g, W, robotConn, envConn, filename):
    """
    :param g: graph g
    :param W: the reachability region
    :param robotConn: robot connecting
    :param envConn:  environment connecting
    :param filename: the file store the node and action
    :return: the predecessors of W
    """
    W_temp = set()
    file = open(filename, "w")
    for node in W:
        predecessor = g.predecessors(node)
        while True:
            try:
                pre = next(predecessor)
                if checkDist(pre,1) == False:
                    continue
                # nodeDict = GetDict_node(g, pre)
                for action_r in robotConn:
                    tempset = set()
                    for action_e in envConn:
                        dst = transfer(g, pre, (action_r,action_e))
                        if dst != None:
                            tempset = tempset.union(dst)
                    if tempset.issubset(W) and len(tempset) != 0 and checkDistSet(tempset, 1) == True:
                        file.write("node is: " + str(pre) + "  the action can ensure reaching the set in one step is: " + action_r.__name__ + "\n")
                        if pre not in policy:
                            policy[pre] = action_r.__name__
                        W_temp.add(pre)
                        break
                    # flag = check_in_W(W, action_r, envConn, nodeDict, pre, node)
                    # if flag == True:
                    #     file.write("node is: " + str(pre) + "  the action can ensure reaching the set in one step is: " + str(action_r) + "\n")
                    #     W_temp.add(pre)
                    #     break
            except StopIteration:
                break;
    file.close()
    print ("W_temp size is", len(W_temp))
    return W_temp

def getPre_reachability_ASW(g, Y, X, robotConn, envConn, filename):
    """
    :param g: thr graph g
    :param Y: the Supp(s) should remain in Y with probability 1
    :param X: the Supp(s) should have possibility to enter X
    :param robotConn: the robot connecting
    :param envConn: the environment connecting
    :return: the Almost-sure win pre
    """
    graphDict = GetDict(g, Y)
    W_temp = set()
    file = open(filename, "w")
    for node in Y:
        for action_r in robotConn:
            flag_Y = check_in_W(Y, action_r, envConn, graphDict, node)
            flag_X = check_intersection_X(X, action_r,envConn, graphDict, node)
            if flag_X == True and flag_Y == True:
                file.write("node is: " + str(node) + "  the action can ensure remaining in Set Y and has probability reaching set X in one step is: " + action_r + "\n")
                W_temp.add(node)
                ##break
    file.close()
    return W_temp

def check_intersection_X(X, action_r, envConn, graphDict, node):      ##check if this node use action_r has probability to transform into X
    flag = -1
    for action_e in envConn:
        for key, value in graphDict[node][(action_r,action_e)].items():
            if key in  X:
                flag = 1
                break
        if flag == 1:
            return True
    return False

def check_in_W_safety (W, action_e, robotConn, nodeDict, node): ## check if this node use action_r can ensure it will not leave W
    """
    :param W: Winning region
    :param action_r: action taken by robot
    :param envConn: environement connection
    :param graphDict: the graph dict
    :param node: the node that at this state
    :return: if this action_r for all action_e, T(s'|s,(a_r,a_e)) >0 , s' ∈W , then return true, else return false
    """
    for action_r in robotConn:
        for key, value in nodeDict[node][(action_r, action_e)].items():
            if value > 1e-5 and key not in W :
            # if key not in W:
            #     print(action_e, "pre is", pre, "key is ", key,value)
                return False
    return True

def check_in_W (W, action_r, envConn, nodeDict, pre): ## check if this node use action_r can ensure it will not leave W
    """
    :param W: Winning region
    :param action_r: action taken by robot
    :param envConn: environement connection
    :param graphDict: the graph dict
    :param node: the node that at this state
    :return: if this action_r for all action_e, T(s'|s,(a_r,a_e)) >0 , s' ∈W , then return true, else return false
    """
    for action_e in envConn:
        for key, value in nodeDict[pre][(action_r, action_e)].items():
            if value > 0.0 and key not in W :
            # if key not in W:
            #     print(action_e, "pre is", pre, "key is ", key,value)
                return False
    return True

def GetDict(g, W):
    """
    :param g: the graph g
    :param W: the winning region W
    :return:  a dict that {key: state, value: dict{key: action, value: {dict{key: pro, value: destination}}}}
    """
    graphDict = {}
    for start_state in W:
        if start_state not in graphDict:
            graphDict[start_state] = {}
        for dst in g[start_state]:
            #graphDict[start_state][dst] = {}
            for label in g[start_state][dst]:
                action = g[start_state][dst][label]['action']
                pro = g[start_state][dst][label]['pro']
                if action not in graphDict[start_state]:
                    graphDict[start_state][action] = {}
                graphDict[start_state][action][dst] = pro
    return graphDict

def GetDict_node(g, node):
    nodeDict = {}
    nodeDict[node] = {}
    for dst in g[node]:
        for label in g[node][dst]:
            action = g[node][dst][label]['action']
            pro = g[node][dst][label]['pro']
            if action not in g[node]:
                nodeDict[node][action] = {}
            nodeDict[node][action][dst] = pro
    return nodeDict



