#This program is a time management app where it helps someone with time management by gamifying it.
import tkinter as tk
from tkinter import messagebox
import os 
import time
from datetime import datetime
#making sure the current directory is the same as the file
os.chdir(os.path.dirname(os.path.abspath(__file__)))

 # this function converts seconds to hours minutes and seconds (hr,min,sec)
def sec_to_time(total_seconds):
    hours = total_seconds/3600
    hour = int(hours)
    print(f"hours: {hour}")

    minutes = (hours-hour)*60
    minute = int(minutes)
    print(f"minutes: {minute}")

    seconds = (minutes-minute)*60
    second = int(seconds)
    print(f"second: {second}")

#this function converts time into seconds
def time_to_sec(hour,minute,second):
    total_seconds = hour*3600 + minute*60 + second
    return total_seconds

#class that manages the tasks and task information
class Tasks:
    def __init__(self,master):
        #setting canvas
        self.tasks_canvas = tk.Canvas(master,width=420,bg="#C5C5C5",borderwidth=2)
        self.tasks_canvas.grid(row=4,column=0,columnspan=3,sticky="nsew")
        #setting frame in canvas
        self.tasks_frame = tk.Frame(self.tasks_canvas,bg="#C5C5C5",width=400,height=200)

        #creating the entry for user to add tasks
        tk.Label(master,text="task:").grid(row=0,column=0)
        self.user_tasks_entry = tk.Entry(master)
        self.user_tasks_entry.grid(row=0,column=1)

        #creating user to enter due date for task
        tk.Label(master,text="due date:").grid(row=1,column=0)
        self.due_date_entry = tk.Entry(master)
        self.due_date_entry.grid(row=1,column=1)

        #creating button to add task
        tk.Button(master,text="add task",command=self.add_task).grid(row=2,column=0,columnspan=2,padx=5,pady=5)

        add_scroll_bar(self.tasks_canvas,self.tasks_frame) #adds a scroll bar to the canvas

        #puts the frame into the canvas
        self.tasks_canvas.create_window((0, 0), window=self.tasks_frame, anchor="nw") 
        #creating variable for number of tasks for positioning 
        self.task_frames = {} #can be used for data saving later
        self.task_information = {} #can be used for data saving later
        self.num_of_tasks = max(self.task_frames.keys()) + 1 if self.task_frames else 0 #gets the last key in the dictionary and adds 1 to it for positioning the next task frame
    
    #checks if the user has given the inputs
    def validate_input(self):
        task = self.user_tasks_entry.get()
        due_date = self.due_date_entry.get()
        if task == "" or due_date == "":
            return False
        
        try:
            datetime.strptime(due_date, "%d/%m/%Y")  # raises ValueError if invalid
        except ValueError:
            messagebox.showerror("Error", "Due date must be in dd/mm/yyyy format (e.g. 25/12/2026).")
            return False

        return True

#function to add tasks 
    def add_task(self):
        if self.validate_input():
            #creating a frame for the task for all relevant task information
            task_frame = tk.Frame(self.tasks_frame,width=400,height=75)
            task_frame.grid(row=self.num_of_tasks,column=1,pady=5,stick="nsew") #positioning the frame in the tasks_frame
            task_frame.grid_propagate(False)#stops the frame from resizing top the widgets inside

            #adds the task information for each task added
            tk.Label(task_frame,text=tasks.user_tasks_entry.get(),wraplength=300).grid(row=0,column=0,sticky="nw",columnspan=2)#label of task 
            tk.Label(task_frame,text=f"due: {tasks.due_date_entry.get()}").grid(row=1,column=0,sticky="nw")#label of of due 
            tk.Button(task_frame, text="X",command=lambda r=self.num_of_tasks: self.delete_task(r)).grid(row=0,column=3,sticky="se") #button to remove task

            #saving information used for saving and creation/ deletion of tasks
            self.task_frames[self.num_of_tasks] = task_frame
            self.task_information[self.num_of_tasks] = {
                "task": tasks.user_tasks_entry.get(),
                "due_date": tasks.due_date_entry.get()}
            
            task_frame.columnconfigure(2,weight=1)
            self.num_of_tasks +=1 #increases by 1 for positioning
            print(self.task_information)
        else:
            messagebox.showerror("Error", "Please fill in both the task and due date fields.")

    def delete_task(self, row):
        # destroy every widget sitting in that row
        frame = self.task_frames.get(row)
        if frame is not None:
            frame.destroy()
            self.task_frames.pop(row, None)
            self.task_information.pop(row, None)
            print(self.task_information)

#class that runs the main program functions and sets the windows
class Main:
    def __init__(self,root):
        self.root = root #sets the variable root as the root which is the Tk window
        self.root.title("productivity manager")
        self.root.geometry("700x700")
        self.root.configure()

        #creating frame for title and user information
        self.top_frame = tk.Frame(self.root,height=50,bg="#d3d3d3")
        self.top_frame.grid(row=0,column=0,columnspan=3,sticky="nsew")

        #creating a frame for menu buttons
        self.button_menu_frame = tk.Frame(self.root,width=100,bg="#d3d3d3")
        self.button_menu_frame.grid(row=1,column=0,stick="nsew",rowspan=5)

        #creating the tasks grid
        self.tasks_frame = tk.Frame(self.root)
        self.tasks_frame.grid(row=1, column=1, padx=10, pady=10)
        self.tasks_frame.columnconfigure(2, weight=5)

        #creating the buttons for the menu
        self.tasks_frame_button = tk.Button(self.button_menu_frame, text="Tasks", command=lambda: self.show_frame(0)).grid(row=0,column=0,sticky="nsew",padx=5,pady=5)#button to show the tasks frame
        self.timer_frame_button = tk.Button(self.button_menu_frame, text="timer/stopwatch", command=lambda: self.show_frame(0)).grid(row=1,column=0,sticky="nsew",padx=5,pady=5)
        self.shop_frame_button = tk.Button(self.button_menu_frame, text="shop", command=lambda: self.show_frame(0)).grid(row=2,column=0,sticky="nsew",padx=5,pady=5) 
        self.logout_frame_button = tk.Button(self.button_menu_frame, text="logout", command=lambda: self.show_frame(0)).grid(row=3,column=0,sticky="nsew",padx=5,pady=5)
        self.close_button = tk.Button(self.button_menu_frame, text="Close", command=self.root.destroy).grid(row=4,column=0,sticky="nsew",padx=5,pady=5) #button to close the program
        

        

    def show_frame(self,frame):
        frames = [self.button_menu_frame,"shop,login","signup","startup"]
        frames[frame].lift()

#function to add a scroll bar to a canvas    
def add_scroll_bar(canvas,frame):
    #creating scrollbar for the canvas
    my_scrollbar = tk.Scrollbar(canvas, orient=tk.VERTICAL, command=canvas.yview)
    my_scrollbar.place(relx=1, rely=0, relheight=1, anchor="ne")
    canvas.configure(yscrollcommand=my_scrollbar.set)
    # Track scrollability
    can_scroll_verticaly = [False]
    can_scroll_horizontaly = [False]
    # Update scrollregion and scrollability flags
    #makes the scroll wheel scrollable when the content is larger than the canvas
    def update_scroll_flags():
        canvas.update_idletasks()
        bbox = canvas.bbox("all")
        if bbox:
            canvas.configure(scrollregion=bbox)
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
            content_width = bbox[2] - bbox[0]
            content_height = bbox[3] - bbox[1]
            can_scroll_verticaly[0] = content_height > canvas_height
            can_scroll_horizontaly[0] = content_width > canvas_width
    def delayed_update(event=None):
        canvas.after(50, update_scroll_flags)
    #moving the canvas
    canvas.bind("<Configure>", delayed_update)
    # Mouse wheel events
    def on_mouse_wheel(event):
        if can_scroll_verticaly[0]:
            canvas.yview_scroll(-int(event.delta / 50), "units")
    #when scrolling sideways with mouse when holding shift
    def on_shift_mouse_wheel(event):
        if can_scroll_horizontaly[0]:
            canvas.xview_scroll(-int(event.delta / 50), "units")
    #moving the canvas
    canvas.bind_all("<MouseWheel>", on_mouse_wheel)
    canvas.bind_all("<Shift-MouseWheel>", on_shift_mouse_wheel)
    frame.bind("<Configure>", delayed_update)
       

#setting up the root
root = tk.Tk()
main = Main(root)
#instantiating tasks frame
tasks = Tasks(main.tasks_frame)

root.mainloop()

