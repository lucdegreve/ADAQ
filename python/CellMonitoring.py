

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as dates

from datetime import datetime
from datetime import timedelta



colors = sns.color_palette("muted")
xfmt = dates.DateFormatter('%Y-%m-%d\n%H:%M:%S')



class CellMonitoring:

  def __init__(self, fig, cell_id, np, legend=False):
    self.nprobes = np
    self.times =  [[] for x in range(5)]
    self.temperatures =  [[] for x in range(5)]

    self.ax = fig.add_subplot(4,2,cell_id)
    self.ax.grid(True)
    self.ax.xaxis_date()
    self.datemin = datetime.now()
    self.datemax = datetime.now()+timedelta(seconds=60)
    self.ax.set_xlim(self.datemin, self.datemax)
    self.ax.xaxis.set_major_formatter(xfmt)
    plt.xticks(rotation=90)
    self.ax.set_ylim(-10,70)

    self.lines = []

    for i in range(np):
      line, = self.ax.plot(self.times[i], self.temperatures[i], c=colors[i], linestyle = '', marker = '.', label='S'+str(i+1))
      self.lines.append(line)

    if legend:
      self.ax.legend(bbox_to_anchor=(0.0, -1.0), loc=1, ncol=5)


  def appendtemp(self, n, t):
    self.times[n].append(datetime.now())
    self.temperatures[n].append(t)
    self.lines[n].set_xdata(self.times[n])
    self.lines[n].set_ydata(self.temperatures[n])                                                                                                                                                           
    self.ax.draw_artist(self.lines[n])
    if datetime.now() > self.datemax:
      delta = datetime.now()-self.datemin
      self.datemax = datetime.now() + delta
      self.ax.set_xlim(self.datemin, self.datemax)
                                                     
