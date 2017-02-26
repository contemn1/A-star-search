import numpy as np

with open("maze.txt","r") as f:
    content = f.readlines()
    alist = np.zeros((101,101))
    alist = [line.strip().split() for line in content ]
    alist = np.asarray([map(int, i) for i in alist])
"""count = 0
for i in alist:
    for j in i:
        if j==0:
            count = count +1
print count """