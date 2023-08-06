import os

import cv2

folder = ''
imgs = []


def downsample(img):
    im = cv2.imread(os.path.join(folder, img), -1)
    if im.shape[1] > 1000:
        im = cv2.resize(im, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    cv2.imwrite(os.path.join(folder, img), im)


def main():
    for img in os.listdir(folder):
        print(img)
        downsample(img)


if __name__ == '__main__':
    main()
