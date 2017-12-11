import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os



def make_checkboxes(names):
    out = []
    for name in names:
        out.append(r'''<label for="{}_box">{}</label> <input type="checkbox" id="{}_box" checked onclick="toggleVisibility('{}');" />'''.format(name, name, name, name))
    return out

def make_images(names, location):
    out = []
    for name in names:
        #src = os.path.join(location, name)
        #out.append('<img id="{}" src="{}.png" class="graph">'.format(name, src))
        out.append(name)
    return out


def make_content_dict(names, location):
    checkboxes = make_checkboxes(names)
    images = make_images(names, location)
    content = {"checkboxes": checkboxes,
               "images": images}
    return content

def single_graph(infile):
    times, observables, names = gdat_to_np(infile)
    upper = np.amax(observables)
    for i, obv in enumerate(observables):
        plot_observable(times, obv, names[i], upper)

    return names


def gdat_to_np(gdat):
    
    with open(gdat, "rU") as infile:
        names = infile.readline().split()[2:]
        num_obs = len(names) + 1

        data = [[] for i in range(num_obs)]
        
        for line in infile:
            fields = line.split()

            for i in range(num_obs):
                data[i].append(float(fields[i]))


    times = np.array(data[0])
    observables = []
    for i in range(1, len(data)):
        observables.append(np.array(data[i]))

    return times, observables, names

def plot_observable(times, obv, name, upper):
    fig = plt.figure()
    plt.ylim([0, upper])
    plt.plot(times, obv)
    fig.suptitle("Best fit observables graph")
    plt.xlabel("Time")
    plt.ylabel("Amount of molecules")
    plt.savefig(os.path.join("media", "{}.png".format(name)), transparent=True)
    plt.cla()




if __name__ == "__main__":
    import sys
    single_graph(sys.argv[1])
