## this is uncomplete launcher wish to execute webservices from raspberry pi, and show tkinter status screen at arm,

import tkinter
import subprocess
import sys
import os


def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


window = tkinter.Tk()
window.title("AR3 Web Service Launcher")
top_frame = tkinter.Frame(window).pack()
bottom_frame = tkinter.Frame(window).pack(side = "bottom")


# You will first create a division with the help of Frame class and align them on TOP and BOTTOM with pack() method.
top_frame = tkinter.Frame(window).pack()
bottom_frame = tkinter.Frame(window).pack(side = "bottom")
log_box_1 = tkinter.Text(top_frame, borderwidth=3, relief="sunken").pack()
print("Start tk inter")

p = subprocess.Popen(["sh","start.sh"])

while p.poll() is None:
    print('Still sleeping')
    time.sleep(1)


#for linetxt in execute(["sh","start.sh"]):
#    print(linetxt)
    # log_box_1.insert(tkinter.END, linetxt)


# Once the frames are created then you are all set to add widgets in both the frames.
# btn1 = tkinter.Button(top_frame, text = "Button1", fg = "red").pack() #'fg or foreground' is for coloring the contents (buttons)
# btn2 = tkinter.Button(top_frame, text = "Button2", fg = "green").pack()
# btn3 = tkinter.Button(bottom_frame, text = "Button3", fg = "purple").pack(side = "left") #'side' is used to left or right align the widgets
# btn4 = tkinter.Button(bottom_frame, text = "Button4", fg = "orange").pack(side = "left")
#command = "route.py"
#result = subprocess.run([sys.executable, "route.py",])
#print("Complete sub process, and run another thing")
window.mainloop()
print("outside window mainloop")




