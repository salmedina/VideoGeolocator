""" Script to combine .mat batch files extracted by netvlad, along with the corresponding file names """
import sys
import os
import glob
import argparse
import numpy as np
from scipy.io import loadmat, savemat

BATCH_KEY = 'batchFeats'
OUTPUT_MAT_NAME = 'feature.mat'
OUTPUT_FILE_NAME = 'files.txt'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Combine mat batch files.')
    parser.add_argument('root', help="Directory path where batch output are saved.")
    parser.add_argument('filename', help="String or wildcard for output folders.")
    parser.add_argument('output', help="Output directory.")
    args = parser.parse_args()

    out_dir = args.output
    if not os.path.exists(out_dir):
        print "Output directory does not exist!"
        exit()

    # load and merge matrix
    merged = None
    image_list = []
    path = os.path.join(args.root, args.filename)
    output_dirs = glob.glob(path)
    for d in output_dirs:
        files = os.listdir(d)
        for f in files:
            if f.endswith('.mat'):
                # matrix file
                mat_path = os.path.join(d, f)
                matrix = loadmat(mat_path)[BATCH_KEY]
                # image name file
                txt_path = os.path.join(d, '.'.join([f.split('.')[0], 'txt']))
                batch_image_list = open(txt_path).readlines()
                image_list += batch_image_list

                if merged is None:
                    merged = matrix
                else:
                    merged = np.concatenate((merged, matrix), axis=1)
                if len(image_list) % 100 == 0:
                    print "\r#Images Merged: {0}".format(len(image_list)),

    # output merged matrix
    mat_out_path = os.path.join(out_dir, OUTPUT_MAT_NAME)
    savemat(mat_out_path, dict(feat_mat=merged))
    # output merged image list
    txt_out_path = os.path.join(out_dir, OUTPUT_FILE_NAME)
    with open(txt_out_path, 'w') as fout:
        fout.write("".join(image_list))

