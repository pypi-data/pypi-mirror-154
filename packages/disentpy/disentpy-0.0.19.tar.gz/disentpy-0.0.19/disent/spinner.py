import time
import threading

def bouncing_ball(arg):
    t = threading.currentThread()
    i,n = 0,25
    while getattr(t, "do_run", True):
        lfill = i % n
        rfill = n - lfill
        s = " "*lfill + "●" + " "*rfill
        if int(i/n) % 2 ==1:
            s = s[::-1]
        s = f"[{s}]"
        print(f'Executing {arg}',s,end='\r')
        time.sleep(0.05)
        i+=1