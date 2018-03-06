import re
import sys
from collections import defaultdict
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import tkinter as tk

if len(sys.argv) != 2:
    print("Must supply a file to parse")
    sys.exit(1)

# dict to hold all the data
data = defaultdict(dict)

# get the data and time seperate
time_date_r = "^(\d+):(.*)"
# get each set of data
key_value_r = "(\w+)=((?:\+|-)?(?:\d|\.|T|F)+)"

with open(sys.argv[1], "r") as input:
    # get each line of input
    for line in input:
        time_date_m = re.search(time_date_r, line)
        # if found
        if time_date_m:
            time = int(time_date_m.group(1))
            # split based on seperaror, whihc is comma
            entries = time_date_m.group(2).split(",")
            for entry in entries:
                key_value_m = re.search(key_value_r, entry)
                if key_value_m:
                    key = key_value_m.group(1)
                    value = key_value_m.group(2)
                    if value == 'T':
                        data[key][time] = 1
                    elif value == 'F':
                        data[key][time] = 0
                    else:
                        data[key][time] = float(value)


# make window manager
master = tk.Tk()
# make title
l = tk.Label(master, text="Robot Log: {0}".format(sys.argv[1]))
l.pack()
#make checkbuttons
chbxs = {}
for catagory in data.keys():
    var = tk.IntVar()
    c = tk.Checkbutton(master, text=catagory, variable=var)
    c.var = var
    c.pack()
    chbxs[catagory] = c

def button_pressed():
    f.clf()
    for catagory, chbx in chbxs.items():
        if chbx.var.get():
            x = [];
            y = [];
            for time, value in data[catagory].items():
                x.append(time)
                y.append(value)
            a = f.add_subplot(111)
            a.plot(x, y, "o-", label=catagory)
    f.legend()
    dataPlot.draw()

b = tk.Button(master, text="Update", command=button_pressed)
b.pack()

f = Figure(figsize=(5,4), dpi=100)

dataPlot = FigureCanvasTkAgg(f, master=master)
dataPlot.show()
dataPlot.get_tk_widget().pack()

master.mainloop()
