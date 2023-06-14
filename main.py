import os, sys
import time

import numpy as np
import matplotlib.pyplot as plt

from BM import *

_filepath = os.path.abspath(__file__)
_dirname = os.path.dirname(_filepath)

def main():
    argvec = sys.argv
    if len(argvec) != 2:
        print("Wrong command; $python main.py [input_file_name]")
        exit()
    filename = argvec[1]

    try:
        input_file = open(os.path.join(_dirname, "input/%s.txt"%filename))
    except FileNotFoundError as e:
        print(e)
        exit()

    n, k, seed, w, H_t, s = extract_parameter(input_file)
    input_file.close()

    #e = np.array([random.randint(0, 1) for _ in range(0, n)])
    e, _ = standard_isd(H_t, n, k, s, w)
    print("error vector : \n%s"%("".join(str(elem) for elem in e)))

    ### Verify e
    H = H_t.T
    recalculated_syndrome = binary_mat_vec_mult(H, e)
    print("recalculated syndrome vector : \n%s"%recalculated_syndrome)
    result = (s==recalculated_syndrome)
    print(result)

def time_plot_experiment():
    size_list = [n for n in range(10, 51, 10)]
    time_avg_list = []
    time_std_list = []

    N = 10

    for size in size_list:
        print("Size %d start"%size)
        filename = "input_%d"%size

        try:
            input_file = open(os.path.join(_dirname, "input/%s.txt"%filename))
        except FileNotFoundError as e:
            print("File not exits %s"%filename)
            size_list.remove(size)
            continue

        n, k, seed, w, H_t, s = extract_parameter(input_file)
        input_file.close()

        ### todo - Run algorithm to get vector e with dimension n X 1
        #e = np.array([random.randint(0, 1) for _ in range(0, n)])
        data_list = []
        for iter in range(0, N):
            print("Start %d-th iter in size %d"%(iter, size))
            time1 = time.time()
            e = standard_isd(H_t, n, k, s, w)
            time2 = time.time()
            print("Complete %d-th iter in size %d"%(iter, size))

            ### Verify e
            H = H_t.T
            recalculated_syndrome = binary_mat_vec_mult(H, e)
            for i in range(0, len(s)):
                assert(s[i]==recalculated_syndrome[i])

            data_list.append(time2-time1)

        time_avg_list.append(np.average(data_list))
        time_std_list.append(np.std(data_list))
        print("Size %d done!"%size)

    plt.clf()
    plt.errorbar(size_list, time_avg_list, yerr=time_std_list, color="black", marker=".")
    plt.savefig(fname="./time.png")

def gaussian_elim_time_experiment():
    SIZE = 100
    N = 1000

    try:
        input_file = open(os.path.join(_dirname, "input/input_%d.txt"%SIZE))
    except FileNotFoundError as e:
        print(e)
        exit()

    n, k, seed, w, H_t, s = extract_parameter(input_file)
    input_file.close()

    total_time_list = []
    gaussian_elim_avg_list = []
    gaussian_elim_std_list = []
    gaussian_elim_number_list = []
    for i in range(0, N):
        e, gaussian_elim_time_list, total_time = standard_isd(H_t, n, k, s, w)
        total_time_list.append(total_time)
        gaussian_elim_avg_list.append(np.average(gaussian_elim_time_list))
        gaussian_elim_std_list.append(np.std(gaussian_elim_time_list))
        gaussian_elim_number_list.append(len(gaussian_elim_time_list))
    
    plt.hist([i for i in range(0, max())])

def extract_parameter(input_file) -> tuple:
    parameter_list = ["n", "seed", "w", "H^transpose", "s^transpose"]

    parameter_index = 0
    line = input_file.readline().rstrip('\n')
    while line:
        assert(line.startswith('#'))
        parameter = line.split(' ')[1]
        assert(parameter_list[parameter_index]==parameter)
        parameter_index += 1

        if parameter=="n":
            n = int(input_file.readline().rstrip('\n'))
        elif parameter=="seed":
            seed = int(input_file.readline().rstrip('\n'))
        elif parameter=="w":
            w = int(input_file.readline().rstrip('\n'))
        elif parameter=="H^transpose":
            H_t, k = extract_H_transpose(n, input_file)
            H_t = np.concatenate((np.identity(n-k, dtype=int), H_t))
        elif parameter=="s^transpose":
            row = []
            for elem in list(input_file.readline().rstrip('\n')):
                row.append(int(elem))
            s = np.array(row)
        else:
            raise Exception()

        line = input_file.readline().rstrip('\n')

    return (n, k, seed, w, H_t, s)

def extract_H_transpose(n: int, input_file) -> tuple:
    H_t = []

    ### Read first column of H, and calculate k
    line = input_file.readline().rstrip('\n')
    k = n - len(line)
    row = []
    for elem in list(line):
        row.append(int(elem))
    H_t.append(row)

    ### Read remaining (k-1) columns of H
    for _ in range(0, k-1):
        row = []
        line = input_file.readline().rstrip('\n')
        for elem in list(line):
            row.append(int(elem))
        H_t.append(row)

    return (np.array(H_t), k)

if __name__ == "__main__":
    #time_plot_experiment()
    main()