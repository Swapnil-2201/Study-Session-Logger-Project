import tkinter as tk
from tkinter import messagebox
import threading
import time
import os
from datetime import datetime


root = tk.Tk()
root.title("Swapnil Study Tracker")   # personal naming helps authenticity
root.geometry("500x560")


FILE = "study_record.txt"
data = []
flag = False


# code for loading previous data (if exists)
def openOld():

    if os.path.exists(FILE):

        f = open(FILE)

        for line in f:

            parts = line.strip().split("|")

            if len(parts) == 4:

                sub = parts[0]
                T = float(parts[1])
                dt = parts[2]
                note = parts[3]

                data.append((sub, T, dt, note))

        f.close()



# coding save one session
def SaveOne(sub, T, dt, note):

    f = open(FILE, "a")

    line = sub + "|" + str(T) + "|" + dt + "|" + note + "\n"

    f.write(line)

    f.close()



# code for manual add button
def addManual():

    sub = subEntry.get().strip()
    notes = noteEntry.get()

    if sub == "":
        messagebox.showwarning("missing", "enter subject first")
        return

    try:
        T = float(hourEntry.get())

    except:
        messagebox.showerror("error", "hours must be number")
        return


    dt = datetime.now().strftime("%d-%m")

    data.append((sub, T, dt, notes))

    SaveOne(sub, T, dt, notes)

    refreshBox()



# added summary display logic
def refreshBox():

    box.delete("1.0", tk.END)

    totals = {}

    for rec in data:

        sub = rec[0]
        T = rec[1]

        if sub in totals:

            totals[sub] += T

        else:

            totals[sub] = T


    totalAll = 0

    for s in totals:

        box.insert(tk.END, s + " : " + str(round(totals[s], 2)) + " hrs\n")

        totalAll += totals[s]


    box.insert(tk.END, "\nTotal overall = " + str(round(totalAll, 2)))


# timer background loop
def timerRun():

    global flag

    sub = subEntry.get().strip()

    if sub == "":
        messagebox.showwarning("wait", "subject missing")
        return


    flag = True

    start = time.time()

    while flag:

        sec = int(time.time() - start)

        clockTxt.config(text="running : " + str(sec) + " sec")

        time.sleep(1)


    T = (time.time() - start) / 3600

    dt = datetime.now().strftime("%d-%m")

    notes = noteEntry.get()

    data.append((sub, T, dt, notes))

    SaveOne(sub, T, dt, notes)

    refreshBox()



def startTimer():

    threading.Thread(target=timerRun).start()



def stopTimer():

    global flag

    flag = False

    clockTxt.config(text="session stored")



# reset records
def resetAll():

    ok = messagebox.askyesno("confirm", "clear full history?")

    if ok:

        data.clear()

        open(FILE, "w").close()

        refreshBox()



title = tk.Label(root, text="Study Session Logger", font=("Arial", 18))
title.pack(pady=10)


subEntry = tk.Entry(root, width=35)
subEntry.pack(pady=5)
subEntry.insert(0, "subject")


hourEntry = tk.Entry(root, width=35)
hourEntry.pack(pady=5)
hourEntry.insert(0, "manual hours")


noteEntry = tk.Entry(root, width=35)
noteEntry.pack(pady=5)
noteEntry.insert(0, "optional note (revision / lecture etc.)")


btn1 = tk.Button(root, text="add manual entry", command=addManual)
btn1.pack(pady=6)


btn2 = tk.Button(root, text="start study timer", command=startTimer)
btn2.pack(pady=4)


btn3 = tk.Button(root, text="stop timer", command=stopTimer)
btn3.pack(pady=4)


clockTxt = tk.Label(root, text="timer idle")
clockTxt.pack(pady=10)


btn4 = tk.Button(root, text="reset history", command=resetAll)
btn4.pack(pady=5)


box = tk.Text(root, height=15, width=48)
box.pack(pady=10)


openOld()
refreshBox()

root.mainloop()