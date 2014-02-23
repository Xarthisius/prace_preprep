import numpy as np
import matplotlib.pyplot as plt

ind = np.arange(7, dtype=np.float64)
width = 0.3
inp = [("data/nosfc", 'b', 'brute search'), ("data/sfc", 'r', 'SFC')]

plt.figure(dpi=300)
plt.loglog(2 ** np.arange(6, 13), 2 ** np.arange(7), color='k')
for fname, color, label in inp:
    data = np.loadtxt(fname)
    data1 = data[:, 1]  # * (data[:, 0] / 64)
    data2 = data[:, 2]  # * (data[:, 0] / 64)
    if fname == 'data/nosfc':
        pp = 0.75
    else:
        pp = 1.0
    #  data1 = 1.0 - np.array([2 ** -i for i in np.arange(7)]) \
    #        / (data[:, 1] / data[0, 1])
    #  data2 = 1.0 - np.array([2 ** -i for i in np.arange(7)]) \
    #        / (data[:, 2] / data[0, 2])
    plt.loglog(data[:, 0], pp * (data1[0] * 0 + data2[0]) /
               (data1 * 0 + data2), 'o-', basex=2, basey=2, label=label,
               color=color)
plt.xlim((2 ** 5, 2 ** 13))
plt.ylim((2 ** -1, 2 ** 7))
plt.xlabel('Number of cores')
plt.ylabel('Normalized speedup')
plt.yticks(2 ** np.array(range(8)), map(str, 2 ** np.array(range(7))))
plt.xticks(2 ** np.array(range(5, 14)), map(str, 2 ** np.array(range(5, 14))))
plt.legend()
plt.title('Strong scalability of sedov problem using AMR')
plt.savefig('fig2.png')

plt.clf()
plt.xticks(ind + width * 1.0, ('64', '128', '256', '512',
                               '1024', '2048', '4096'))
for fname, color, label in inp:
    data = np.loadtxt(fname)
    data1 = data[:, 1]  # * (data[:, 0] / 64)
    data2 = data[:, 2]  # * (data[:, 0] / 64)
    #  data1 = 1.0 - np.array([2 ** -i for i in np.arange(7)]) \
    #        / (data[:, 1] / data[0, 1])
    #  data2 = 1.0 - np.array([2 ** -i for i in np.arange(7)]) \
    #        / (data[:, 2] / data[0, 2])
    # p1 = plt.bar(ind, data1*3.0, width, color='r')
    # p2 = plt.bar(ind, data2, width, color='y', bottom=data1*3.0)
    p2 = plt.bar(ind, data2, width, color=color, label=label)
    ind += 0.3
plt.xlabel('Number of cores')
plt.ylabel('Walltime [s]')
plt.title('Effective walltime per step spent on grid operation in AMR')
plt.legend()
plt.savefig('fig3.png')
