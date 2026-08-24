import time
import psutil

def display_usage(cpu_usage , mem_usage , bars = 50):
    cpu_percent = (cpu_usage / 100.0)
    cpu_bar = "#" * int(cpu_percent * bars) + "-" * (bars - int(cpu_percent * bars))

    mem_percent = (mem_usage / 100.0)
    mem_bar = "#" * int(mem_percent * bars) + "-" * (bars - int(mem_percent * bars))
    print(f"CPU usage: |{cpu_bar}| {cpu_usage:.3f}%" , end = "")
    print(f"   Mem usage: |{mem_bar}| {mem_usage:.3f}%" , end = "\r")

while True:
    display_usage(psutil.cpu_percent() , psutil.virtual_memory().percent , 30)
    time.sleep(0.5)