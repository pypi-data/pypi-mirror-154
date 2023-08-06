import argparse
import os.path

import cv2
import numpy as np


def file_to_exr(input_file, output_file, gamma=2.2, verbose=False):
    img = cv2.imread(input_file, -1)
    img = (img.astype(np.float32) / 255) ** gamma
    cv2.imwrite(output_file, img)
    if verbose:
        print(f'save {input_file} to {output_file}')


def to_exr(folder='.', input_names=None, input_types=None, output_formatter='{}', output_type='exr',
           recursion=False, verbose=False):
    if input_names is None and input_types is None:
        input_types = ['png', 'jpg']

    for file in os.listdir(folder):
        (filename, extension) = os.path.splitext(file)
        extension = extension[1:]
        file = os.path.join(folder, file)

        if os.path.isdir(file):
            if recursion:
                to_exr(file, input_names, input_types, output_formatter, output_type, recursion)
            else:
                continue

        output_file = f'{output_formatter.format(filename)}.{output_type}'
        if input_names is None:
            if extension in input_types:
                file_to_exr(file, output_file, verbose=verbose)
                continue

        if input_types is None:
            if filename in input_names:
                file_to_exr(file, output_file, verbose=verbose)
                continue

        if filename in input_names and extension in input_types:
            file_to_exr(file, output_file, verbose=verbose)


def to_exr_main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', '-f', type=str, default='.')
    parser.add_argument('--input_files', '-i', type=str, default=None)
    parser.add_argument('--input_types', type=str, default=None)
    parser.add_argument('--output_formatter', '-o', type=str, default='{}')
    parser.add_argument('--output_type', type=str, default='exr')
    parser.add_argument('--recursion', '-r', action='store_true')
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()

    to_exr(args.folder, args.input_files, args.input_types, args.output_formatter, args.output_type,
           args.recursion, args.verbose)
