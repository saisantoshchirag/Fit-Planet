import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
import seaborn as sns

# Data
arr = np.array([0, 1506, 0, 123, 2233, 2048, 2320, 232, 6756, 1566, 0, 0, 0, 0, 1004, 0, 12048, 0, 1004, 0])
df = pd.DataFrame({'y1':arr})
# multiple line plot
plt.plot('y1', data=df, marker='.', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4)
t = [datetime.now().day - i for i in range(len(arr))]
plt.xticks(t)
# plt.xticks(rotation=70)
# plt.legend()
plt.show()
# height = [3, 12, 5, 18, 45]
# bars = ('A', 'B', 'C', 'D', 'E')
# y_pos = np.arange(len(bars))
# plt.bar(y_pos, height, color=(0.2, 0.4, 0.6, 0.6))
# plt.show()
# # Custom Axis title
# plt.xlabel('title of the xlabel', fontweight='bold', color='orange', fontsize='17', horizontalalignment='center')
