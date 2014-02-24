import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('data/jeans.dat')
x = 2 ** np.array(range(13))

plt.semilogx(x, data, 'o-', linewidth=2, basex=2)
plt.axvline(x=32.5, lw=2, color='g')
plt.xticks(x, map(str, x))
plt.yticks(np.arange(6))
plt.ylabel("Mean simulation step walltime [s]")
plt.xlabel("Number of CPUs")
plt.text(1.5, 4.0, 'Single node')
plt.text(128, 1.25, 'Many nodes')
plt.title("Weak scaling for Jeans problem using uniform grid")
plt.savefig('fig4.png')
