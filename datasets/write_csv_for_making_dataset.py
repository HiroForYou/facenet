#!/usr/bin/env python
# coding: utf-8

# In[10]:

import argparse
import csv
import glob
import os
import time

import multitasking
import pandas as pd
from .format_multitasking_data import main as format_data


def reset_csv():
    with open('multitasking.csv', 'w') as f:
        f.write('id,name,ext\n')


reset_csv()
state = 0


def write_csv(file, newrow):
    with open(file, mode='a') as f:
        f_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        f_writer.writerow(newrow)


@multitasking.task
def generate_set(data, process_name, filename):
    time0 = time.time()
    df = pd.DataFrame()
    print("The number of files: ", len(data))
    for idx, file in enumerate(data):
        if idx % 100 == 0:
            print("[{}/{}]".format(idx, len(data) - 1))
        '''    
        try:
            img = Image.open(file) # open the image file
            img.verify() # verify that it is, in fact, an image
        except (IOError, SyntaxError) as e:
            if verbosity == 1:
                print('Bad file:', file) # print out the names of corrupt files
            pass
        else:
            face_id    = os.path.basename(file).split('.')[0]
            face_label = os.path.basename(os.path.dirname(file))
            df = df.append({'id': face_id, 'name': face_label}, ignore_index = True)
        '''
        extension = file.split('.')[-1]
        face_id = os.path.basename(file).split('.')[0]
        face_label = os.path.basename(os.path.dirname(file))
        write_csv('multitasking.csv', [face_id, face_label, extension])
    print("Process", process_name, 'finished!')
    check_and_format(filename)


def check_and_format(filename):
    global state
    state += 1
    if state == 4:
        format_data(filename)


if __name__ == '__main__':
    verbosity = 1

    parser = argparse.ArgumentParser(description='Face Recognition using Triplet Loss')

    parser.add_argument('--root-dir', type=str, help='path to dataset root dir')
    parser.add_argument('--final-file', type=str, help='Final file name')

    args = parser.parse_args()

    root_dir = args.root_dir
    filename = args.final_file

    files = glob.glob(root_dir + "/*/*")

    div = len(files) // 4
    chunk1 = files[0:div]
    chunk2 = files[div:div + div]
    chunk3 = files[div + div:div + div + div]
    chunk4 = files[div + div + div:]

    generate_set(chunk1, 'chunk1', filename)
    generate_set(chunk2, 'chunk2', filename)
    generate_set(chunk3, 'chunk3', filename)
    generate_set(chunk4, 'chunk4', filename)
