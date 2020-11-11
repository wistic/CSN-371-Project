import json
import os
import matplotlib.pyplot as plt
import itertools
import numpy as np


def plotgraphs(output_folder_path, mode):
    if output_folder_path[-1] != '/':
        output_folder_path = output_folder_path + '/'

    words_count_file = output_folder_path + mode + '-words-count.json'
    tags_count_file = output_folder_path + mode + '-tags-count.json'

    with open(tags_count_file, 'r') as f:
        tags_dictionary = json.load(f)

    # Plotting Tags vs Frequency Bar Graph
    plt.title('Tags vs Frequency')
    plt.ylabel('Frequency')
    plt.xlabel('Tags')
    plt.bar(range(0, len(tags_dictionary)*2, 2), list(tags_dictionary.values()),
            align='center', width=1)
    plt.xticks(range(0, len(tags_dictionary)*2, 2),
               list(tags_dictionary.keys()), rotation=90, fontsize=8)
    fig_size = plt.gcf().get_size_inches()
    plt.gcf().set_size_inches(fig_size[0]*2, fig_size[1]*1, forward=True)
    plt.tight_layout(pad=0.5)
    ax = plt.gca()
    ax.set_xlim(left=-2)
    plt.savefig(output_folder_path + mode + '-tags-bar-graph.png')
    plt.close()

    # Plotting Tags Pie Chart
    plt.title('Top 10 tags')
    labels = list(itertools.islice(tags_dictionary.keys(), 10))
    labels.append('Other')
    sizes = list(itertools.islice(tags_dictionary.values(), 10))
    total = sum(tags_dictionary.values())
    other_size = total-sum(itertools.islice(tags_dictionary.values(), 10))
    sizes.append(other_size)

    cmap = plt.get_cmap("tab20c")
    colors = cmap(np.arange(11))
    plt.pie(sizes,  labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)

    plt.axis('equal')
    plt.savefig(output_folder_path + mode + '-tags-pie-chart.png')
    plt.close()

    with open(words_count_file, 'r') as f:
        words_dictionary = json.load(f)

    # Plotting Words pie chart
    plt.title('Top 10 words')
    labels = list(itertools.islice(words_dictionary.keys(), 10))
    labels.append('Other')
    sizes = list(itertools.islice(words_dictionary.values(), 10))
    total = sum(words_dictionary.values())
    other_size = total-sum(itertools.islice(words_dictionary.values(), 10))
    sizes.append(other_size)
    explode = (0, 0, 0, 0.1, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0)
    cmap = plt.get_cmap("tab20c")
    colors = cmap(np.arange(11)*2)
    plt.pie(sizes,  labels=labels, colors=colors, explode=explode,
            autopct='%1.1f%%', shadow=True, startangle=140)

    plt.axis('equal')
    plt.savefig(output_folder_path + mode + '-words-pie-chart.png')
    plt.close()
