import os
import numpy as np
import time
import json
import datetime
import itertools
import pandas as pd
import argparse

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_speed_vs_date(points, fname):
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.plot(points[:,0], points[:,1], "ro",label="times")
    ax.legend(loc="upper left",numpoints=1)
    ax.grid(True)
    ax.set_title("speed vs date")
    ax.set_xlabel("date")
    ax.set_ylabel("speed [s]")
    add_last_updated(ax)
    fig.autofmt_xdate()
    fig.savefig(fname)
    # os.system("ic {}".format(fname))

def add_last_updated(ax):
    ax.text(0.01, 0.00,str(datetime.datetime.now()),
            horizontalalignment='left',
            verticalalignment='bottom',
            transform = ax.transAxes)

def plot_speed_vs_solvenum(points, fname):
    fig, ax = plt.subplots(nrows=1, ncols=1)
    xs = np.arange(len(points[:,1]))
    ax.plot(xs, points[:,1], "bo",label="times")

    rmean = pd.rolling_mean(points[:,1],window=50)
    rstd = pd.rolling_std(points[:,1],window=50)

    ax.plot(xs, rmean, 'k', color='#1B2ACC')
    ax.fill_between(xs, rmean-1.*rstd, rmean+1.*rstd,
            alpha=0.4, edgecolor='#1B2ACC', facecolor='#089FFF',
            linewidth=1, linestyle='-', antialiased=True, label="SMA(50) $\\pm 1\\sigma$")

    ax.legend(loc="upper left",numpoints=1)
    ax.grid(True)
    ax.set_title("speed vs solve number (total of {} solves)".format(len(xs)))
    ax.set_xlabel("solve number")
    ax.set_ylabel("speed [s]")
    add_last_updated(ax)
    fig.savefig(fname)


def group_by_day(points):
    groups = itertools.groupby(points, lambda x: x[0].replace(hour=0, minute=0, second=0))
    new_points = []
    for cat,group in groups:
        vals = np.array(list(group))[:,1]
        median, std = np.median(vals), vals.std()
        new_points.append([cat, median, std])
    return np.array(new_points)

def plot_speed_vs_day(points, fname):

    points = group_by_day(points)
    days = points[:,0]
    means = points[:,1]
    stds = np.array(points[:,2],dtype=float)

    fig, ax = plt.subplots(nrows=1, ncols=1)
    xs = np.arange(len(points[:,1]))

    # Linear fit
    offsets = np.array([1.0*(d-days[0]).days for d in days])
    coef, cov = np.polyfit(offsets, means, 1, w=1./stds, cov=True)
    errs = np.diag(cov)**2
    fit_label = "linear fit: [${:.1f}\\pm{:.1f} + ({:.1f}\\pm{:.1f})$*days] sec".format(coef[1], errs[1], coef[0], errs[0])
    fit_y = coef[0]*offsets + coef[1]
    ax.plot(days, fit_y, 'k', color='r', linewidth=2., label=fit_label)

    ax.plot(days, means, 'k', color='#1B2ACC')
    ax.errorbar(days, means, yerr=stds, fmt='ko', color='#1B2ACC', label="daily $\\mu \\pm 1\\sigma$")

    ax.legend(loc="upper left",numpoints=1)
    ax.grid(True)
    ax.set_title("speed vs day")
    ax.set_xlabel("day")
    ax.set_ylabel("speed [s]")
    fig.autofmt_xdate()
    ax.margins(0.05,0.05)
    add_last_updated(ax)
    fig.savefig(fname)


def get_points(fname):
    d_data = {}
    with open(fname,"r") as fhin:
        for line in fhin:
            entry = json.loads(line)
            sid = entry["id"]
            t = float(entry["time"])/1000.
            dt = datetime.datetime.strptime(entry["created_at"].split(".",1)[0].replace("Z",""), "%Y-%m-%dT%H:%M:%S")
            if sid not in d_data:
                d_data[sid] = [dt,t]
    points = np.array(sorted(d_data.values()))
    return points

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input log file", default="log.txt")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        raise Exception("{} doesn't exist!".format(args.input))

    points = get_points(args.input)

    os.mkdir("plots")
    plot_speed_vs_date(points, "plots/speed_vs_date.png")
    plot_speed_vs_solvenum(points, "plots/speed_vs_solvenum.png")
    plot_speed_vs_day(points, "plots/speed_vs_day.png")

