import sys

import cv2
import numpy as np

imName = sys.argv[1]
im = cv2.imread(imName)
gamma = 2.4
im = (im.astype(np.float32) / 255) ** gamma
cv2.imwrite(imName.replace('png', 'exr'), im)
