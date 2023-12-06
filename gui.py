from tkinter import *
from tkinter import ttk
import serial
import re

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

## GPS ##

lat_label = ttk.Label(mainframe, font = font, padding = padding, text='Lattitude')
lat_label.grid(column=0, row=0)

long_label = ttk.Label(mainframe, font = font, padding = padding, text='Longitude')
long_label.grid(column=1, row=0)

elev_label = ttk.Label(mainframe, font = font, padding = padding, text='Elevation')
elev_label.grid(column=2, row=0)

num_sat_label = ttk.Label(mainframe, font = font, padding = padding, text='Num satellites')
num_sat_label.grid(column=3, row=0)

## IMU ##

# vel #

vel_x_label = ttk.Label(mainframe, font = font, padding = padding, text='Velocity: X')
vel_x_label.grid(column=0, row=2)

vel_y_label = ttk.Label(mainframe, font = font, padding = padding, text='Velocity: Y')
vel_y_label.grid(column=1, row=2)

vel_z_label = ttk.Label(mainframe, font = font, padding = padding, text='Velocity: Z')
vel_z_label.grid(column=2, row=2)

# acc #

acc_x_label = ttk.Label(mainframe, font = font, padding = padding, text='Acceleration: X')
acc_x_label.grid(column=0, row=4)

acc_y_label = ttk.Label(mainframe, font = font, padding = padding, text='Acceleration: Y')
acc_y_label.grid(column=1, row=4)

acc_z_label = ttk.Label(mainframe, font = font, padding = padding, text='Acceleration: Z')
acc_z_label.grid(column=2, row=4)

# mag #

mag_x_label = ttk.Label(mainframe, font = font, padding = padding, text='Mag field: X')
mag_x_label.grid(column=0, row=6)

mag_y_label = ttk.Label(mainframe, font = font, padding = padding, text='Mag field: Y')
mag_y_label.grid(column=1, row=6)

mag_z_label = ttk.Label(mainframe, font = font, padding = padding, text='Mag field: Z')
mag_z_label.grid(column=2, row=6)

### data display ####

data = data_struct

data["GPS"]["lattitude"] = StringVar()
data["GPS"]["longtiude"] = StringVar()
data["GPS"]["elevation"] = StringVar()
data["GPS"]["num_satellites"] = StringVar()

# imu data
data["IMU"]["velocity"]['x'] = StringVar()
data["IMU"]["velocity"]['y'] = StringVar()
data["IMU"]["velocity"]['z'] = StringVar()
data["IMU"]["acceleration"]['x'] = StringVar()
data["IMU"]["acceleration"]['y'] = StringVar()
data["IMU"]["acceleration"]['z'] = StringVar()
data["IMU"]["mag_field"]['x'] = StringVar()
data["IMU"]["mag_field"]['y'] = StringVar()
data["IMU"]["mag_field"]['z'] = StringVar()

font = ("TkDefaultFont", 14)
padding = 0

## GPS ##

lat_data = ttk.Label(mainframe, font = font, padding = padding, textvariable = data["GPS"]["lattitude"])
lat_data.grid(column=0, row=1)

long_data = ttk.Label(mainframe, font = font, padding = padding, textvariable = data["GPS"]['longtiude'])
long_data.grid(column=1, row=1)

elev_data = ttk.Label(mainframe, font = font, padding = padding, textvariable = data["GPS"]['elevation'])
elev_data.grid(column=2, row=1)

num_sat_data = ttk.Label(mainframe, font = font, padding = padding, textvariable = data["GPS"]["num_satellites"])
num_sat_data.grid(column=3, row=1)

## IMU ##

# vel #

vel_x_data = ttk.Label(mainframe, font = font, padding = padding, textvariable = data["IMU"]["velocity"]['x'])
vel_x_data.grid(column=0, row=3)

vel_y_data = ttk.Label(mainframe, font = font, padding = padding, textvariable = data["IMU"]["velocity"]['y'])
vel_y_data.grid(column=1, row=3)

vel_z_data = ttk.Label(mainframe, font = font, padding = padding, textvariable = data["IMU"]["velocity"]['z'])
vel_z_data.grid(column=2, row=3)

# acc #

acc_x_data = ttk.Label(mainframe, font = font, padding = padding, textvariable = data["IMU"]["acceleration"]['x'])
acc_x_data.grid(column=0, row=5)

acc_y_data = ttk.Label(mainframe, font = font, padding = padding, textvariable = data["IMU"]["acceleration"]['y'])
acc_y_data.grid(column=1, row=5)

acc_z_data = ttk.Label(mainframe, font = font, padding = padding, textvariable = data["IMU"]["acceleration"]['z'])
acc_z_data.grid(column=2, row=5)

# mag #

mag_x_data = ttk.Label(mainframe, font = font, padding = padding, textvariable = data["IMU"]["mag_field"]['x'])
mag_x_data.grid(column=0, row=7)

mag_y_data = ttk.Label(mainframe, font = font, padding = padding, textvariable = data["IMU"]["mag_field"]['y'])
mag_y_data.grid(column=1, row=7)

mag_z_data = ttk.Label(mainframe, font = font, padding = padding, textvariable = data["IMU"]["mag_field"]['z'])
mag_z_data.grid(column=2, row=7)

### buttons ###

running = False
status = StringVar()
status.set("Press start")

status_label = ttk.Label(mainframe, font = ("TkDefaultFont", 24, "bold"), padding = 10, text='Status')
status_label.grid(column=3, row=6)

status_data = ttk.Label(mainframe, font = font, padding = padding, textvariable = status)
status_data.grid(column=3, row=7)

def start():
    running = True
    status.set("Running")
    # serial_write(b'doesnt matter')

def stop():
    running = False
    status.set("Paused")
    # serial_write(b'doesnt matter')

start = ttk.Button(mainframe, text='Start', command = start)
start.grid(column=3, row=2)

stop = ttk.Button(mainframe, text='Stop', command = stop)
stop.grid(column=3, row=4)

### I/O with pico ###

serial_port = "/dev/cu.usbmodem1101"
pico_serial = serial.Serial(serial_port, timeout=0.2)

def serial_read():
    data = pico_serial.read()
    data_string = ''.join([chr(b) for b in data])
    return data_string

def serial_write(data):
    pico_serial.write(data)

### main ###

while True:
    root.update()
    usb_data = serial_read()
    root.update()
    usb_data = " 1 - 2 - 3 - 4 - a1 - a2 - a3 - b1 - b2 - b3 - c1 - c2 - c3 -"
    regex = re.findall(" (.*?) -", usb_data)

    data["GPS"]["lattitude"].set(regex[0])
    data["GPS"]["longtiude"].set(regex[1])
    data["GPS"]["elevation"].set(regex[2])
    data["GPS"]["num_satellites"].set(regex[3])
    root.update()

    # imu data
    data["IMU"]["velocity"]['x'].set(regex[4])
    data["IMU"]["velocity"]['y'].set(regex[5])
    data["IMU"]["velocity"]['z'].set(regex[6])
    data["IMU"]["acceleration"]['x'].set(regex[7])
    data["IMU"]["acceleration"]['y'].set(regex[8])
    data["IMU"]["acceleration"]['z'].set(regex[9])
    data["IMU"]["mag_field"]['x'].set(regex[10])
    data["IMU"]["mag_field"]['y'].set(regex[11])
    data["IMU"]["mag_field"]['z'].set(regex[12])
    print('loop')

    root.update()

