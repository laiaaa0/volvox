import matplotlib.pyplot as plt
from arena import Arena
a = Arena()
num_iterations = 1000
for i in range (num_iterations):
    a.update()
    a.plot()
plt.show()