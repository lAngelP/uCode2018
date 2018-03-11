#../DataAnalyser/output/*.json

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
import os
import json
import matplotlib

fileArray = None
for root, dirs, files in os.walk("../DataAnalyser/output/"):
    fileArray = list(filter(lambda file: file.endswith(".json"), files))

labels = []
meanSent = []

for file in fileArray:
    object = json.load(open("../DataAnalyser/output/" + file, "r", encoding="UTF-8"))['data']
    X1 = [[obj['user']['followers'], obj['sentient']] for obj in object]

    X = [np.log10(x) for [x, y] in X1]
    y = [y for [x, y] in X1]
    meanSent = meanSent + [np.mean(y)]
    labels = labels + [file]

    matplotlib.rcParams['axes.unicode_minus'] = False
    fig, ax = plt.subplots()
    ax.plot(X, y, 'rx')
    ax.set_title('Followers of ' + file + " by sentient data.")
    plt.xlabel("Seguidors (en escala logarítmica)")
    plt.ylabel("Resultado análisis semántico")
    plt.show()

# Fixing random state for reproducibility
np.random.seed(19680801)



fig, ax = plt.subplots()

# Fixing random state for reproducibility
np.random.seed(19680801)


# histogram our data with numpy
n, bins = np.histogram(meanSent, 50)

# get the corners of the rectangles for the histogram
left = np.array(bins[:-1])
right = np.array(bins[1:])
bottom = np.zeros(len(left))
top = bottom + n


# we need a (numrects x numsides x 2) numpy array for the path helper
# function to build a compound path
XY = np.array([[left, left, right, right], [bottom, top, top, bottom]]).T

# get the Path object
barpath = path.Path.make_compound_path_from_polys(XY)

# make a patch out of it
patch = patches.PathPatch(barpath)
ax.add_patch(patch)

# update the view limits
ax.set_xlim(left[0], right[-1])
ax.set_ylim(bottom.min(), top.max())

plt.show()