import argparse
import math
import os

import cv2
import numpy as np


def interpolate_depth(depth: np.ndarray):
    h, w, c = depth.shape
    assert (c == 3)
    result = np.zeros_like(depth)
    flag = False
    for ci in range(w):
        col = depth[:, ci, :]
        has_window = np.any(np.isinf(col))
        if not has_window:
            result[:, ci, :] = col
            continue
        start_row = -1
        end_row = -1
        active = False
        for ri in range(h):
            if not active:
                if not np.isinf(col[ri, 2]):
                    start_row = ri
                    continue
                else:
                    active = True
            else:
                if np.isinf(col[ri, 2]):
                    continue
                else:
                    end_row = ri
                    if start_row == -1:
                        col[:end_row, 2] = col[end_row, 2]
                    else:
                        col[start_row:end_row + 1, 2] = np.linspace(col[start_row, 2], col[end_row, 2],
                                                                    end_row - start_row + 1)
                    start_row = ri
                    end_row = -1
                    active = False
        if active:
            if start_row == -1:
                flag = True
            else:
                col[start_row:, 2] = col[start_row, 2]
        result[:, ci, :] = col
    return result


def get_view_position(depth, fov):
    width, height = depth.shape[1], depth.shape[0]
    v_pos = np.zeros((height, width, 3), dtype=np.float32)

    x = np.array(range(width))
    y = np.array(range(height))

    x = 2 * x / width - 1
    y = 2 * y / height - 1

    fov_x = math.radians(fov)
    fov_y = 2 * math.atan(math.tan(fov_x / 2) * height / width)

    v_pos[..., 2] = depth[..., 2] * x * math.tan(fov_x / 2)
    v_pos[..., 1] = -(depth[..., 2].T * y).T * math.tan(fov_y / 2)
    v_pos[..., 0] = -depth[..., 2]

    return v_pos


def load_exr(filename, g_buffer, fov, handle_inf=False):
    dic = {}
    for g in g_buffer:
        if os.path.exists(filename + '_' + g + '.exr'):
            dic[g] = cv2.imread(filename + '_' + g + '.exr', -1)
        elif g == 'direction':
            if os.path.exists(filename + '_view_normal.exr'):
                dic[g] = cv2.imread(filename + '_view_normal.exr', -1)
            else:
                dic[g] = cv2.imread(filename + '_normal.exr', -1)
        else:
            print('no file: ' + filename + '_' + g + '.exr')

    if len(dic['depth'].shape) == 2:
        dic['depth'] = np.stack([np.zeros_like(dic['depth']), np.zeros_like(dic['depth']), dic['depth']], axis=2)
    if handle_inf:
        dic['depth'] = interpolate_depth(dic['depth'])
        cv2.imwrite(filename + '_depth.exr', dic['depth'])
    dic['v_pos'] = get_view_position(dic['depth'], fov)
    return dic


def main():
    parser = argparse.ArgumentParser()

    # 场景所在目录
    parser.add_argument('--folder', default='')

    # 需要 blend 的 G-Buffer
    parser.add_argument('--gbuffer', default=['depth', 'direction', 'mat_info', 'albedo'], nargs='+')
    parser.add_argument('--fov', type=float, default=120)

    # 场景名
    parser.add_argument('--scene', default='cornell-box-rr-0')
    # 插入物体名
    parser.add_argument('--insert', default='insert-0')
    # 输出场景名
    parser.add_argument('--output', default='output')

    args = parser.parse_args()

    scene = load_exr(os.path.join(args.folder, args.scene), args.gbuffer, args.fov, True)
    cv2.imwrite(os.path.join(args.folder, args.scene + '_vpos.exr'), scene['v_pos'])

    insert = load_exr(os.path.join(args.folder, args.insert), args.gbuffer, args.fov)
    cv2.imwrite(os.path.join(args.folder, args.insert + '_vpos.exr'), insert['v_pos'])

    for i in range(scene['depth'].shape[0]):
        for j in range(scene['depth'].shape[1]):
            if insert['depth'][i][j][2] < scene['depth'][i][j][2]:
                for g in args.gbuffer:
                    scene[g][i][j] = insert[g][i][j]
                scene['v_pos'][i][j] = insert['v_pos'][i][j]

    for g in args.gbuffer:
        if g == 'direction':
            nan_i, nan_j = np.nonzero(np.isnan(scene[g][:, :, 2]))
            for i, j in zip(nan_i, nan_j):
                top = scene[g][i - 1, j]
                left = scene[g][i, j - 1]
                right = scene[g][i, j + 1]
                bottom = scene[g][i + 1, j]
                scene[g][i, j] = (top + left + right + bottom) / 4
                if np.isnan(scene[g][i, j][2]):
                    scene[g][i, j] = (top + bottom) / 4
                if np.isnan(scene[g][i, j][2]):
                    scene[g][i, j] = (left + right) / 4
                scene[g][i, j] /= np.linalg.norm(scene[g][i, j])
            cv2.imwrite(os.path.join(args.folder, args.output + '_view_normal.exr'), scene[g])
        else:
            cv2.imwrite(os.path.join(args.folder, args.output + '_' + g + '.exr'), scene[g])

    scene['v_pos'] /= abs(scene['v_pos'][..., 0].min())
    cv2.imwrite(os.path.join(args.folder, args.output + '_vpos.exr'), scene['v_pos'])

    os.system(f'cd {args.folder} && cp {args.scene}_gpu.exr {args.output}.exr')
    os.system(f'cd {args.folder} && cp {args.scene}_gpu.exr {args.scene}.exr')
    os.system(f'cd {args.folder} && cp {args.scene}.exr {args.scene}_output.exr')

    im = cv2.imread(os.path.join(args.folder, args.scene + '_output.exr'), -1)
    im = np.clip(im ** (1 / 2.2), 0, 1)
    im = (im * 255).astype(np.uint8)
    cv2.imwrite(os.path.join(args.folder, args.scene + '_output.png'), im)


if __name__ == '__main__':
    main()
