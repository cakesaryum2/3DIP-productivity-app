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
        self.tasks_canvas = tk.Canvas(master,bg="blue",width=300,height=300)
        self.tasks_canvas.grid(row=4,column=2)
        #setting frame in canvas
        self.tasks_frame = tk.Frame(self.tasks_canvas)
        self.tasks_canvas.create_window((0, 0), window=self.tasks_frame, anchor="nw") #puts the frame into the canvas
        self.num_of_tasks = 0 #creating variable for number of tasks for positioning
        self.task_frames = {}

#function to add tasks 
    def add_task(self):
        #creating a frame for the tasks for all relevant task information
        task_frame = tk.Frame(self.tasks_frame)
        task_frame.grid(row=self.num_of_tasks,column=1)
        tk.Label(task_frame,text="test").grid(row=1,column=1)
        tk.Button(task_frame, text="X",command=lambda r=self.num_of_tasks: self.delete_task(r)).grid(row=2,column=2)
        self.task_frames[self.num_of_tasks] = task_frame
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
        self.root.title("task manager")
        self.root.geometry("700x700")

        self.tasks = Tasks(self.root)
        tk.Button(self.root,text="button",command=self.tasks.add_task).grid(row=1,column=1)


#setting up the root
root = tk.Tk()
app = Main(root)


root.mainloop()

