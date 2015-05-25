import networkx as nx
import matplotlib.pyplot as plt
import math
import os

import numpy as np


def make_degree_distribution(graph, full_path="dist.png", weight=None, log="linear", marker="ro"):
    degree_list = graph.degree(weight=weight).values()
    degree_len = float(len(degree_list))
    degrees = dict((i, degree_list.count(i) / degree_len) for i in set(degree_list))
    # print degrees
    # x, y = remove_zeros(degrees.keys(), degrees.values())
    # x, y = xrange(len(degrees.keys())), sorted(degrees.values())
    x, y = degrees.keys(), degrees.values()
    plt.title("Probability graph")

    plt.yscale(log)
    plt.xscale(log)

    plt.plot(x, y, marker)

    plt.xlabel("Degree of nodes")
    plt.ylabel("Probability P(k)")

    plt.savefig(full_path)
    plt.close('all')


def make_xy_plot(x, y, full_path="xy.png", log="linear", marker="ro", labels=[None, None]):
    plt.yscale(log)
    plt.xscale(log)

    # plt.xlabel(labels[0])
    # plt.ylabel(labels[1])
    plt.figure(figsize=(20, 5))
    plt.bar(x, y, color="#D15FEE")
    full_path = "/home/clutcher/projects/vgr/xy.png"
    plt.savefig(full_path)
    plt.close('all')


def make_ranked_plot(y, full_path="xy.png", log="linear", marker="ro"):
    plt.yscale(log)
    plt.xscale(log)

    plt.plot(xrange(len(y)), sorted(y, reverse=True), marker)

    plt.savefig(full_path)
    plt.close('all')


def add_xy_plot(x, y, log="linear", marker="o", color="r", labels=None):
    if labels is not None:
        plt.xlabel(labels[0])
        plt.ylabel(labels[1])
    plt.yscale(log)
    plt.xscale(log)

    plt.plot(x, y, marker=marker, color=color)


def save_plots(full_path):
    plt.savefig(full_path)
    plt.close('all')


def get_color_by_db(db_dir):
    if db_dir == "afdb":
        color = "#d6aa2e"  # orange
    elif db_dir == "chf2db":
        color = "#b1171a"  # red
    elif db_dir == "chfdb":
        color = "#b1171a"  # red
    elif db_dir == "ltafdb":
        color = "#b11786"  # violet
    elif db_dir == "mitdb":
        color = "#172db1"  # blue
    elif db_dir == "nsr2db":
        color = "#008515"  # green
    else:
        color = "#676767"  # gray

    return color


def remove_zeros(xi, yi):
    """Deleting pairs (x, 0)"""
    xi_temp = []
    yi_temp = []
    iterator = 0
    for y in yi:
        if y:
            yi_temp.append(y)
            xi_temp.append(xi[iterator])
            iterator += 1
        else:
            iterator += 1

    return xi_temp, yi_temp
