#This program is a time management app where it helps someone with time management by gamifying it.
from tkinter import*
from tkinter import messagebox
from tkcalendar import Calendar
import os 
import time
from datetime import datetime
import json
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
class Tasks_screen:
    def __init__(self,master):
        #setting canvas for tasks to go into
        self.tasks_canvas = Canvas(master,width=400,height=300,bg="#C5C5C5",borderwidth=6)
        self.tasks_canvas.grid(row=4,column=0,columnspan=3,sticky="nsew")
        #setting frame in canvas to into the canvas to put elements into
        self.tasks_frame = Frame(self.tasks_canvas,bg="#703535",width=500,height=300)

        #creating the entry for user to add tasks
        Label(master,text="task:").grid(row=1,column=0)
        self.user_tasks_entry = Entry(master)
        self.user_tasks_entry.grid(row=1,column=1,pady=5,sticky="w")
        Label(master,text="description:").grid(row=2,column=0)
        self.user_description_entry = Entry(master)
        self.user_description_entry.grid(row=2,column=1,pady=5,sticky="w")

        #creating a calendar that the user can select a date from for the due date
        self.calander = Calendar(master, selectmode = 'day', date_pattern="dd/mm/yyyy",
               year = datetime.now().year, month = datetime.now().month,
               day = datetime.now().day,font=("Arial", 10),)
        self.calander.grid(row=0,column=0,columnspan=2,sticky="nsew")

        #creating button to add task
        Button(master,text="add task",command=self.add_task).grid(row=3,column=0,columnspan=2,padx=5,pady=5)

        add_scroll_bar(self.tasks_canvas,self.tasks_frame) #adds a scroll bar to the canvas

        #puts the frame into the canvas
        self.tasks_canvas.create_window((0, 0), window=self.tasks_frame, anchor="nw") 
        #creating variable for number of tasks for positioning 
        self.task_frames = {} #can be used for data saving later saves the object not frame
        self.num_of_tasks = max(self.task_frames.keys()) + 1 if self.task_frames else 0 #gets the last key in the dictionary and adds 1 to it for positioning the next task frame

        
    #checks if the user has given the inputs
    def validate_input(self):
        task = self.user_tasks_entry.get()
        due_date = self.calander.get_date()
        current_time = time.time()

        
        
        try:#chekcs if the duedate is in the correct format 
            if task == "" or due_date == "": #checks if entries are empty and gives error message returns false for validation
                messagebox.showerror("Error", "Please fill in tasks or select a date on the calendar")
                return False
            datetime.strptime(due_date, "%d/%m/%Y")  # raises ValueError if invalid
            due_time = time.mktime(time.strptime(due_date, "%d/%m/%Y"))
            time_diff = due_time - current_time  
            print(f"current time: {current_time} due_time: {due_time} time_diff: {time_diff}")
            if time_diff < -86400:  #if the due date is in the past (1 day in seconds)
                messagebox.showerror("Error", "Due date cannot be in the past.")
                return False

        except (ValueError,OverflowError):
            messagebox.showerror("Error", "Due date must be in dd/mm/yyyy format (e.g. 25/12/2026).") 
            return False #returns false for failed validation

        return True
    
#function to add tasks 
    def add_task(self):
        if self.validate_input():
            self.task = Task(self.user_tasks_entry.get(), self.calander.get_date(), self.num_of_tasks,self.user_description_entry.get())  # Create a new instance of User_Task for each task added
            #saving information used for saving and creation/ deletion of tasks
            self.task_frames[self.num_of_tasks] = self.task
            self.num_of_tasks +=1 #increases by 1 for positioning
            self.user_tasks_entry.delete(0, END)  # Clear the entry after adding the task
            self.user_description_entry.delete(0, END)  # Clear the entry after adding the task
        else:
            pass
        
    def complete_task(self, row):
        # destroy every widget sitting in that row
        task = self.task_frames.get(row)
        print(task)
        frame = task.task_frame 
        if frame is not None:
            frame.destroy()
            self.task_frames.pop(row, None)
            # get the time of completion and compare with the time due to see if the task was completed on time or late and to calculate points to reward the user with
            print(self.calc_points(task.due_date)) 

    def calc_points(self,due):
        current_time = time.time()
        try:
            due_time = time.mktime(time.strptime(due, "%d/%m/%Y"))
            time_diff = due_time - current_time  
            x = time_diff/100
            if time_diff < 0 or time_diff > 1209600:  #if the task is completed late or the task is completed more than 2 weeks early
                return default_point_reward
            else:
                return default_point_reward + int((x/64)**1.1)  #rewarding the user with more points for completing the task early
                
        except OverflowError:
            return default_point_reward  #if the due date is too far in the future or past, just return the default point reward

#class that manages each individual user's tasks and information
class Task():
        def __init__(self,task,due_date,position,description):
            #creating a frame for the task for all relevant task information
            self.task_frame = Frame(tasks_screen.tasks_frame,width=400,height=75)
            #self.task_frame.grid_propagate(False)#stops the frame from resizing top the widgets inside
            self.task_frame.columnconfigure(0,minsize=300)
            self.task_frame.columnconfigure(2,weight=1)

            self.task = task
            self.due_date = due_date
            self.position = position
            self.description = description

            #adds the task information for each task added
            Label(self.task_frame,text=self.task,wraplength=400).grid(row=0,column=0,sticky="nw",columnspan=2)#label of task 
            Label(self.task_frame,text=f"due: {self.due_date}").grid(row=2,column=0,sticky="nw")#label of of due 
            Label(self.task_frame,text=f"description:\n {self.description}",wraplength=400,justify="left").grid(row=1,column=0,sticky="nw")#label of of due 
            Button(self.task_frame, text="X",command=lambda r=self.position: tasks_screen.complete_task(r)).grid(row=0,column=3,sticky="ne") #button to remove task
            self.task_frame.grid(row=tasks_screen.num_of_tasks,column=1,pady=5,stick="nsew") #positioning the frame in the tasks_frame

#class that manages the login screen
class Login_screen:
    def __init__(self,master):
        #setting frame in canvas
        self.main_login_frame = Frame(master,bg="blue",width=700,height=700)
        self.main_login_frame.grid(row=0,column=0)
        self.main_login_frame.grid_propagate(False)
        self.main_login_frame.columnconfigure(0,weight=1)
        self.main_login_frame.columnconfigure(2,weight=1)
        #creating login title and buttons for signup and login
        self.login_title = Label(self.main_login_frame,text="LOGIN").grid(row=0,column=1,padx=5,pady=5)
        self.login_btn = Button(self.main_login_frame,text="login",command=lambda:self.login_frame.lift()).grid(row=1,column=1,padx=5,pady=5)
        self.signup_btn = Button(self.main_login_frame,text="signup",command=lambda:self.signup_frame.lift()).grid(row=2,column=1,padx=5,pady=5)

        #frame for the login
        self.login_frame = Frame(master,bg="#FA2727",width=width-100,height=200)
        self.login_frame.grid(row=0,column=0,sticky="nsew")
        self.login_frame.columnconfigure(0,weight=1)
        self.login_frame.columnconfigure(3,weight=1)
        #creating buttons and entries for the login
        Label(self.login_frame,text="Login").grid(row=0,column=1,columnspan=2,padx=5,pady=5)
        Label(self.login_frame,text="username:").grid(row=1,column=1,padx=5,pady=5,sticky="e")
        Label(self.login_frame,text="password:").grid(row=2,column=1,padx=5,pady=5,sticky="e")
        self.login_username_entry = Entry(self.login_frame)
        self.login_username_entry.grid(row=1,column=2,padx=5,pady=5)
        self.login_password_entry = Entry(self.login_frame)
        self.login_password_entry.grid(row=2,column=2,padx=5,pady=5)
        Button(self.login_frame,text="back",command=lambda:self.main_login_frame.lift()).grid(row=3,column=1,padx=5,pady=5)
        Button(self.login_frame,text="login",command=self.login).grid(row=3,column=2,padx=5,pady=5)
        Label(self.login_frame,text="Don't have an account?").grid(row=4,column=1,columnspan=2,padx=5,pady=5)
        Button(self.login_frame,text="signup",command=lambda:self.signup_frame.lift()).grid(row=5,column=1,columnspan=2,padx=5,pady=5)

        #frame for the signup 
        self.signup_frame = Frame(master,bg="#E127FA",width=width-100,height=height-50)
        self.signup_frame.grid(row=0,column=0,sticky="nsew")
        self.signup_frame.columnconfigure(0,weight=1)
        self.signup_frame.columnconfigure(3,weight=1)
        Label(self.signup_frame,text="Signup").grid(row=0,column=1,columnspan=2,padx=5,pady=5)
        Label(self.signup_frame,text="username:").grid(row=1,column=1,padx=5,pady=5,sticky="e")
        Label(self.signup_frame,text="age:").grid(row=2,column=1,padx=5,pady=5,sticky="e")
        Label(self.signup_frame,text="password:").grid(row=3,column=1,padx=5,pady=5,sticky="e")
        Label(self.signup_frame,text="confirm password:").grid(row=4,column=1,padx=5,pady=5,sticky="e")
        self.signup_username_entry = Entry(self.signup_frame)
        self.signup_username_entry.grid(row=1,column=2,padx=5,pady=5)
        self.age_entry = Entry(self.signup_frame)
        self.age_entry.grid(row=2,column=2,padx=5,pady=5)
        self.signup_password_entry = Entry(self.signup_frame)
        self.signup_password_entry.grid(row=3,column=2,padx=5,pady=5)
        self.confirm_password_entry = Entry(self.signup_frame)
        self.confirm_password_entry.grid(row=4,column=2,padx=5,pady=5)
        Button(self.signup_frame,text="back",command=lambda:self.main_login_frame.lift()).grid(row=5,column=1,padx=5,pady=5)
        Button(self.signup_frame,text="signup",command=self.signup).grid(row=5,column=2,padx=5,pady=5)
        Label(self.signup_frame,text="Already have an account?").grid(row=6,column=1,columnspan=2,padx=5,pady=5)
        Button(self.signup_frame,text="login",command=lambda:self.login_frame.lift()).grid(row=7,column=1,columnspan=2,padx=5,pady=5)
        self.main_login_frame.lift()

    def signup(self):
        #getting the user info from the user to create an account 
        username = self.signup_username_entry.get()
        age = self.age_entry.get()
        password = self.signup_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        with open(r"userdata.json","r") as file:
            users = json.load(file)
        #chekcing if the username exists already(add when saving is created)
        #checking if age is valid (minimum age is 13+)
        try:
            if int(age)<min_age:
                messagebox.showerror("age not valid","you must be 13 or older to register an account")
            #checking that each password is the same
            elif password != confirm_password:
                messagebox.showerror("password","your passwords must match")
            elif username in users:
                messagebox.showerror("username","this username already exists")
            else:
                #save new user data
                new_user_data = {"username":username,
                "password":password,
                "points":0,
                "level":0,
                "tasks":
                    {"0":{"task_details":"",
                    "due_date":"",
                    "position":0}},
                "shop_details":
                    {"item_name":
                        {"own":False,
                        "equiped":False}}}
                with open(r"userdata.json","r") as file:
                    users = json.load(file)
                users[username] = new_user_data
                with open(r"userdata.json","w") as file:
                    json.dump(users,file,indent=4)
                get_user_data(username)

                main.username_lbl.config(text=f"username: {user.username}")
                main.level_lbl.config(text=f"level: {user.level}")
                main.points_lbl.config(text=f"points: {user.points}")
                main.next_level_lbl.config(text=f"Next lvl: {user.points}/10000")

                main.main_frame.lift()
        except ValueError:messagebox.showerror("age","your age must be an integer")

    def login(self):
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()
        #checks if username exists and gets the password if it does and if password exists
        if self.validate_login(username,password):
            main.username_lbl.config(text=f"username: {user.username}")
            main.level_lbl.config(text=f"level: {user.level}")
            main.points_lbl.config(text=f"points: {user.points}")
            main.next_level_lbl.config(text=f"Next lvl: {user.points}/10000")
            main.main_frame.lift()
        else:
            messagebox.showerror("login failuire","username or password incorrect")

    def validate_login(self,username,password):
        with open(r"userdata.json","r") as file:
            users = json.load(file)
            if username in users:
                if password == users[username]["password"]:
                    get_user_data(username)
                    return True
                else:
                    return False
            else:
                return False

#class that manages the shop screen
class Shop_screen:
    def __init__(self,master):
        Label(master,text="shop").grid(row=0,column=0)

#class that holds the user data and information for the user
class User_data:
    def __init__(self,username,password,user_data):
        self.username = username
        self.password = password
        self.points = user_data[username]["points"]
        self.level = user_data[username]["level"]
        self.tasks_info = user_data[username]["tasks"]
        self.shop_details = user_data[username]["shop_details"]

#class that runs the main program functions and sets the windows
class Main:
    def __init__(self,root):
        self.root = root #sets the variable root as the root which is the Tk window
        self.root.configure(bg="#813677")

        #creating a main frame that holds all the other freames but the login frame
        self.main_frame = Frame(self.root,height=700,width=700)
        self.main_frame.grid(column=0,row=0)
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        
        self.main_frame.grid_propagate(False)

        #creating frame for title and user information
        self.top_frame = Frame(self.main_frame,height=60,bg="#d3d3d3")
        self.top_frame.grid(row=0,column=1,columnspan=3,sticky="nsew")
        self.top_frame.grid_propagate(False) #stops the frame from resizing to the widgets inside
        self.top_frame.columnconfigure(0,weight=2)
        self.top_frame.columnconfigure(1,weight=8)
        self.top_frame.columnconfigure(2,weight=1)
        

        #creating a frame for menu buttons and image
        self.button_menu_frame = Frame(self.main_frame,width=100,bg="#d3d3d3")
        self.button_menu_frame.grid(row=0,column=0,sticky="nsew",rowspan=5)

        #creating shop frame
        self.shop_frame = Frame(self.main_frame,width=350,height=700,bg="#1076C9")
        self.shop_frame.grid(row=1,column=1,sticky="ne",rowspan=5)
        self.shop_frame.grid_propagate(False)

        #creating the tasks grid
        self.tasks_frame = Frame(self.main_frame,borderwidth=6)
        self.tasks_frame.grid(row=1, column=1,sticky="nsew")
        self.tasks_frame.columnconfigure(3, weight=5)
        self.tasks_frame.columnconfigure(2, weight=4)
        self.tasks_frame.columnconfigure(1, weight=1)

        
        #adding in the user info for top frame
        self.username_lbl = Label(self.top_frame,text="username: UsernameUsernameUsername")
        self.points_lbl = Label(self.top_frame,text="points: 1000")
        self.level_lbl = Label(self.top_frame,text="level: 3")
        self.next_level_lbl = Label(self.top_frame,text="Next lvl: 1000/10000")

        self.username_lbl.grid(row=0,column=0,sticky="w",padx=5,pady=2)
        self.points_lbl.grid(row=0,column=2,sticky="nesw",padx=5,pady=2)
        self.level_lbl.grid(row=1,column=0,sticky="w",padx=5,pady=2)
        self.next_level_lbl.grid(row=1,column=2,sticky="w",padx=5,pady=2)

        #adding frame for user image
        image_frame = Frame(self.button_menu_frame,width=100,height=100)
        image_frame.grid(row=0,column=0,pady=5)

        #creating the buttons for the menu
        self.tasks_frame_button = Button(self.button_menu_frame, text="Tasks", command=lambda: self.show_frame(0)).grid(row=1,column=0,sticky="nsew",padx=5,pady=5)#button to show the tasks frame
        self.timer_frame_button = Button(self.button_menu_frame, text="timer/stopwatch", command=lambda: self.show_frame(0)).grid(row=2,column=0,sticky="nsew",padx=5,pady=5)
        self.shop_frame_button = Button(self.button_menu_frame, text="shop", command=lambda: self.show_frame(1)).grid(row=3,column=0,sticky="nsew",padx=5,pady=5) 
        self.logout_frame_button = Button(self.button_menu_frame, text="logout", command=self.logout).grid(row=4,column=0,sticky="nsew",padx=5,pady=5)
        self.close_button = Button(self.button_menu_frame, text="Close", command=self.root.destroy).grid(row=5,column=0,sticky="nsew",padx=5,pady=5) #button to close the program


    def show_frame(self,frame):
        frames = [self.tasks_frame,self.shop_frame]
        frames[frame].lift()

    def logout(self):
        login_screen.main_login_frame.lift()
        main.tasks_frame.lift()
        login_screen.age_entry.delete(0,END)
        login_screen.signup_password_entry.delete(0,END)
        login_screen.signup_username_entry.delete(0,END)
        login_screen.login_password_entry.delete(0,END)
        login_screen.login_username_entry.delete(0,END)
        login_screen.confirm_password_entry.delete(0,END)

#function that gets user data from external file
def get_user_data(username):
    global user
    with open(r"userdata.json","r") as file:
        users = json.load(file) 
    print({users[username]["username"]})
    user = User_data(users[username]["username"],users[username]["password"],users)

#function that saves userdata to external file
def save_user_date(username):
    pass

#function to add a scroll bar to a canvas    
def add_scroll_bar(canvas,frame):
    #creating scrollbar for the canvas
    my_scrollbar = Scrollbar(canvas, orient=VERTICAL, command=canvas.yview)
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
root = Tk()
root.title("productivity manager")
root.geometry("700x700")
#variables for width and heigth of window used for sizing frames
width=700
height=700
min_age = 13
default_point_reward =10
main = Main(root)
#instantiating tasks frame
shop = Shop_screen(main.shop_frame)
tasks_screen = Tasks_screen(main.tasks_frame)
login_screen = Login_screen(main.root)

root.mainloop()

