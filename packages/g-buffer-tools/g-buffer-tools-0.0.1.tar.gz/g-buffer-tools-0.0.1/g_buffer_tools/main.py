import os
import cv2


def clip(path, x, y, h, w, right_top):
    img = cv2.imread('./in/' + path + '.png', -1)
    # print(img.shape)
    # print(img.dtype)

    patch = img[y - h // 2:y + h // 2, x - w // 2:x + w // 2]

    w_2, h_2 = 90, 90
    patch = cv2.resize(patch, (w_2, h_2))
    # cv2.imwrite(save_path + '.png', patch)
    # print(patch.shape)
    # print(patch.dtype)

    pt1 = (x - w // 2, y - h // 2)
    pt2 = (x + w // 2, y + h // 2)
    cv2.rectangle(img, pt1, pt2, (0, 0, 255), 2)

    if right_top:
        img[0:h_2, 256 - w_2:256] = patch
        pt1 = (255 - 1, 1)
        pt2 = (255 - w_2, h_2)
        cv2.rectangle(img, pt1, pt2, (0, 0, 255), 2)
    else:
        img[0:h_2, 0:w_2] = patch
        pt1 = (1, 1)
        pt2 = (w_2, h_2)
        cv2.rectangle(img, pt1, pt2, (0, 0, 255), 2)

    print('./out/' + path + '.png')
    cv2.imwrite('./out/' + path + '.png', img)


paths = []
mid = []


def main():
    for i in range(6):
        for root, ds, fs in os.walk('./in/' + paths[i]):
            print(root)
            for f in fs:
                print(f)
                filename = f.split('.')[0]
                x, y = mid[i]
                clip(paths[i] + '/' + filename, x, y, 32, 32, i != 0)


if __name__ == '__main__':
    main()
