"""Using PIL to manipulate bitmap file."""
from scipy import misc
import numpy as np
N = 200
img = misc.imread('Lekagul Roadways.bmp')
img_un = np.unique(img)
print(img_un)
