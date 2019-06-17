import networkx as nx
from collections import defaultdict
import pickle

class Node:
    def __init__(self, id):
        self.id = id

# def add_node(g, node):
#     """
#     :param g: g is the multidirectedgraph
#     :param node: node is the node to add to the graph
#     :return:
#     """
#     g.add_node(node)
#
# def add_edge(g, start, dest, action):
#     """
#     :param g: g is the multidirectedgraph
#     :param start: start node
#     :param dest: destination node
#     :param action: action required to transfer from start to destination
#     :return:
#     """
#     g.add_edge(start, dest, action = action)

def transfer(g,start,action):
    """
    :param g: g is the multidirectedgraph
    :param start: start node
    :param action: the action take
    :return: the destination after the action, return NULL if this node can not take such action
    """
    for dst in g[start]:
        for label in g[start][dst]:
            action_temp = g[start][dst][label]["action"]
            if action_temp == action:
                return dst
    return None

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

def checkDist(node, r):
    if (abs(node[0][0]-node[1][0]) + abs(node[0][1] - node[1][1])) <=r:
        return False
    return True

def checkDistSet(set, r):
    for node in set:
        if checkDist(node,r) == False:
            return False
    return True

def getPre_safety(g,W,action1,action2, filename):
    W_temp = set()
    actDict = {}
    file = open(filename,"w")
    for node in W:
        #judge = -1
        for action_r in action1:
            tempset = set()
            for action_e in action2:
                dst = transfer(g, node, (action_r, action_e))
                if dst != None:
                    tempset.add(dst)
            if tempset.issubset(W) and len(tempset) != 0:
                #judge = 1
                if node not in actDict:
                    actDict[node] = set()
                actDict[node].add(action_r)
                #file.write("node is: " + node.id + "  the action can remain in set is: " + action_r + "\n")
                file.write("node is: " + str(node) + "  the action can remain in set is: " + str(action_r) + "\n")
                W_temp.add(node)
                #break
        # if (judge == 1):
        #     W_temp.add(node)
    file.close()
    return W_temp, actDict

# def getPre_reachability(g, W, action1, action2, filename):
#     W_temp = set()
#     actDict = {}
#     file = open(filename,"w")
#     for node in W:
#         #judge = -1
#         predecessor = g.predecessors(node)
#         while True:
#             try:
#                 pre = next(predecessor)
#                 for action_r in action1:
#                     tempset = set()
#                     for action_e in action2:
#                         dst = transfer(g, pre, (action_r,action_e))
#                         if dst!=None:                                    ##Add dist restriction 2019/1/31
#                              tempset.add(dst)
#                     if tempset.issubset(W) and len(tempset) != 0:
#                         #judge = 1
#                         if pre not in actDict:
#                             actDict[pre] = set()
#                         actDict[pre].add(action_r)
#                         #print(type(node))
#                         file.write("node is: " + str(node) + "    its pre node is: "+ str(pre) +"   the action can ensure reaching the set is: " + str(action_r) + "\n")          ###1.30test注释
#                         W_temp.add(pre)
#                         #break
#             except StopIteration:
#                 break
#     file.close()
#     nodeset = set()              ###1.30 modify
#     for node in W_temp:
#         #print(key)
#         nodeset.add(str(node))
#     return W_temp,nodeset
#     #return W_temp, actDict      #1.30 modify

def getPre_reachability(g, W, action1, action2, filename):
    W_temp = set()
    actDict = {}
    file = open(filename,"w")
    for node in W:
        #judge = -1
        predecessor = g.predecessors(node)
        while True:
            try:
                pre = next(predecessor)
                if checkDist(pre,1) == False:
                    continue
                for action_r in action1:
                    tempset = set()
                    for action_e in action2:
                        dst = transfer(g, pre, (action_r,action_e))
                        if dst!=None:                                    ##Add dist restriction 2019/1/31
                             tempset.add(dst)
                    if tempset.issubset(W) and len(tempset) != 0 and checkDistSet(tempset,1) == True:
                        #judge = 1
                        if pre not in actDict:
                            actDict[pre] = set()
                        actDict[pre].add(action_r)
                        #print(type(node))
                        file.write("node is: " + str(node) + "    its pre node is: "+ str(pre) +"   the action can ensure reaching the set is: " + str(action_r) + "\n")          ###1.30test注释
                        W_temp.add(pre)
                        #break
            except StopIteration:
                break
    file.close()
    nodeset = set()              ###1.30 modify
    for node in W_temp:
        #print(key)
        nodeset.add(str(node))
    print("W_temp size is", len(W_temp))
    filename = "./deterministic/W_temp.pkl"
    pickfile = open(filename, "wb")
    pickle.dump(W_temp, pickfile)
    pickfile.close()
    return W_temp,nodeset

def safetyGame_solver(g,W,action1,action2):
    """
    :param g:g is the multidirectedgraph
    :param W: set W
    :return: the final set that is safe
    """
    i = 0
    filename = "./deterministic/record_safety/step" + str(i) + ".txt"
    picklename = "./deterministic/record_safety/Dict.pkl"
    pickfile = open(picklename,"ab")
    W_temp, actDict = getPre_safety(g,W,action1,action2, filename)
    W_temp = W.intersection(W_temp)
    #pickle.dump(actDict, pickfile)           ##thinking about how to save this
    while(setCompare(W,W_temp)!= True):
        i += 1
        filename = "./deterministic/record_safety/step" + str(i) + ".txt"
        #picklename = "./deterministic/record_safety/Dict.pkl"
        W = W_temp
        W_temp, actDict = getPre_safety(g,W,action1,action2, filename)
        #pickle.dump(actDict, pickfile)
        W_temp = W.intersection(W_temp)
    pickfile.close()
    return W

def reachability_game_solver(g, W, action1, action2):
    """
    :param g: graph g
    :param W: initial set
    :return: the final set reachability set
    """
    i = 0
    filename = "./deterministic/record_reachability/step" + str(i) + ".txt"
    picklename = "./deterministic/record_reachability/Dict.pkl"
    pickfile = open(picklename, "ab")
    #W_temp, actDict = getPre_reachability(g, W, action1, action2, filename)
    W_temp, nodeset = getPre_reachability(g, W, action1, action2, filename)
    # for node in W:
    #     print(node)
    # print (len(W))
    W_formal = W
    W = W.union(W_temp)
    # print (len(W_temp))
    nodesetM = set()
    for node in W_temp:
        nodesetM.add(str(node))
    pickle.dump(nodesetM, pickfile)
    while (setCompare(W, W_formal) != True):
        i += 1
        filename = "./deterministic/record_reachability/step" + str(i) + ".txt"
        #picklename = "./deterministic/record_reachability/Dict" + str(i) + ".pkl"
        W_formal = W
        #W_temp, actDict = getPre_reachability(g, W, action1, action2, filename)
        W_temp, nodeset = getPre_reachability(g, W, action1, action2, filename)
        W = W.union(W_temp)
        nodesetM = set()
        for node in W_temp:
            nodesetM.add(str(node))
        pickle.dump(nodesetM, pickfile)
        # pickle.dump(nodeset, pickfile)
    pickfile.close()
    return W

def reachability_game_solver_outer_ASW(g, Y, X, action1, action2):
    outer_index = 0
    Y_temp = reachability_game_solver_inner_ASW(g, Y, X, action1, action2, outer_index)
    while setCompare(Y_temp, Y) != True:
        outer_index += 1
        Y = Y_temp
        Y_temp = reachability_game_solver_inner_ASW(g, Y, X, action1, action2, outer_index)
    return Y

def reachability_game_solver_inner_ASW(g, Y, X, action1, action2, outer_index):     ##inner start X = B
    inner_index = 0
    filename = "./deterministic/record_reachability_ASW/outer" + str(outer_index) + "inner" + str(inner_index) +".txt"
    setrecord = "./deterministic/record_reachability_ASW/Set_Outer" + str(outer_index) + "inner" + str(inner_index) + ".txt"
    picklename = "./deterministic/record_reachability_ASW/Dict_Outer" + str(outer_index) + ".pkl"
    pickfile = open(picklename, "ab")
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
    X_temp, actDict = getPre_ASW(g, Y, X, action1, action2, filename)
    pickle.dump(actDict, pickfile)
    while setCompare(X_temp,X) != True:
        inner_index += 1
        filename = "./deterministic/record_reachability_ASW/outer" + str(outer_index) + "inner" + str(inner_index) + ".txt"
        setrecord = "./deterministic/record_reachability_ASW/Set_Outer" + str(outer_index) + "inner" + str(inner_index) + ".txt"
        #picklename = "./deterministic/record_reachability_ASW/Dict_Outer" + str(outer_index) + "inner" + str(inner_index) + ".pkl"
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
        X_temp, actDict = getPre_ASW(g, Y, X, action1, action2, filename)
        pickle.dump(actDict, pickfile)
    pickfile.close()
    return X

def getPre_ASW(g, Y, X, action1, action2, filename):
    """
    :param g: graph g
    :param Y: set Y which the state will not leave
    :param X: set X which the state may enter
    :param action1: the action robot can take
    :param action2: the action environment can take
    :return:
    """
    X_temp = set()
    actDict = {}
    file = open(filename, "w")
    for node in Y:
        for action_r in action1:
            tempset = set()    ##store every possible following state if robot take action_r
            for action_e in action2:
                dst = transfer(g, node,(action_r, action_e))
                if dst != None:
                    tempset.add(dst)
            if tempset.issubset(Y) and len(tempset.intersection(X)) !=0:
                X_temp.add(node)
                if node not in actDict:
                    actDict[node] = set()
                actDict[node].add(action_r)
                file.write("node is: " + node.id + "  the action can remain in set Y and has probability to enter X is: " + action_r + "\n")
                break
    file.close()
    return X_temp, actDict

def ExchangeSet(inputSet):
    res = set()
    for node in inputSet:
        st1 = node[0]
        st2 = node[1]
        res.add((st2,st1))
    return res