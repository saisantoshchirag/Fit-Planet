import os
import pandas as pd
path = r'C:\sem-5\SOAD\project\activity\media\videos\data'
files = []
dirs = []
i=0
for root,dir,_ in os.walk(path):
    for d in dir:
        cur_path = os.path.join(root,d)
        for r, k, f in os.walk(cur_path):
            for file in f:
                if '.mp4' in file:
                    files.append(os.path.join(cur_path,file))
                i+=1
                dirs.append([d,d])
# for i in files:
#     print(i)
# print(len(files))
#print(dirs)
file = pd.read_csv('FINAL.csv')