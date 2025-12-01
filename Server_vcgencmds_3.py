# TPRG 2 ASSIGNMENT 2
# Server_csgencmds.py
# Kyle Krepelka
# 100923825
# Nov 30, 2025

# This server runs on Pi, sends Pi's your 4 arguments from the vcgencmds, sent as Json object.

# details of the Pi's vcgencmds - https://www.tomshardware.com/how-to/raspberry-pi-benchmark-vcgencmd
# more vcgens on Pi 4, https://forums.raspberrypi.com/viewtopic.php?t=245733
# more of these at https://www.nicm.dev/vcgencmd/

import socket
import os
import time
import json

s = socket.socket()
host = '192.168.2.178'
port = 5000
s.bind((host, port))
s.listen(5)

# CPU TEMPERATURE 
raw_temp = os.popen("vcgencmd measure_temp").readline().strip()
# Example output: "temp=48.1'C"
try:
    temp_value = raw_temp.replace("temp=", "").replace("'C", "")
    temp_value = float(temp_value)
except:
    temp_value = None


# CLOCK SPEED
raw_clock = os.popen("vcgencmd measure_clock arm").readline().strip()

try:
    clk_value = int(raw_clock.split('=')[1])
except:
    clk_value = None


# GPU Memory
raw_gpu_mem = os.popen("vcgencmd get_mem gpu").readline().strip()
# Example output: "gpu=76M"

try:
    gpu_mem_mb = int(''.join(filter(str.isdigit, raw_gpu_mem)))
except:
    gpu_mem_mb = None
                

# Build a JSON dictionary
f_dict = {
    "CPU_Temperature": {
        "raw": raw_temp,
        "temp_c": temp_value
    },
    "CPU_Clock": {
        "raw": raw_clock,
        "freq_hz": clk_value,
        "freq_mhz": clk_value / 1_000_000 if clk_value else None
    },
    "GPU_Memory": {
        "raw": raw_gpu_mem,
        "gpu_mem_mb": gpu_mem_mb
    }
}
    


while True:
    c, addr = s.accept()
    print('Got connection from', addr)
    
    json_bytes = json.dumps(f_dict).encode()

    c.send(json_bytes)
    c.close()
