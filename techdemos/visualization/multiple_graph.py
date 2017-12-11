import os
import glob
import sys
import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def graph_average_distances(main_folder, exp_file):
    directories = get_directories(main_folder)
    exp_obvs = get_exp_obvs(exp_file)
    best_perms = get_best_perms(directories)
    perm_obvs = get_perm_obvs(best_perms, exp_obvs)

    average_distances = get_differences(perm_obvs, exp_obvs)
    times = get_times(exp_file)

    obvs_arrays = []
    for obvs in average_distances:
       obvs_arrays.append(np.array(average_distances[obvs]))

    #time_array = np.array(times)
    generations = np.linspace(1, 50, 50)

    for i, obvs in enumerate(average_distances):
        make_graph(obvs, obvs_arrays[i], generations)

    return average_distances.keys()

def make_graph(name, obvs_diffs, generations):
    fig = plt.figure()
    plt.plot(generations, obvs_diffs)
    fig.suptitle("Average distances of {}".format(name))
    plt.xlabel("Generation")
    plt.ylabel("Average distance across all times")
    plt.savefig(os.path.join("media", "{}.png".format(name)), transparent=True)
    #plt.savefig("{}.png".format(name))
    plt.cla()


def get_directories(main_folder):
    return [os.path.abspath(os.path.join(main_folder, name))
            for name in os.listdir(main_folder)
            if os.path.isdir(os.path.join(main_folder, name))
            and name.isdigit()]


def get_best_perms(directories):
    FILE_NAME = "perm_model_diff.txt"
    out = {}
    for d in directories:
        with open(os.path.join(d, FILE_NAME), "rU") as f:
            f.readline()
            out[d] = f.readline().split()[0]
    return out


def get_exp_obvs(exp_file):
    out = {}
    with open(exp_file, "rU") as f:
        obvs = f.readline().split()[2:]
        for o in obvs:
            out[o] = []
        for line in f:
            fields = line.split()[1:]
            out[obvs[0]].append(float(fields[0]))
            out[obvs[1]].append(float(fields[1]))
    return out
            

def get_perm_obvs(perms, exp_obvs):
    out = {}
    for directory in perms:
        file = glob.glob(os.path.join(directory, "*{}.gdat".format(perms[directory])))[0]
        with open(file, "rU") as f:
            fields = f.readline().split()[1:]
            index_dict = {}
            for e in exp_obvs:
                index_dict[e] = fields.index(e)

            temp = {}
            for i in index_dict:
                temp[i] = []
            for line in f:
                fields = line.split()
                for i in index_dict:
                    temp[i].append(fields[index_dict[i]])
            out[int(os.path.basename(directory))] = temp
    return out
            

def get_differences(perm_obvs, exp_obvs):
    out = {} # Two keys: obv1 and obv2
             # Values are a list of 50 floats, each being the difference between the obv and perm at gen1, gen2, etc.
    
    for obv_name in exp_obvs:
        out[obv_name] = []
        for generation in sorted(perm_obvs.keys()):
            diff_total = 0
            for i, datum in enumerate(perm_obvs[generation][obv_name]):
                diff_total += abs(float(datum) - float(exp_obvs[obv_name][i]))
            diff = diff_total / len(exp_obvs[obv_name])
            #diff_percent = diff / exp_obvs[
            out[obv_name].append(diff)

    return out


def get_times(exp_file):
    out = []
    with open(exp_file, "rU") as f:
        f.readline()
        for line in f:
            out.append(float(line.split()[0]))
    return out



if __name__ == "__main__":
    graph_average_distances(sys.argv[1], sys.argv[2])
