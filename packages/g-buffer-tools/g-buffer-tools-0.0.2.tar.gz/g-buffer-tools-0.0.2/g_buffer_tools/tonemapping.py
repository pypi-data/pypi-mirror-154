import cv2


def tone_mapping(img, gamma=1.0):
    # print(img)
    im = cv2.imread(img, -1)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    im[:, :, 2] = im[:, :, 2] * 2 ** 0.8
    im = cv2.cvtColor(im, cv2.COLOR_HSV2BGR)
    cv2.imwrite(img.replace(".exr", "_new.exr"), im)
