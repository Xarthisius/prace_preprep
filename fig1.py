import numpy as np
import matplotlib.pyplot as plt

inp = [
    ("data/plain", 'g', r'$512^3\; \rm{uniform}$'),
    ("data/jeans_big", 'y', r'$1024^3\; \rm{uniform}$'),
    ("data/bsize32", 'r', r'$512^3\; \rm{B}_{\rm{size}}=32^3$'),
    ("data/bsize32_merged", 'b', r'$512^3\; \rm{B}_{\rm{size}}=32^3$ opt'),
]

plt.figure(dpi=300)
gold = np.array([34.202, 512.0, 34.202, 34.202])
plt.loglog(2 ** np.arange(5, 14), 2 ** np.arange(9), '--', color='k')
for i, (fname, color, label) in enumerate(inp):
    data = np.loadtxt(fname)
    plt.loglog(data[:, 0], gold[i] / data[:, 1], 'o-',
               basex=2, basey=2, label=label, color=color)
    if i < 2:
        plt.loglog(data[:, 0], data[:, 0] / 32 * data[:, -1]
                   / data[0, -1], '-', basex=2, basey=2, color='k')
plt.xlim((25, 9000))
plt.ylim((2 ** -1, 2 ** 8))
plt.xlabel('Number of cores')
plt.ylabel('Normalized speedup')
plt.yticks(2 ** np.array(range(9)), map(str, 2 ** np.array(range(9))))
plt.xticks(2 ** np.array(range(5, 14)), map(str, 2 ** np.array(range(5, 14))))
plt.legend(loc='lower right')
plt.title('Strong scalability of jeans problem')
plt.savefig('fig1.png')
