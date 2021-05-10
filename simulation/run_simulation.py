import matplotlib.pyplot as plt
from simulation.arena import Arena, Pattern
a = Arena(pattern=Pattern.DYNAMIC)
num_iterations = 100
for i in range(num_iterations):
    a.update()
    a.plot()
plt.show()
