"""
__filename__ = 'diff_plotter.py'
__author__ = 'Konstantinos Zoumpatianos <zoumpatianos@disi.unitn.it>'
__description__ = 'Provides graphical comparison (using plots) between same columns in numeric CSV files.'
__usage__ = 'python diff_plotter.py output.svg [csv filenames]'
__example__ = 'Example: python diff_plotter.py comparison.svg table1.csv table2.csv table3.csv'
"""
import random
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pylab
import math

FONTSIZE = 9
PLOTSIZE = (18.5,10.5)
HSPACE = 0.7
WSPACE = 0.5


class DiffPlotter(object):
    """DiffPlotter class contains all the file loading and plotting functionlity"""
   
    labels = []
    data = []
    rows = []
    subplots = None
    colors = []
    
    def __init__(self, filenames, fontsize=FONTSIZE, plotsize=PLOTSIZE, hspace=HSPACE, 
                 wspace=WSPACE):
        """Initializes the plotter and loads files in memory"""
        random.seed(100)
        matplotlib.rcParams.update({'font.size': FONTSIZE})
    
        for fname in filenames:
            loaded_labels = False
            file_data = []
            for line in open(fname,'r').readlines():
                if not loaded_labels:
                    self.labels += [map(str, line.split(","))]
                    loaded_labels = True
                    continue
                file_data += [map(float, line.split(","))]
            self.data += [file_data]
        s = int(math.ceil(math.sqrt(len(self.labels[0]))))
        self.subplots = map(lambda x:(s,s,x), range(1,(s*s)+1))
        self.colors = map(lambda x: ("#%s" % "".join([hex(random.randrange(0, 255))[2:] for i in range(3)])), [""]*len(self.labels[0]))
        
    def plot(self):      
        """Plots the data previously loaded from source CSV files."""
        self.rows = []
        for data_1 in self.data:
            rows_1 = []
            for i in range(0, len(data_1[0])):
                tmp_row = [0]
                for j in range(0,len(data_1)):
                    tmp_row += [data_1[j][i]]
                rows_1 += [tmp_row]
            self.rows += [rows_1]
        plt.figure(1)
        plt.subplots_adjust(hspace=HSPACE, wspace=WSPACE)
        
        for row_id in range(0, len(self.rows[0])):
            splot = plt.subplot(*self.subplots[row_id])
            cid = 0
            for rows_1 in self.rows:
                p1, = plt.plot(np.arange(0, len(rows_1[row_id]), 1), rows_1[row_id], color=self.colors[cid], label="", ls='-')
                cid += 1
            splot.set_title(self.labels[0][row_id].replace("_", " "), fontsize=10)
        fig = plt.gcf()
        fig.set_size_inches(*PLOTSIZE)
	
    def save(self, ofilename):
        """Saves plot in file."""
        plt.savefig(ofilename)
    
        

if __name__ == "__main__":
    diff_plotter = DiffPlotter(sys.argv[2:])
    diff_plotter.plot()
    diff_plotter.save(sys.argv[1])
