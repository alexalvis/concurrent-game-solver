import networkx as nx
from deterministic_concurrent_game_v2 import *
from itertools import product

#define state
s0 = Node("s0")
s1 = Node("s1")
s2 = Node("s2")
s3 = Node("s3")
s4 = Node("s4")
states = {s0,s1,s2,s3,s4}

#define action
action1 = {"a","b","c"}
action2 = {"d","e","f"}

#define graph
grf = nx.MultiDiGraph()

#add node
for node in states:
    grf.add_node(node)

#add transfer state
grf.add_edge(s1,s0,action = ("a","d"))
grf.add_edge(s1,s0,action = ("b","e"))
grf.add_edge(s1,s0,action = ("c","e"))
grf.add_edge(s1,s2,action = ("a","f"))
grf.add_edge(s1,s2,action = ("b","f"))
grf.add_edge(s1,s2,action = ("c","d"))
grf.add_edge(s1,s3,action = ("a","e"))
grf.add_edge(s1,s4,action = ("b","d"))
grf.add_edge(s1,s4,action = ("c","f"))
for action in product(action1,action2):
    grf.add_edge(s4, s4,action = action)
    grf.add_edge(s2, s1, action=action)
    grf.add_edge(s3, s1, action=action)
    grf.add_edge(s0, s0, action=action)

W = {s0,s1,s2}

result1 = safetyGame_solver(grf,W,action1,action2)
result2 = reachabilityGame_solver(grf,W,action1,action2)
for node in result2:
    print(node.id)

