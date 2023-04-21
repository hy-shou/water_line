import numpy as np
import traj_dist.distance as tdist
import pickle
import matplotlib.pyplot as plt

traj_list = pickle.load(open("./data/benchmark_trajectories.pkl", "rb"),encoding='iso-8859-1')[:10]
traj_A = traj_list[0]
traj_B = traj_list[1]



# Simple distance
ax = traj_A[:,0]
ay = traj_A[:,1]
print(ay)
ay[4] = 36
plt.plot(ax, ay)

bx = traj_B[:,0]
by = traj_B[:,1]
plt.plot(bx, by)
plt.show()


# https://github.com/bguillouet/traj-dist

dist = tdist.sspd(traj_A, traj_B)
print(dist)

# dist_sowd = tdist.sowd_grid(traj_list, traj_list,type_d="spherical")
# print(dist_sowd)

# Pairwise distance

# pdist = tdist.pdist(traj_list, metric="sspd")
# print(pdist)

# Distance between two list of trajectories

# cdist = tdist.cdist(traj_list, traj_list, metric="sspd")
# print(cdist)
#
# sowd_grid