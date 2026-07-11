#This program is a time management app where it helps someone with time management by gamifying it.
import tkinter as tk
import os 
import time
#making sure the current directory is the same as the file
os.chdir(os.path.dirname(os.path.abspath(__file__)))
tasks = []
def adding_tasks():
    task = input("enter task: ")
    tasks.append(task)

# username = input("enter your username: ")
# password = input("enter your password: ")

# adding_tasks()
# print(tasks)

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

#class for tasks users add
class Tasks:
    def __init__(self,master):
        #setting canvas
        self.tasks_canvas = tk.Canvas(master,bg="blue",width=420)
        self.tasks_canvas.grid(row=4,column=2)
        #setting frame in canvas
        self.tasks_frame = tk.Frame(self.tasks_canvas,bg="#86FFA4",width=400,height=200)
        #creating scrollbar for the canvas
        my_scrollbar = tk.Scrollbar(self.tasks_canvas, orient=tk.VERTICAL, command=self.tasks_canvas.yview)
        my_scrollbar.place(relx=1, rely=0, relheight=1, anchor="ne")
        self.tasks_canvas.configure(yscrollcommand=my_scrollbar.set)

                # Track scrollability
        can_scroll_verticaly = [False]
        can_scroll_horizontaly = [False]

        # Update scrollregion and scrollability flags
        #makes the scroll wheel scrollable when the content is larger than the canvas
        def update_scroll_flags():
            self.tasks_canvas.update_idletasks()
            bbox = self.tasks_canvas.bbox("all")
            if bbox:
                self.tasks_canvas.configure(scrollregion=bbox)
                canvas_width = self.tasks_canvas.winfo_width()
                canvas_height = self.tasks_canvas.winfo_height()
                content_width = bbox[2] - bbox[0]
                content_height = bbox[3] - bbox[1]
                can_scroll_verticaly[0] = content_height > canvas_height
                can_scroll_horizontaly[0] = content_width > canvas_width

        def delayed_update(event=None):
            self.tasks_canvas.after(50, update_scroll_flags)
        #moving the canvas
        self.tasks_canvas.bind("<Configure>", delayed_update)

        # Mouse wheel events
        def on_mouse_wheel(event):
            if can_scroll_verticaly[0]:
                self.tasks_canvas.yview_scroll(-int(event.delta / 50), "units")
        #when crolling sideways with mouse when holding shift
        def on_shift_mouse_wheel(event):
            if can_scroll_horizontaly[0]:
                self.tasks_canvas.xview_scroll(-int(event.delta / 50), "units")
        #moving the canvas
        self.tasks_canvas.bind_all("<MouseWheel>", on_mouse_wheel)
        self.tasks_canvas.bind_all("<Shift-MouseWheel>", on_shift_mouse_wheel)
        self.tasks_frame.bind("<Configure>", delayed_update)

        #puts the frame into the canvas
        self.tasks_canvas.create_window((0, 0), window=self.tasks_frame, anchor="nw") 
        #creating variable for number of tasks for positioning
        self.num_of_tasks = 0 
        self.task_frames = {}

#function to add tasks 
    def add_task(self):
        #creating a frame for the tasks for all relevant task information
        task_frame = tk.Frame(self.tasks_frame,bg="red",width=400,height=75)
        task_frame.grid(row=self.num_of_tasks,column=1,pady=5,stick="nsew") #positioning the frame in the tasks_frame
        task_frame.grid_propagate(False)
        tk.Label(task_frame,text=app.user_tasks_entry.get(),wraplength=300).grid(row=0,column=0,sticky="nw",columnspan=2)#label of task 
        tk.Label(task_frame,text=f"due (due date)").grid(row=1,column=0,sticky="nw")#label of of due 
        tk.Button(task_frame, text="X",command=lambda r=self.num_of_tasks: self.delete_task(r)).grid(row=0,column=3,sticky="se") #button to remove task
        self.task_frames[self.num_of_tasks] = task_frame
        task_frame.columnconfigure(2,weight=1)
        self.num_of_tasks +=1 #increases by 1 for positioning
        print("he")#temp test

    def delete_task(self, row):
        # destroy every widget sitting in that row
        frame = self.task_frames.get(row)
        if frame is not None:
            frame.destroy()


class Main:
    def __init__(self,root):
        self.root = root #sets the variable root as the root which is the Tk window
        self.root.title("productivity manager")
        self.root.geometry("700x700")

        self.user_tasks_entry = tk.Entry(self.root)
        self.user_tasks_entry.grid(row=0,column=1)
        #creating the frames and canvas for label creation
        self.tasks = Tasks(self.root)
        tk.Button(self.root,text="button",command=self.tasks.add_task).grid(row=1,column=1)


#setting up the root
root = tk.Tk()
app = Main(root)


root.mainloop()

