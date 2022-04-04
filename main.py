"""
 # @ Author: Wen Bin
 # @ Create Time: 2022-02-04 11:01:38
 # @ Modified by: Wen Bin
 # @ Description:
 """

import sys
import os
import getopt
import matplotlib.pyplot as plt
import plotly.express as px

import numpy as np
import pandas as pd

options = "d:x:b:"
long_options = ["dir", "exclude", "block"]  # Long options
fileExt = r".CSV"

xlabel = "Unit block"
ylabel = "Volts"


class CSV_obj:
    fname = None
    df = None

    def __init__(self, fpath):
        self.fpath = fpath
        self.__getfilename()

    def __getfilename(self):
        filename_wext = os.path.basename(self.fpath)
        self.fname = filename_wext.split(".")[0]
        self.__createdataframe()

    def __createdataframe(self):
        self.df = pd.read_csv(self.fpath, usecols=[1], skiprows=15)
        self.df.rename(columns={self.df.columns[0]: self.fname}, inplace=True)


def get_files(fileDir):
    return [
        os.path.join(fileDir, _) for _ in os.listdir(fileDir) if _.endswith(fileExt)
    ]


def parse_files(fileDir, exclude, block_size):
    fig, ax = plt.subplots(figsize=(10, 7))
    total = 0
    count = 0
    ax.set(xlabel="Unit block", ylabel="Volts")
    for i, item in enumerate(get_files(fileDir)):
        ptr = CSV_obj(item)  # Create data object
        max_value = ptr.df[ptr.fname].max()  # Gets value of peak
        exlflag = "x "
        if str(i + 1) not in exclude:
            if block_size:
                ptr.df["rolling"] = (
                    ptr.df[ptr.fname].rolling(block_size, center=True).mean()
                )
                ptr.df["rolling"].plot.line(lw=0.5, ax=ax)  # Add line plot
                max_value = ptr.df["rolling"].max()
            else:
                ptr.df[ptr.fname].plot.line(lw=0.5, ax=ax)  # Add line plot
            total += max_value
            count += 1
            exlflag = ""

        print("{0}Sample: {1},  peak = {2}".format(exlflag, ptr.fname, max_value))

    avg = total / count
    print(
        "\nAverage max: {0} / {1} = {2} \nExcluded: {3}".format(
            total, count, avg, exclude
        )
    )
    # plt.savefig("{}/export.png".format(fileDir), format="png", dpi=150)
    plt.show()
    plt.close()


def main(argv):
    data_dir = ""
    exclude = []
    block = 0
    try:
        opts, args = getopt.getopt(argv, options, long_options)
        for opt, arg in opts:
            if opt in ("-d", "--dir"):
                data_dir = arg
                print("Input directory: {0}".format(arg))

            elif opt in ("-x", "--exclude"):
                exclude = arg.split(",")
                print("Excluding samples: {0}\n".format(exclude))

            elif opt in ("-b", "--block"):
                block = int(arg)
                print("Block : {0}".format(arg))

        if len(argv) == 0:
            raise getopt.error("No arguments given")
        elif data_dir:
            parse_files(data_dir, exclude, block)

    except getopt.error as err:
        print(str(err))
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
