import customtkinter as tk
import string

from tkinter import filedialog

import utility_functions as uf  # import utility functions
import gcode_translator as gt  # import gcode translator
import rt_user_functions as ruf  # extra functions such as 'exiting'

from globals import GlobalState
from globals import RobotStats


def button_function():
    print("Button pressed")
    return



global status_text
global z_offset_textbox
global speed_textbox

def print_control(root, leftcol, rightcol, buttoncolor, rcol):
    #button to initialize the robot
    init_button = tk.CTkButton(master=root, text="Initialize Robot", font=("Avenir Heavy",15), fg_color= buttoncolor, command=init_print_but)
    init_button.place(relx=leftcol, rely=0.50, anchor=tk.NW)

    #button to set file path
    file_button = tk.CTkButton(master=root, text="Select File", font=("Avenir Heavy",15),fg_color= '#089DC3', command=select_file)
    file_button.place(relx=leftcol, rely=0.35, anchor=tk.NW)

    #button to start printing
    start_button = tk.CTkButton(master=root, text="Start Printing", font=("Avenir Heavy",15),fg_color= buttoncolor, command=start_print_but)
    start_button.place(relx=leftcol, rely=0.65, anchor=tk.NW)

    #button to stop printing
    start_button = tk.CTkButton(master=root, text="Stop Printing", font=("Avenir Heavy",15), fg_color= '#DC0F24' ,command=stop_print_but)
    start_button.place(relx=leftcol, rely=0.80, anchor=tk.NW)

    return

def print_monitor(root, leftcol, rightcol, buttoncolor, rcol):
    global status_text

    #status info
    status_label = tk.CTkLabel(master=root, text="Status:", font=("Avenir Heavy", 15, 'bold'), width = 40, pady = 10, anchor = 'center')
    status_label.place(relx=leftcol, rely=0.18, anchor=tk.NW)

    status_text = tk.CTkLabel(master=root, text = " - ", font=("Avenir Heavy",12), height=4, width=450, anchor = tk.W)
    status_text.place(relx=leftcol, rely=0.25, anchor=tk.NW)

    status_text.configure(text = GlobalState().status_text)

    #terminal info
    terminal_label = tk.CTkLabel(master=root, text="Print info", font=("Avenir Heavy", 15, 'bold'), width = 40, pady = 10, anchor = 'center')
    terminal_label.place(relx=rightcol, rely=0.18, anchor=tk.NW)

    terminal_text = tk.CTkLabel(master=root, text = " - ", font=("Avenir",12), height=root.winfo_screenheight()*0.35, width=350,fg_color = '#1A0F10', anchor = tk.NW)
    terminal_text.place(relx=rightcol, rely=0.25, anchor=tk.NW)

    terminal_text.configure(text = "This is updated")

    return

def cosmetics(root, leftcol, rightcol, buttoncolor, rcol):
    #title
    info_title = tk.CTkLabel(master=root, text="SonoBone control interface", font=("Avenir Heavy", 25, 'bold'), fg_color= '#333332', width = root.winfo_screenwidth(), pady = 20, anchor = 'center')
    info_title.place(relwidth = 1)

    return


def tuning(root, leftcol, rightcol, buttoncolor, rcol):

    global z_offset_textbox
    global speed_textbox
    #set z offsetbutton up and down
    z_offset_up_button = tk.CTkButton(master=root, text="↑", font=("Avenir Heavy",15), fg_color= buttoncolor, command=z_up_but, width = 50, height = 25, anchor = 'center')
    z_offset_up_button.place(relx=rcol, rely=0.25, anchor=tk.NW)
    z_offset_down_button = tk.CTkButton(master=root, text="↓", font=("Avenir Heavy",15), fg_color= buttoncolor, command=z_down_but, width = 50, height = 25, anchor = 'center')
    z_offset_down_button.place(relx=rcol, rely=0.45, anchor=tk.NW)

    #z offset textbox
    z_offset_textbox = tk.CTkEntry(master=root, font=("Avenir", 15), width=50)
    z_offset_textbox.place(relx=rcol, rely=0.35, anchor=tk.NW)
    # Set the text of z_offset_textbox
    z_offset_textbox.insert(0, GlobalState().user_z_offset)

    z_offset_label= tk.CTkLabel(master=root, text="Z-offset", font=("Avenir Heavy", 15, 'bold'), width = 40, anchor = 'center')
    z_offset_label.place(relx=rcol, rely=0.18, anchor=tk.NW)

    #set speed button up and down
    speed_up_button = tk.CTkButton(master=root, text="↑", font=("Avenir Heavy",15), fg_color= buttoncolor, command=speed_up_but, width = 50, height = 25)
    speed_up_button.place(relx=rcol, rely=0.63, anchor=tk.NW)
    speed_down_button = tk.CTkButton(master=root, text="↓", font=("Avenir Heavy",15), fg_color= buttoncolor, command=speed_down_but, width = 50, height = 25, anchor = 'center')
    speed_down_button.place(relx=rcol, rely=0.83, anchor=tk.NW)

    #speed textbox
    speed_textbox = tk.CTkEntry(master=root, font=("Avenir", 15), width=50)
    speed_textbox.place(relx=rcol, rely=0.73, anchor=tk.NW)
    speed_textbox.insert(0, f'{GlobalState().printspeed_percentage}%')

    speed_label= tk.CTkLabel(master=root, text="Speed", font=("Avenir Heavy", 15, 'bold'), width = 40, anchor = 'center')
    speed_label.place(relx=rcol, rely=0.56, anchor=tk.NW)

    return

#------------------ Button functions ------------------

def start_print_but():

    return
    

def stop_print_but():

    return


def init_print_but():
    #initiate robot
    Robotuf.activationsequence()
    return


def reset():

    return

def z_up_but():
    global z_offset_textbox
    GlobalState().user_z_offset += GlobalState().user_z_offset_increment
    z_offset_textbox.delete(0, tk.END)
    # Insert the new text
    z_offset_textbox.insert(0, str(GlobalState().user_z_offset))
    return

def z_down_but():
    global z_offset_textbox
    GlobalState().user_z_offset -= GlobalState().user_z_offset_increment
    z_offset_textbox.delete(0, tk.END)
    # Insert the new text
    z_offset_textbox.insert(0, str(GlobalState().user_z_offset))
    return


def speed_up_but():
    global speed_textbox
    GlobalState().printspeed_percentage += GlobalState().printspeed_increment
    speed_textbox.delete(0, tk.END)
    # Insert the new text
    speed_textbox.insert(0, f'{GlobalState().printspeed_percentage}%')
    return

def speed_down_but():
    global speed_textbox
    GlobalState().printspeed_percentage -= GlobalState().printspeed_increment
    speed_textbox.delete(0, tk.END)
    # Insert the new text
    speed_textbox.insert(0, f'{GlobalState().printspeed_percentage}%')
    return
    


def select_file():
    global status_text
    file_path = filedialog.askopenfilename()
    print("Selected file:", file_path)
    # Use the file_path variable as needed
    GlobalState.filepath = file_path
    GlobalState.status_text = "File selected"
    status_text.configure(text=GlobalState().status_text)


# ------------------ GUI ------------------

def init_gui():
    
    leftcol = 0.05
    rightcol = 0.35
    rcol = 0.88
    buttoncolor = '#0859C3'

    tk.set_appearance_mode("System")  # Modes: system (default), light, dark
    tk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

    root = tk.CTk()  # create CTk window like you do with the Tk window
    root.geometry("700x420")
    root.title("SonoBone control interface")


    print_control(root, leftcol,rightcol,buttoncolor,rcol)
    print_monitor(root, leftcol,rightcol,buttoncolor,rcol)
    cosmetics(root, leftcol,rightcol,buttoncolor,rcol)
    tuning(root, leftcol,rightcol,buttoncolor,rcol)

    root.mainloop()
    

