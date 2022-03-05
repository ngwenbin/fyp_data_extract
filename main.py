'''
 # @ Author: Wen Bin
 # @ Create Time: 2022-02-04 11:01:38
 # @ Modified by: Wen Bin
 # @ Description:
 '''

import sys
import os
import getopt
import argparse
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

import numpy as np
import pandas as pd


options = "d:"
long_options = ["dir"]  # Long options
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
    return [os.path.join(fileDir, _) for _ in os.listdir(fileDir) if _.endswith(fileExt)]


def parse_files(fileDir):
    fig, ax = plt.subplots(figsize=(16, 9))
    total = 0
    count = 0
    nums = 0
    ax.set(xlabel='Unit block', ylabel='Volts')
    for i in get_files(fileDir):
        ptr = CSV_obj(i)
        ptr.df.plot.line(lw=0.5, ax=ax)
        max_value = ptr.df[ptr.fname].max()
        if not nums == 0 or not nums == 5:
            print(nums, max_value)
            total += max_value
            count += 1
        nums += 1
    avg = total / count
    print("Average max: {0}".format(avg))
    # plt.savefig("{}/export.png".format(fileDir), format="png", dpi=150)
    # plt.show()
    # plt.close()


def main(argv):
    try:
        opts, args = getopt.getopt(argv, options, long_options)

        for opt, arg in opts:
            if opt in ("-d", "--dir"):
                print("Input directory = " + arg)
                parse_files(arg)

        if len(argv) == 0:
            raise getopt.error("No arguments given")

    except getopt.error as err:
        print(str(err))
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
