import pickle
import os
from itertools import product
from deterministic_concurrent_game_v2 import *
filename1 = "D:\RBE Program\concurrent_omega_regular\stochastic\\Set_(9,5).pkl"
filename2 = "D:\RBE Program\concurrent_omega_regular\Set.pkl"
filename3 = "D:\RBE Program\MCTS_SSP\MCTS\\result(0,5,3,7)\KL_goal_adAction.pkl"
filename4 = "almostSureWinningPolicy95.pkl"
Set1 = set()
Set2 = set()
# with open(filename, "rb") as f:
#     fileSize = os.fstat(f.fileno()).st_size
#     while f.tell()<fileSize:
#         DictList.append(pickle.load(f))

with open(filename1, "rb") as f1:
    Set1 = pickle.load(f1)

with open(filename2, "rb") as f2:
    Set2 = pickle.load(f2)

with open(filename3, "rb") as f3:
    traj = pickle.load(f3)

with open(filename4, "rb") as f4:
    almostSureWinningRegion = pickle.load(f4)


# print(len(almostSureWinningRegion))
# for state in almostSureWinningRegion:
#     st0 = state[0]
#     st1 = state[1]
#     dis1 = abs(st0[0] - 9) + abs(st0[1] - 5)
#     dis2 = abs(st1[0] - 9) + abs(st1[1] - 5)
#     if dis1 >= dis2:
#         input("111")
#     print(state, "  ", almostSureWinningRegion[state])


# print(len(DictList[11]))
# i = 0
# for key in DictList[11]:
#     #print(key[13])
#     if ((int(key[2]) ==9 and int(key[5]) == 5)):
#         i += 1
#         print(key)
# print(i)
# print (len(ResSet))
# for node in ResSet:
#     print(node)
# for node in Set1:
#     if node in Set2:
#         print("False")
# print("End")
print(len(Set1))