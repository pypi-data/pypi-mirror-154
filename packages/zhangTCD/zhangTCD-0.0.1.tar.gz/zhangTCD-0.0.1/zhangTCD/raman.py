from .xydata import xydata
from .reference import reference

import matplotlib.pyplot as plt

from datetime import date

class raman(xydata, reference):
    datatype = '.txt'
    imgformat = '.bmp'
    def __init__(self, rawdatafile, material):
        xydata.__init__(self, rawdatafile+raman.datatype, quantity = ['Raman Shift', 'cm$^{-1}$', 'Intensity', 'a.u.'], title='Raman spectra', fig=[20, '#e6f0f8'])
        reference.__init__(self, material, 'raman')
        self.img = plt.imread(rawdatafile+raman.imgformat)
        plt.clf()
        #fig = plt.figure(figsize=(self.fig[0],aspect*self.fig[0]), constrained_layout=True);
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(self.fig[0],0.2*self.fig[0]), gridspec_kw={'width_ratios': [1, 3.5]})
        
        #gs = fig.add_gridspec(1, 2);
        #ax1 = fig.add_subplot(gs[0, 0])
        ax1.imshow(self.img)
        ax1.title.set_text("Sample image")
        #ax2 = fig.add_subplot(gs[0, 1:])
        ax2.set_yticklabels('')
        self.plot(ax=ax2, title = "Full Spectra")
        plt.show();
