import os

import cv2
import numpy as np


def tonemapping(img):
    img = np.clip(img ** (1 / 2.2), 0, 1)
    return (img * 255).astype(np.uint8)


if __name__ == '__main__':
    folder = ''

    img = cv2.imread(os.path.join(folder, '00_reserved.exr'), -1)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_write = cv2.VideoWriter(os.path.join(folder, '2(24-35).mp4'), fourcc, 6, img.shape[1::-1])

    frame_num = 12

    # for _ in range(2):
    for i in range(frame_num * 2, 3 * frame_num):
        file_name = '{:02d}_reserved.exr'.format(i)
        img = cv2.imread(os.path.join(folder, file_name), -1)
        # convert exr to png
        img = tonemapping(img)
        video_write.write(img.astype(np.uint8))

        cv2.imwrite(os.path.join(folder, '{:02d}.png'.format(i)), img)

    # video_write.write(img.astype(np.uint8))
    # video_write.write(img.astype(np.uint8))
    #
    # for i in range(frame_num - 1, -1, -1):
    #     file_name = '{:02d}_reserved.exr'.format(i)
    #     img = cv2.imread(os.path.join(folder, file_name), -1)
    #     # convert exr to png
    #     img = tonemapping(img)
    #     video_write.write(img.astype(np.uint8))

    # video_write.write(img.astype(np.uint8))
    # video_write.write(img.astype(np.uint8))
    #
    # for i in range(24):
    #     file_name = '{:02d}_reserved.exr'.format(i)
    #     img = cv2.imread(os.path.join(folder, file_name), -1)
    #     # convert exr to png
    #     img = tonemapping(img)
    #     video_write.write(img.astype(np.uint8))
    #
    # video_write.write(img.astype(np.uint8))
    # video_write.write(img.astype(np.uint8))
    #
    # for i in range(23, -1, -1):
    #     file_name = '{:02d}_reserved.exr'.format(i)
    #     img = cv2.imread(os.path.join(folder, file_name), -1)
    #     # convert exr to png
    #     img = tonemapping(img)
    #     video_write.write(img.astype(np.uint8))
