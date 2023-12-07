import time
import board
import digitalio
import busio
import usb_cdc
import adafruit_icm20x
import adafruit_gps
import storage
import sdcardio
import os

# gps library https://github.com/adafruit/Adafruit_CircuitPython_GPS
# imu library https://learn.adafruit.com/adafruit-tdk-invensense-icm-20948-9-dof-imu/python-circuitpython

data = {
    "test" : "test",
    "GPS" : {
        "lattitude" : 'NA',
        "longtiude" : 'NA',
        "elevation" : 'NA',
        "num_satellites" : 'NA'
    },
    "IMU" : {
        "velocity" : 'NA',
        "acceleration" : 'NA',
        "mag_field" : 'NA',
    }
}

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

imu_i2c = busio.I2C(scl=board.GP21, sda=board.GP20)   # instantiate i2c for imu, scl 27 = gp21, sda 26 = gp20
imu_i2c.try_lock()
imu_addy = hex(imu_i2c.scan()[0])
imu_i2c.unlock()
imu = adafruit_icm20x.ICM20948(imu_i2c, int(imu_addy))

gps_scl_pin = "GP19" #integar value specifying pico pin
gps_sda_pin = "GP18"
gps_i2c = busio.I2C(scl = board.GP19, sda=board.GP18)
gps_i2c.try_lock()
gps_addy = hex(gps_i2c.scan()[0])
gps_i2c.unlock()
gps = adafruit_gps.GPS_GtopI2C(gps_i2c, address = int(gps_addy), debug=False)

radio_rx_pin = "GP1"
radio_tx_pin = "GP0"
radio_baud_rate = 9600 # from datasheet
radio_uart = busio.UART(tx = board.GP0, rx = board.GP1, baudrate = 9600)

gui_rx_pin = "GP5"
gui_tx_pin = "GP4"
gui_baud_rate = 9600 # default?
gui_uart = busio.UART(tx = board.GP4, rx = board.GP5, baudrate = 9600, timeout = 0.1)

sd_mosi_pin = "GP11"
sd_miso_pin = "GP12"
sd_sck_pin = "GP10"
sd_chip_select = "GP13"
sd_spi = busio.SPI(clock = board.GP10, MOSI = board.GP11, MISO = board.GP12)

#sd = sdcardio.SDCard(sd_spi, board.GP13)
#vfs = storage.VfsFat(sd)
#storage.mount(vfs, '/sd')
#os.listdir('/sd')


def uart_write(port, data):
    data_b = str.encode(data)
    port.write(data_b)

def uart_read(port, num_bytes):
    data = port.read(num_bytes) # returned as byte array
    data_string = ''.join([chr(b) for b in data])
    return data_string

def gui_uart_read(port, num_bytes, state):
    data = port.read(num_bytes) # returned as byte array
    if data != None:
        data_string = ''.join([chr(b) for b in data])
        if data_string == "start":
            return True
        if data_string == "stop":
            return False
    
    return state

def i2c_read(port):
    port.try_lock() # need to lock i2c before scanning
    add = hex((port.scan())[0]) # get first address from i2c port
    port.unlock()

    i2c.readfrom_into(0x18, data)
    data_string = ''.join([chr(b) for b in data])
    return data_string

def sd_write(data):
    with open("/sd/data.txt", "w") as f:
        f.write(data)


### MAIN ###

start = False

while True:
    while not start:
        led.value = True
        if gui_uart_read(gui_uart, 8, start):
            start = True
        time.sleep(0.2)
        led.value = False
        if gui_uart_read(gui_uart, 8, start):
            start = True
        time.sleep(0.2)

    while start:
        led.value = True

        # gps data
        gps.update()
        data["GPS"]["lattitude"] = str(gps.latitude)
        data["GPS"]["longtiude"] = str(gps.longitude)
        data["GPS"]["elevation"] = str(gps.altitude_m)
        data["GPS"]["num_satellites"] = str(gps.satellites)

        # imu data
        data["IMU"]["velocity"] = "%.2f + %.2f + %.2f" % imu.gyro
        data["IMU"]["acceleration"] = "%.2f + %.2f + %.2f" % imu.acceleration
        data["IMU"]["mag_field"] = "%.2f + %.2f + %.2f" % imu.magnetic

        # "-" used as delimeter for parsing
        data_line = " %s + %s + %s + %s + %s + %s + %s " % (data["GPS"]["lattitude"], data["GPS"]["longtiude"],
                                                           data["GPS"]["elevation"], data["GPS"]["num_satellites"],
                                                           data["IMU"]["velocity"], data["IMU"]["acceleration"],
                                                           data["IMU"]["mag_field"])
        print(data_line)
        # write to SD
        #sd_write(data_line)

        # write to radio
        uart_write(radio_uart, data_line)

        # write to gui
        uart_write(gui_uart, data_line)
        
        if not gui_uart_read(gui_uart, 8, start):
            start = False

        time.sleep(0.1)

