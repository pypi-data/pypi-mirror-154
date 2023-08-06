import argparse
import numpy as np
import os

import cv2


def main():
    parser = argparse.ArgumentParser()

    # 场景所在目录
    parser.add_argument('--folder', default='')

    parser.add_argument('--remove', default=[], nargs='+')
    parser.add_argument('--reserve', default=[], nargs='+')
    parser.add_argument('--use_aa', action='store_true')

    parser.add_argument('--source', default='')
    parser.add_argument('--mask', default='')

    parser.add_argument('--downsample', '-d', action='store_true')

    parser.add_argument('--target', default='')
    parser.add_argument('--windows', action='store_true')
    parser.add_argument('--target_center', default=[], nargs='+')
    parser.add_argument('--target_width', type=int, default=-1)

    parser.add_argument('--mask_output', default='')
    parser.add_argument('--output', default='')

    args = parser.parse_args()
    print(args)

    use_remove = args.remove != []
    use_reserve = args.reserve != []

    target = cv2.imread(os.path.join(args.folder, args.target), -1)

    source = cv2.imread(os.path.join(args.folder, args.source), -1)
    if args.downsample:
        source = cv2.resize(source, (source.shape[1] // 2, source.shape[0] // 2), interpolation=cv2.INTER_AREA)
    cv2.imwrite(os.path.join(args.folder, args.source.split('.')[0] + '_half.exr'), source)

    mask = cv2.imread(os.path.join(args.folder, args.mask), -1)

    def get_alpha(mask, shape):
        alpha = np.ndarray((mask.shape[0], mask.shape[1]), dtype=np.float32)
        for i in range(mask.shape[0]):
            for j in range(mask.shape[1]):
                if args.use_aa:
                    alpha[i][j] = mask[i][j][2] + 1
                    if alpha[i][j] > 1:
                        alpha[i][j] -= int(alpha[i][j])
                        if alpha[i][j] == 0:
                            alpha[i][j] = 1
                else:
                    if use_remove:
                        if str(int(mask[i][j][2])) in args.remove:
                            alpha[i][j] = 0
                        else:
                            alpha[i][j] = 1
                    if use_reserve:
                        if str(int(mask[i][j][2])) in args.reserve:
                            alpha[i][j] = 1
                        else:
                            alpha[i][j] = 0
        # alpha = cv2.erode(alpha, np.ones((3, 3), np.float32), iterations=10)
        alpha = cv2.resize(alpha, (shape[1], shape[0]), interpolation=cv2.INTER_AREA)
        return alpha

    if not args.windows:
        alpha = get_alpha(mask, target.shape)
    else:
        alpha = get_alpha(mask, source.shape)
    cv2.imwrite(os.path.join(args.folder, args.mask_output), alpha)

    if args.windows:
        # scale = target.shape[1] / (args.target_width * 2)
        # target = cv2.resize(target, (source.shape[1]/, source.shape[0]), interpolation=cv2.INTER_AREA)
        center_0 = int(args.target_center[0])
        center_1 = int(args.target_center[1])
        radius = int(args.target_width)
        for i in range(center_1 - radius, center_1 + radius):
            for j in range(center_0 - radius, center_0 + radius):
                if i - (center_1 - radius) >= target.shape[0] or j - (center_0 - radius) >= target.shape[1]:
                    continue
                if i >= source.shape[0] or j >= source.shape[1]:
                    # print(i, j)
                    continue
                source[i][j] = source[i][j] * (1. - alpha[i][j]) + \
                               target[i - (center_1 - radius)][j - (center_0 - radius)] * alpha[i][j]
                # print(i - (center_1 - radius), j - (center_0 - radius))
    else:
        # print(target.shape)
        # print(source.shape)
        for i in range(target.shape[0]):
            for j in range(target.shape[1]):
                source[i][j] = source[i][j] * (1. - alpha[i][j]) + target[i][j][0:3] * alpha[i][j]

    cv2.imwrite(os.path.join(args.folder, args.output), source)


if __name__ == '__main__':
    main()
