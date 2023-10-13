import os
import tkinter
import random
from glob import iglob
import platform

import serial
import serial_asyncio
from time import sleep

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from functools import partial

import asyncio

import elm327

SERIAL_PORT = ""
SERIAL_SPEED = 0
SERIAL_PORTS = []
SERIAL = None
CONNECTED = False



async def update(window: tk.Tk) -> None:
    while True:
        try:
            window.state()
        except:
            loop.stop()
            exit(0)
        window.update()
        await asyncio.sleep(1 / 60)

def scan_serial_ports():
    global SERIAL_PORTS
    SERIAL_PORTS.clear()

    if platform.system().lower() == "linux":
        # iterate over every serial interface in /dev/ (like tty*, ttyACM*, ttyUSB*, etc)
        for interface in iglob("/dev/tty*"):
            try:
                s = serial.Serial(interface)                    # try to open the serial port
                s.close()                                       # close the port again
                SERIAL_PORTS.append(interface)                         # add the port to the list
            except serial.SerialException:
                continue                                        # port seems unavailable, continue

    elif platform.system() == "Windows":
        for i in range(1, 255):
            try:
                s = serial.Serial(f"COM{i}")                    # try to open every COM port
                s.close()                                       # close it again
                SERIAL_PORTS.append(f"COM{i}")
            except serial.SerialException:
                continue                                        # COM port seems to be unavailable, continue
    else:
        print("Unknown Operating System")


def return_fake_ports() -> list[str]:
    return [f"/dev/ttyACM{i}" for i in range(20)]


def serial_button_callback(win: tk.Toplevel, serial_list: tk.Listbox) -> None:
    scan_serial_ports()
    serial_list.config(listvariable=tk.Variable(value=SERIAL_PORTS))
    win.update()


def list_select(e: tk.Event):
    list_box: tk.Listbox = e.widget
    label: tk.Label = list_box.master.master.nametowidget("config_frame").nametowidget("name_label")

    cursor = list_box.curselection()[0]
    global SERIAL_PORT
    SERIAL_PORT = SERIAL_PORTS[cursor]
    label.config(text=SERIAL_PORT)


def show_serial_popup() -> None:
    win = tk.Toplevel()
    serial_ports = tk.Variable(master=win, name="serial_ports")
    serial_ports.set(["test1", "test2"])
    print(win.getvar("serial_ports"))
    win.wm_title("Serial Port Configuration")
    scan_serial_ports()

    list_frame = tk.Frame(master=win, padx=10, pady=10, name="list_frame")
    config_frame = tk.Frame(master=win, padx=10, pady=10, name="config_frame")

    list_frame.grid(row=0, column=0)
    config_frame.grid(row=0, column=1)
    print(SERIAL_PORTS)
    serial_list = tk.Listbox(master=list_frame, listvariable=tk.Variable(value=SERIAL_PORTS))
    serial_list.pack()
    serial_list.bind("<<ListboxSelect>>", list_select)

    label = tk.Label(master=config_frame, text=f"Selected Port:    {serial_list.curselection()}", name="name_label", )
    label.pack()

    refresh_button = tk.Button(master=config_frame, text="Re-Scan serial ports", command=partial(serial_button_callback, win, serial_list))
    refresh_button.pack()

    win.mainloop()


window = tk.Tk()

window.title("OBD2 Reader Giga Edition(tm)")

loop = asyncio.new_event_loop()


def text_popup(text: str):
    win = tk.Toplevel()
    text_label = tk.Label(master=win, text=text)
    text_label.pack()
    close_button = tk.Button(master=win, text="OK", command=win.destroy)
    close_button.pack()
    win.mainloop()


def connect_serial():
    if not SERIAL or SERIAL_PORTS or SERIAL_SPEED or SERIAL_PORT:
        text_popup("You have not selected a serial device! Please select one before connecting")


async def main():
    loop.create_task(update(window))

    menu = tk.Menu(master=window,)

    serial_menu = tk.Menu(menu, tearoff=0)
    file_menu = tk.Menu(menu, tearoff=0)
    stuff_menu = tk.Menu(menu, tearoff=0)

    serial_menu.add_command(label="Configure Serial Ports", command=show_serial_popup)
    serial_menu.add_command(label="Connect", command=connect_serial)

    file_menu.add_command(label="Exit", command=lambda m: m)
    stuff_menu.add_command(label="Stuff", command=show_serial_popup)

    menu.add_cascade(label="File", menu=file_menu)
    menu.add_cascade(label="Config", menu=serial_menu)
    menu.add_cascade(label="Stuff", menu=stuff_menu)

    window.config(menu=menu)

    tabs = ttk.Notebook(master=window)
    #menu.pack()

    status_tab = ttk.Frame(tabs)
    sensor_tab = ttk.Frame(tabs)
    nuts_tab = ttk.Frame(tabs)

    tabs.add(status_tab, text="Status")
    tabs.add(sensor_tab, text="Sensors")

    tabs.add(nuts_tab, text="Nuts")

    tabs.pack(expand=1, fill=tk.BOTH)

    columns = ("sensor", "value")

    sensor_view = ttk.Treeview(
        master=sensor_tab,
        columns=columns,
        show="headings",
        padding=0
    )

    sensor_view.heading("sensor", text="Sensor Name")
    sensor_view.heading("value", text="Sensor Name")

    sensor_view.pack()

    sensor_items = []

    for i in range(0, 20):
        sensor_items.append(sensor_view.insert("", tk.END, values=(f"Sensor #{i}", random.random() * i)))




loop.create_task(update(window))
loop.create_task(main())
loop.run_forever()
#loop.run_until_complete(main())

