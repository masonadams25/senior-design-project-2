from tkinter import *
from tkinter import ttk

from data import data_struct

root = Tk() # create main root for gui
root.title("Project 2 GUI")

mainframe = ttk.Frame(root, padding="3 3 12 12") # create main frame
mainframe.grid(column=0, row=0, sticky=(N, W, E, S)) # set grid layout onto frame
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

### labels ###

font = ("TkDefaultFont", 24, "bold")
padding = 10

# GPS #

lat_label = ttk.Label(mainframe, font = font, padding = padding, text='Lattitude')
lat_label.grid(column=0, row=0)

long_label = ttk.Label(mainframe, font = font, padding = padding, text='Longitude')
long_label.grid(column=1, row=0)

elev_label = ttk.Label(mainframe, font = font, padding = padding, text='Elevation')
elev_label.grid(column=2, row=0)

num_sat_label = ttk.Label(mainframe, font = font, padding = padding, text='Num satellites')
num_sat_label.grid(column=3, row=0)

# IMU #

# Vel #

vel_x_label = ttk.Label(mainframe, font = font, padding = padding, text='Velocity: X')
vel_x_label.grid(column=0, row=2)

vel_y_label = ttk.Label(mainframe, font = font, padding = padding, text='Velocity: Y')
vel_y_label.grid(column=1, row=2)

vel_z_label = ttk.Label(mainframe, font = font, padding = padding, text='Velocity: Z')
vel_z_label.grid(column=2, row=2)

# Acc #

acc_x_label = ttk.Label(mainframe, font = font, padding = padding, text='Acceleration: X')
acc_x_label.grid(column=0, row=4)

acc_y_label = ttk.Label(mainframe, font = font, padding = padding, text='Acceleration: Y')
acc_y_label.grid(column=1, row=4)

acc_z_label = ttk.Label(mainframe, font = font, padding = padding, text='Acceleration: Z')
acc_z_label.grid(column=2, row=4)

# Mag #

mag_x_label = ttk.Label(mainframe, font = font, padding = padding, text='Mag field: X')
mag_x_label.grid(column=0, row=6)

mag_y_label = ttk.Label(mainframe, font = font, padding = padding, text='Mag field: Y')
mag_y_label.grid(column=1, row=6)

mag_z_label = ttk.Label(mainframe, font = font, padding = padding, text='Mag field: Z')
mag_z_label.grid(column=2, row=6)

### data display ####

data = data_struct

font = ("TkDefaultFont", 14)
padding = 0

# GPS #

lat_data = ttk.Label(mainframe, font = font, padding = padding, text = data["GPS"]["lattitude"])
lat_data.grid(column=0, row=1)

long_data = ttk.Label(mainframe, font = font, padding = padding, text = data["GPS"]['longtiude'])
long_data.grid(column=1, row=1)

elev_data = ttk.Label(mainframe, font = font, padding = padding, text = data["GPS"]['elevation'])
elev_data.grid(column=2, row=1)

num_sat_data = ttk.Label(mainframe, font = font, padding = padding, text = data["GPS"]["num_satellites"])
num_sat_data.grid(column=3, row=1)

# IMU #

# Vel #

vel_x_data = ttk.Label(mainframe, font = font, padding = padding, text = data["IMU"]["velocity"]["x"])
vel_x_data.grid(column=0, row=3)

vel_y_data = ttk.Label(mainframe, font = font, padding = padding, text = data["IMU"]["velocity"]["y"])
vel_y_data.grid(column=1, row=3)

vel_z_data = ttk.Label(mainframe, font = font, padding = padding, text = data["IMU"]["velocity"]["z"])
vel_z_data.grid(column=2, row=3)

# Acc #

acc_x_data = ttk.Label(mainframe, font = font, padding = padding, text = data["IMU"]["acceleration"]["x"])
acc_x_data.grid(column=0, row=5)

acc_y_data = ttk.Label(mainframe, font = font, padding = padding, text = data["IMU"]["acceleration"]["y"])
acc_y_data.grid(column=1, row=5)

acc_z_data = ttk.Label(mainframe, font = font, padding = padding, text = data["IMU"]["acceleration"]["x"])
acc_z_data.grid(column=2, row=5)

# Mag #

mag_x_data = ttk.Label(mainframe, font = font, padding = padding, text = data["IMU"]["mag_field"]["x"])
mag_x_data.grid(column=0, row=7)

mag_y_data = ttk.Label(mainframe, font = font, padding = padding, text = data["IMU"]["mag_field"]["y"])
mag_y_data.grid(column=1, row=7)

mag_z_data = ttk.Label(mainframe, font = font, padding = padding, text = data["IMU"]["mag_field"]["z"])
mag_z_data.grid(column=2, row=7)

### Buttons ###

running = False
status = StringVar()
status.set("Paused")

status_label = ttk.Label(mainframe, font = ("TkDefaultFont", 24, "bold"), padding = 10, text='Status')
status_label.grid(column=3, row=6)

status_data = ttk.Label(mainframe, font = font, padding = padding, textvariable = status)
status_data.grid(column=3, row=7)


def start():
    running = True
    status.set("Running")

def stop():
    running = False
    status.set("Paused")

start = ttk.Button(mainframe, text='Start', command = start)
start.grid(column=3, row=2)

stop = ttk.Button(mainframe, text='Stop', command = stop)
stop.grid(column=3, row=4)

while running:
    pass

root.mainloop()