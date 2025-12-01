
import socket
import json

host = "192.168.2.178"
port = 5000
s = socket.socket()
s.connect((host, port))
data = s.recv(1024)
s.close()

# Show what was received 
print("Raw received:", data)
json_str = data.decode()
info = json.loads(json_str)

print("\n===== Raspberry Pi System Info =====")

# CPU Temperature
cpu = info["CPU_Temperature"]
print(f"CPU Temperature: {cpu['temp_c']} °C")

# CPU Clock
clk = info["CPU_Clock"]
print(f"CPU Frequency: {clk['freq_mhz']} MHz")

# GPU Memory 
gpu = info["GPU_Memory"]
print(f"GPU Memory: {gpu['gpu_mem_mb']} MB")

# Core Voltage
volts = info["Core_Voltage"]
print(f"Core Voltage: {volts['volts']} V")
