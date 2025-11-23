import time 
extra_time = 3.5
safe_fill_time = min(extra_time, 5)

for i in range(int(safe_fill_time)):
    print(i)
    time.sleep(0.5)