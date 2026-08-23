#This program is a time management app where it helps someone with time management by gamifying it.
from tkinter import*
from tkinter import messagebox
from tkcalendar import Calendar
import os 
import time
from datetime import datetime
import json
from PIL import Image, ImageTk
import random
#making sure the current directory is the same as the file
os.chdir(os.path.dirname(os.path.abspath(__file__)))
#class that manages the tasks and task information
class TasksScreen:
    def __init__(self,master):
        self.task_frames = {} #used for saving each task object
        self.create_task_screen(master)
    def create_task_screen(self,master):
        #setting canvas for tasks to go into
        self.tasks_canvas = Canvas(master,width=400,height=250,bg=secondary_colour,borderwidth=6)
        self.tasks_canvas.grid(row=4,column=0,columnspan=3,sticky="nsew")
        #setting frame in canvas to into the canvas to put elements into
        self.tasks_frame = Frame(self.tasks_canvas,bg=secondary_colour,width=500,height=250)

        #creating the entry for user to add tasks
        Label(master,text="task:",bg=main_colour,fg=text_colour).grid(row=1,column=0) 
        self.user_tasks_entry = Entry(master)
        self.user_tasks_entry.grid(row=1,column=1,pady=5,sticky="w")
        Label(master,text="description:",bg=main_colour,fg=text_colour).grid(row=2,column=0)
        self.user_description_entry = Entry(master)
        self.user_description_entry.grid(row=2,column=1,pady=5,sticky="w")

        #creating a calendar that the user can select a date from for the due date
        self.calander = Calendar(master, selectmode = 'day', date_pattern="dd/mm/yyyy",
               year = datetime.now().year, month = datetime.now().month,
               day = datetime.now().day,font=("Arial", 10),)
        self.calander.grid(row=0,column=0,columnspan=2,sticky="nsew")

        #creating button to add task
        Button(master,text="add task",command=self.add_task,bg=main_colour,fg=text_colour).grid(row=3,column=0,columnspan=2,padx=5,pady=5)
        #button to remove all tasks
        Button(master,text="clear all tasks",command=self.clear_task_data,bg=main_colour,fg=text_colour).grid(row=5,column=0,padx=5,pady=5)
        add_scroll_bar(self.tasks_canvas,self.tasks_frame) #adds a scroll bar to the canvas
        #puts the frame into the canvas
        self.tasks_canvas.create_window((0, 0), window=self.tasks_frame, anchor="nw") 

        
    #creates the tasks saved from file
    def display_existing_tasks(self): 
         self.num_of_tasks = max(self.task_frames.keys()) + 1 if self.task_frames else 0 #gets the last key in the dictionary and adds 1 to it for positioning the next task frame       
         for task_information in user.tasks_info.values():
            self.task = Task(task_information["task_details"], task_information["due_date"], task_information["position"], task_information["description"])
            self.task_frames[task_information["position"]] = self.task

    #checks if the user has given the inputs
    def validate_input(self):
        task = self.user_tasks_entry.get()
        due_date = self.calander.get_date()
        current_time = time.time()

        try:#checks if the duedate is in the correct format 
            if task == "" or due_date == "": #checks if entries are empty and gives error message returns false for validation
                messagebox.showerror("Error", "Please fill in tasks or select a date on the calendar")
                return False
            datetime.strptime(due_date, "%d/%m/%Y")  # raises ValueError if invalid
            due_time = time.mktime(time.strptime(due_date, "%d/%m/%Y"))
            time_diff = due_time - current_time  
            if time_diff < -86400:  #if the due date is in the past (1 day in seconds)
                messagebox.showerror("Error", "Due date cannot be in the past.")
                return False
        except (ValueError,OverflowError):
            messagebox.showerror("Error", "Due date must be in dd/mm/yyyy format (e.g. 25/12/2026).") 
            return False 
        return True
    
#function to add tasks 
    def add_task(self):
        if self.validate_input():
            self.num_of_tasks = max(self.task_frames.keys()) + 1 if self.task_frames else 0 #gets the last key in the dictionary and adds 1 to it for positioning the next task frame
            self.task = Task(self.user_tasks_entry.get(), self.calander.get_date(), self.num_of_tasks,self.user_description_entry.get())  # Create a new instance of User_Task for each task added
            #saving information used for saving and creation/ deletion of tasks
            self.task_frames[self.num_of_tasks] = self.task
            self.num_of_tasks +=1 #increases by 1 for positioning
            self.user_tasks_entry.delete(0, END)  # Clear the entry after adding the task
            self.user_description_entry.delete(0, END)  
            self.save_tasks()
        else:
            pass

#function that removes task from task screen
    def remove_task(self, row):
        task = self.task_frames.get(row)
        frame = task.task_frame 
        if frame is not None:
            frame.destroy()
            self.task_frames.pop(row, None)

#function that removes and completes tasks from tasks screen (rewards users)           
    def complete_task(self, row):
        # destroy every widget sitting in that row
        task = self.task_frames.get(row)
        self.remove_task(row)
        # get the time of completion and compare with the time due to see if the task was completed on time or late and to calculate points to reward the user with
        user.points += self.calc_points(task.due_date)
        user.exp += self.calc_points(task.due_date)
        main.points_lbl.config(text=f"points: {user.points}")
        main.update_level()
        tip_frame = Frame(main.tasks_frame,bg=secondary_colour,width=250,height=80)
        tip_frame.grid(row=0,column=2,columnspan=3,sticky="ne")
        tip_frame.pack_propagate(False)
        Label(tip_frame,text="productivty tips",bg=secondary_colour,fg=text_colour).pack()
        Label(tip_frame,text=tip_messages[random.randint(0,(len(tip_messages))-1)],justify="left",bg=secondary_colour,fg=text_colour,wraplength=200).pack(side="left")
        tip_frame.after(2000,tip_frame.destroy)

#function that calculates the points rewarded
    def calc_points(self,due):
        current_time = time.time()
        try:
            due_time = time.mktime(time.strptime(due, "%d/%m/%Y"))
            time_diff = due_time - current_time  
            x = time_diff/100 #reduces the size of number so calculation wont become as large
            if time_diff < 0 or time_diff > HPRT:  #if the task is completed late or the task is completed more than 2 weeks early
                return DEFAULT_POINT_REWARD
            else:
                return DEFAULT_POINT_REWARD + int((x/64)**1.1)  #rewarding the user with more points for completing the task early
        except OverflowError:
            return DEFAULT_POINT_REWARD  #if the due date is too far in the future or past, just return the default point reward

#function that clears all tasks from tasks screen without removing task data 
    def clear_tasks(self):
        for position in self.task_frames.keys():
            task = self.task_frames.get(position)
            frame = task.task_frame 
            if frame is not None:
                frame.destroy()

#function that clears all tasks data and tasks from task screen
    def clear_task_data(self):
        self.clear_tasks()
        self.task_frames.clear()

#function that saves tasks to user information for data saving
    def save_tasks(self):
        task_information = {}
        for t in self.task_frames.values():
            task_information[t.position] = {
                "task_details": t.task,
                "due_date": t.due_date,
                "description": t.description,
                "position": t.position}
        user.tasks_info = task_information
#class that manages each individual user's tasks and information
class Task:
        def __init__(self,task,due_date,position,description):
            #creating a frame for the task for all relevant task information
            self.task_frame = Frame(tasks_screen.tasks_frame,width=400,height=75,bg=main_colour)
            #self.task_frame.grid_propagate(False)#stops the frame from resizing top the widgets inside
            self.task_frame.columnconfigure(0,minsize=300)
            self.task_frame.columnconfigure(2,weight=1)
            self.task = task
            self.due_date = due_date
            self.position = position
            self.description = description

            #adds the task information for each task added
            Label(self.task_frame,text=self.task,wraplength=400,bg=main_colour,fg=text_colour).grid(row=0,column=0,sticky="nw",columnspan=2)#label of task 
            Label(self.task_frame,text=f"due: {self.due_date}",bg=main_colour,fg=text_colour).grid(row=2,column=0,sticky="nw")#label of of due 
            Label(self.task_frame,text=f"description:\n{self.description}",wraplength=400,justify="left",bg=main_colour,fg=text_colour).grid(row=1,column=0,sticky="nw")#label of of due 
            Button(self.task_frame, text="complete",command=lambda r=self.position: tasks_screen.complete_task(r),bg=main_colour,fg=text_colour).grid(row=0,column=3,sticky="ne") #button to remove task
            Button(self.task_frame, text="remove",command=lambda r=self.position: tasks_screen.remove_task(r),bg=main_colour,fg=text_colour).grid(row=1,column=3,sticky="ne") #button to remove task
            self.task_frame.grid(row=self.position,column=1,pady=5,stick="nsew") #positioning the frame in the tasks_frame

#class that manages the login screen
class LoginScreen:
    def __init__(self,master):
        #setting frame in canvas
        self.main_login_frame = Frame(master,bg=main_colour,width=700,height=700)
        self.main_login_frame.grid(row=0,column=0)
        self.main_login_frame.grid_propagate(False)
        self.main_login_frame.columnconfigure(0,weight=1)
        self.main_login_frame.columnconfigure(2,weight=1)
        #creating login title and buttons for signup and login
        self.login_title = Label(self.main_login_frame,text="Welcome to the productivty app",bg=main_colour,fg=text_colour,font = ("Arial",20)).grid(row=0,column=1,padx=5,pady=5)
        self.login_btn = Button(self.main_login_frame,text="login",command=lambda:self.login_frame.lift(),bg=main_colour,fg=text_colour,font = ("Arial",15)).grid(row=1,column=1,padx=5,pady=5)
        self.signup_btn = Button(self.main_login_frame,text="signup",command=lambda:self.signup_frame.lift(),bg=main_colour,fg=text_colour,font = ("Arial",15)).grid(row=2,column=1,padx=5,pady=5)
        Button(self.main_login_frame,text="close",command=root.destroy,bg=main_colour,fg=text_colour,font = ("Arial",15)).grid(row=3,column=1,padx=5,pady=5)

        #frame for the login
        self.login_frame = Frame(master,bg=main_colour,width=600,height=200)
        self.login_frame.grid(row=0,column=0,sticky="nsew")
        self.login_frame.columnconfigure(0,weight=1)
        self.login_frame.columnconfigure(3,weight=1)
        #creating buttons and entries for the login
        Label(self.login_frame,text="Login",bg=main_colour,fg=text_colour,font = ("Arial",20)).grid(row=0,column=1,columnspan=2,padx=5,pady=5)
        Label(self.login_frame,text="username:",bg=main_colour,fg=text_colour,font = ("Arial",10)).grid(row=1,column=1,padx=5,pady=5,sticky="e")
        Label(self.login_frame,text="password:",bg=main_colour,fg=text_colour,font = ("Arial",10)).grid(row=2,column=1,padx=5,pady=5,sticky="e")
        self.login_username_entry = Entry(self.login_frame)
        self.login_username_entry.grid(row=1,column=2,padx=5,pady=5)
        self.login_password_entry = Entry(self.login_frame,show="*")
        self.login_password_entry.grid(row=2,column=2,padx=5,pady=5)
        Button(self.login_frame,text="back",command=lambda:self.main_login_frame.lift(),bg=main_colour,fg=text_colour,font = ("Arial",10)).grid(row=3,column=1,padx=5,pady=5)
        Button(self.login_frame,text="login",command=self.login,bg=main_colour,fg=text_colour,font = ("Arial",10)).grid(row=3,column=2,padx=5,pady=5)
        Label(self.login_frame,text="Don't have an account?",bg=main_colour,fg=text_colour).grid(row=4,column=1,columnspan=2,padx=5,pady=5)
        Button(self.login_frame,text="signup",command=lambda:self.signup_frame.lift(),bg=main_colour,fg=text_colour).grid(row=5,column=1,columnspan=2,padx=5,pady=5)

        #frame for the signup 
        self.signup_frame = Frame(master,bg=main_colour,width=600,height=650)
        self.signup_frame.grid(row=0,column=0,sticky="nsew")
        self.signup_frame.columnconfigure(0,weight=1)
        self.signup_frame.columnconfigure(3,weight=1)
        Label(self.signup_frame,text="Signup",bg=main_colour,fg=text_colour,font = ("Arial",20)).grid(row=0,column=1,columnspan=2,padx=5,pady=5)
        Label(self.signup_frame,text="username:",bg=main_colour,fg=text_colour,font = ("Arial",10)).grid(row=1,column=1,padx=5,pady=5,sticky="e")
        Label(self.signup_frame,text="age:",bg=main_colour,fg=text_colour,font = ("Arial",10)).grid(row=2,column=1,padx=5,pady=5,sticky="e")
        Label(self.signup_frame,text="password:",bg=main_colour,fg=text_colour,font = ("Arial",10)).grid(row=3,column=1,padx=5,pady=5,sticky="e")
        Label(self.signup_frame,text="confirm password:",bg=main_colour,fg=text_colour,font = ("Arial",10)).grid(row=4,column=1,padx=5,pady=5,sticky="e")
        self.signup_username_entry = Entry(self.signup_frame)
        self.signup_username_entry.grid(row=1,column=2,padx=5,pady=5)
        self.age_entry = Entry(self.signup_frame)
        self.age_entry.grid(row=2,column=2,padx=5,pady=5)
        self.signup_password_entry = Entry(self.signup_frame,show="*")
        self.signup_password_entry.grid(row=3,column=2,padx=5,pady=5)
        self.confirm_password_entry = Entry(self.signup_frame,show="*")
        self.confirm_password_entry.grid(row=4,column=2,padx=5,pady=5)
        Button(self.signup_frame,text="back",command=lambda:self.main_login_frame.lift(),bg=main_colour,fg=text_colour,font = ("Arial",10)).grid(row=5,column=1,padx=5,pady=5)
        Button(self.signup_frame,text="signup",command=self.signup,bg=main_colour,fg=text_colour,font = ("Arial",10)).grid(row=5,column=2,padx=5,pady=5)
        Label(self.signup_frame,text="Already have an account?",bg=main_colour,fg=text_colour).grid(row=6,column=1,columnspan=2,padx=5,pady=5)
        Button(self.signup_frame,text="login",command=lambda:self.login_frame.lift(),bg=main_colour,fg=text_colour).grid(row=7,column=1,columnspan=2,padx=5,pady=5)
        self.main_login_frame.lift()

    def signup(self):
        #getting the user info from the user to create an account 
        username = self.signup_username_entry.get()
        age = self.age_entry.get()
        password = self.signup_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        with open(r"userdata.json","r") as file:
            users = json.load(file)
        #checking if inputs are valid  (minimum age is 13+)
        try:
            if int(age)<MIN_AGE:
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
                "exp": 0,
                "tasks": {},
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
                
                #creating the new profile gui
                img = Image.open(DEFAULT_PROFILE)
                img = img.resize((75, 75)) 
                self.image = ImageTk.PhotoImage(img)
                main.image_label.config(image=self.image)
                main.update_user_info_display()
                shop_screen.create_items() #creates item in the shop
                main.main_frame.lift()
        except ValueError:messagebox.showerror("age","your age must be an integer")

    def login(self):
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()
        #checks if username exists and gets the password if it does and if password exists
        if self.validate_login(username,password):
            main.update_user_info_display() #updates user information
            tasks_screen.display_existing_tasks()  # Display existing tasks after login
            img = Image.open(DEFAULT_PROFILE)
            img = img.resize((75, 75)) 
            self.image = ImageTk.PhotoImage(img)
            main.image_label.config(image=self.image)
            shop_screen.create_items() #creates items in the shop
            shop_screen.apply_theme() #applies any themes the user has
            main.main_frame.lift()
        else: messagebox.showerror("login failuire","username or password incorrect")

    def validate_login(self,username,password):
        with open(r"userdata.json","r") as file:
            users = json.load(file)
            if username in users:
                if password == users[username]["password"]:
                    get_user_data(username)
                    return True
                else: return False
            else: return False

#class that manages the shop screen
class ShopScreen:
    def __init__(self,master):
        self.items = {}
        self.create_shop_screen(master)
    #function created all elements for the shop screen
    def create_shop_screen(self,master):
        Label(master,text="shop",font=("Arial", 20),bg=secondary_colour,fg=text_colour).grid(row=0,column=0,columnspan=2)
        self.shop_canvas = Canvas(master,width=320,height=500,bg=secondary_colour)
        self.shop_canvas.grid(row=2,column=0,columnspan=3,sticky="nsew",pady=5,padx=5)
        self.shop_frame = Frame(self.shop_canvas,bg=secondary_colour,width=320,height=500)
        self.shop_canvas.create_window((0, 0), window=self.shop_frame, anchor="nw") 
        Button(master,text="close",command=lambda: main.show_frame(0),bg=main_colour,fg=text_colour).grid(row=3,column=0,sticky="sw")
        add_scroll_bar(self.shop_canvas,self.shop_frame)
#function that creates each shop item
    def create_items(self):
        with open("shopdata.json","r") as file:
            shop_data = json.load(file)
        for item_data in shop_data:
            item = Items(item_data["item"],item_data["price"],item_data["description"],item_data["type"],display=item_data["display"])
            self.items[item_data["item"]] = item
#function that clear shops items
    def clear_shop(self):
        for item in self.shop_frame.winfo_children():#gets all children from frame
            item.destroy() 
        self.items.clear()#clear the shop data
#function that applies the theme equiped from the shop
    def apply_theme(self):
        for x in main.shop_frame.winfo_children(): #removing all widgets
            x.destroy()
        for x in main.tasks_frame.winfo_children():
            x.destroy()
        for x in main.main_frame.winfo_children():
            x.destroy()
        shop_screen.items.clear() #clearing memeory
        tasks_screen.task_frames.clear()
        main.create_main_frames()#recreating the widgets with new colour
        tasks_screen.create_task_screen(main.tasks_frame) 
        tasks_screen.display_existing_tasks()
        main.update_user_info_display()
        shop_screen.create_shop_screen(main.shop_frame) 
        shop_screen.create_items()
         
#class that handles each shop item
class Items:
    def __init__(self,item_name,price,description,type,display):
        self.item_name = item_name
        self.price = price
        self.description = description 
        self.type = type
        self.display = display #displays preview of item, either image for profile or colour for colour scheme
        try:
            self.own = user.shop_details[item_name]["own"]
            self.equiped = user.shop_details[item_name]["equiped"]
        except KeyError:
            user.shop_details[item_name] = {
                "own": False,
                "equiped": False}
            self.own = False
            self.equiped = False
        self.item_frame = Frame(shop_screen.shop_frame,width = 300,height = 100,bg=main_colour)
        self.item_frame.columnconfigure(3,weight=1)
        Label(self.item_frame,text=self.item_name,bg=main_colour,fg=text_colour).grid(row=0,column=1,sticky="w")
        Label(self.item_frame,text=self.description,wraplength=150,justify="left",bg=main_colour,fg=text_colour).grid(row=1,column=1,sticky="w")
        Label(self.item_frame,text=f"cost: {self.price}",bg=main_colour,fg=text_colour).grid(row=2,column=1,sticky="w")
        display_frame = Frame(self.item_frame,width=75,height=75)
        display_frame.grid(row=0,rowspan=3,column=0)
        if self.type == "colour":
            display_frame.config(bg=display[0]) #display 0 gets display colour
        elif self.type == "profile":
            img = Image.open(self.display)
            img = img.resize((75, 75)) #resizing image to fit
            image = ImageTk.PhotoImage(img)
            label = Label(display_frame,image=image)
            label.image = image
            label.pack()
        self.item_btn = Button(self.item_frame,text="",bg=main_colour,fg=text_colour)
        self.item_btn.grid(row=1,rowspan=3,column=3,sticky="e")
        self.check_item()
        self.item_frame.pack(pady=5,padx=2)
        self.item_frame.grid_propagate(False)
#funciton that checks the items state for button
    def check_item(self):
        if self.own:
            if self.equiped:
                self.equip_item(True)
                self.item_btn.config(text = "unequip",command=self.unequip_item)
            else:
                self.item_btn.config(text = "equip",command=self.equip_item)
        else:
            self.item_btn.config(text = "buy",command=self.buy_item)
    def buy_item(self):
        #reduce points and update, change buy to equip
        if user.points >= self.price:
            user.points = user.points - self.price
            main.points_lbl.config(text=f"points: {user.points}")
            self.item_btn.config(text = "equip",command=self.equip_item)
            user.shop_details[self.item_name]["own"] = True
        else: messagebox.showerror("not enough points","You do not have enough points to afford this item")
#function that equips the equipped item
    def equip_item(self,equiped=False):
        #apply item and change to unequip
        self.item_btn.config(text = "unequip",command=self.unequip_item)
        user.shop_details[self.item_name]["equiped"] = True
        self.equiped=True
        if self.type == "profile":
            for i in shop_screen.items.values(): #unequips equipped item other than the one user has equipped
                if i.item_name != self.item_name and i.equiped == True and i.own == True:
                    if self.type and i.type == "profile":
                        i.equiped = False
                        user.shop_details[i.item_name]["equiped"] = False
                        i.item_btn.config(text = "equip",command=i.equip_item)
            img = Image.open(self.display)#displays image
            img = img.resize((75, 75)) #resizing image to fit
            self.image = ImageTk.PhotoImage(img)
            main.image_label.config(image=self.image)
        if self.type == "colour":
            for i in shop_screen.items.values():#unequips equipped item other than the one user has equipped
                if i.item_name != self.item_name and i.equiped == True and i.own == True:
                    if self.type and i.type == "colour":
                        i.equiped = False
                        user.shop_details[i.item_name]["equiped"] = False
                        i.item_btn.config(text = "equip",command=i.equip_item)
            main.save_user_data()
            #updates colours
            global main_colour,secondary_colour,text_colour
            main_colour = self.display[1]
            secondary_colour = self.display[2]
            text_colour = self.display[3]
            if not equiped:
                shop_screen.apply_theme()
    def unequip_item(self):
        #removes item and defaults if nothing else is applied
        self.item_btn.config(text = "equip",command=self.equip_item)
        user.shop_details[self.item_name]["equiped"] = False
        self.equiped = False
        if self.type == "profile":
            img = Image.open(DEFAULT_PROFILE)
            img = img.resize((75, 75)) #resizing image to fit
            self.image = ImageTk.PhotoImage(img)
            main.image_label.config(image=self.image) 
        if self.type == "colour":
            #changing colours back to default
            global main_colour,secondary_colour,text_colour
            main_colour = DEFAULT_MAIN_COLOUR
            secondary_colour = DEFAULT_SECONDARY_COLOUR
            text_colour = "#000000"
            shop_screen.apply_theme()

#class that holds the user data and information for the user
class UserData:
    def __init__(self,username,password,user_data):
        self.username = username
        self.password = password
        self.points = user_data[username]["points"]
        self.exp = user_data[username]["exp"]
        self.level = user_data[username]["level"]
        self.tasks_info = user_data[username]["tasks"]
        self.shop_details = user_data[username]["shop_details"]

class StopwatchTimer: #class to create a stopwatch window for each stopwatch created
    def __init__(self, master): #master takes the self.root which is the window for the main app function 
        self.window = Toplevel(master,bg=main_colour) # Create a new window for each stopwatch top level allows us to have multiple stopwatches without them interfering with each other
        self.window.title("Stopwatch/timer")
        self.window.geometry("250x250")
        self.window.columnconfigure((0,4),weight=1)
        vmcd = self.window.register(self.limit_input_length)#register validation function
        self.stopwatch_running = False #variable to track if the stopwatch/timer is running or not, used to control the flow of the program and prevent multiple timers from running at the same time
        self.timer_running = False 
        self.elapsed_time = 0.0
        self.start_time = 0.0
        self.timer_remaining = 0.0

        #timer gui
        self.timer_frame = Frame(self.window,bg=main_colour,width=250,height=200)
        self.timer_frame.grid(row=1,column=1,columnspan=2,pady=5,sticky="nsew")
        self.timer_frame.grid_propagate(False)
        self.timer_frame.columnconfigure((0,7),weight=1)
        Label(self.timer_frame, text="timer", font=("Arial", 17),justify="center",pady=10,bg=main_colour,fg=text_colour).grid(row=0,column=1,columnspan=6)
        self.timer_label = Label(self.timer_frame, text="00:00:00", font=("Arial", 25),justify="center",bg=main_colour,fg=text_colour)
        self.timer_label.grid(row=2,column=1,columnspan=6)
        Label(self.timer_frame,text="hour",bg=main_colour,fg=text_colour).grid(row=1,column=1)
        self.hour_entry = Entry(self.timer_frame,width=3, validate="key",validatecommand=(vmcd,"%P"))
        self.hour_entry.grid(row=1,column=2)
        Label(self.timer_frame,text="min",bg=main_colour,fg=text_colour).grid(row=1,column=3)
        self.minute_entry = Entry(self.timer_frame,width=3, validate="key",validatecommand=(vmcd,"%P"))
        self.minute_entry.grid(row=1,column=4)
        Label(self.timer_frame,text="sec",bg=main_colour,fg=text_colour).grid(row=1,column=5)
        self.second_entry = Entry(self.timer_frame,width=3, validate="key",validatecommand=(vmcd,"%P"))
        self.second_entry.grid(row=1,column=6)
        Button(self.timer_frame, text="Start", command=self.start_timer,bg=main_colour,fg=text_colour).grid(row=3,column=2,pady=5)
        Button(self.timer_frame, text="Stop", command=self.stop_timer,bg=main_colour,fg=text_colour).grid(row=3,column=3,pady=5)
        Button(self.timer_frame, text="Reset", command=self.reset_timer,bg=main_colour,fg=text_colour).grid(row=3,column=4,pady=5)

        #stopwatch gui
        self.stopwatch_frame = Frame(self.window,bg=main_colour,width=250,height=200)
        self.stopwatch_frame.grid(row=1,column=1,columnspan=3,pady=5,sticky="nsew")
        self.stopwatch_frame.grid_propagate(False)
        self.stopwatch_frame.columnconfigure((0,4),weight=1)
        Label(self.stopwatch_frame, text="stopwatch", font=("Arial", 17),justify="center",pady=10,bg=main_colour,fg=text_colour).grid(row=0,column=1,columnspan=3)
        self.stopwatch_label = Label(self.stopwatch_frame, text="00:00:00", font=("Arial", 25),justify="center",bg=main_colour,fg=text_colour)
        self.stopwatch_label.grid(row=1,column=1,columnspan=3)
        Button(self.stopwatch_frame, text="Start", command=lambda:self.start_stopwatch(self.update_stopwatch),bg=main_colour,fg=text_colour).grid(row=2,column=1,pady=5)
        Button(self.stopwatch_frame, text="Stop", command=self.stop_stopwatch,bg=main_colour,fg=text_colour).grid(row=2,column=2,pady=5)
        Button(self.stopwatch_frame, text="Reset", command=self.reset_stopwatch,bg=main_colour,fg=text_colour).grid(row=2,column=3,pady=5)
        #buttons to switch stopwatch to timer
        Button(self.window, text="stopwatch", command=lambda:self.stopwatch_frame.lift(),bg=main_colour,fg=text_colour).grid(row=0,column=1,pady=5,sticky="e")
        Button(self.window, text="timer", command=lambda:self.timer_frame.lift(),bg=main_colour,fg=text_colour).grid(row=0,column=2,pady=5,sticky="w")

    # Function to validate input length
    def limit_input_length(self,input_text):
        if len(input_text) > 3:
            return False
        return True

    def update_stopwatch(self):
        if self.stopwatch_running:
            # Calculate current elapsed time
            current_elapsed = time.time() - self.start_time + self.elapsed_time
            self.display_stopwatch(current_elapsed)
            # Schedule the next update in 100ms (0.1 seconds)
            self.window.after(100, self.update_stopwatch)

    def display_stopwatch(self, total_seconds):
        hours = total_seconds/3600
        hour = int(hours)
        minutes = (hours-hour)*60
        minute = int(minutes)
        seconds = (minutes-minute)*60
        second = int(seconds)
        self.stopwatch_label.config(text=f"{int(hour):02}:{int(minute):02}:{second:02}")

    def start_stopwatch(self,function):
        if not self.stopwatch_running:
            self.start_time = time.time()
            self.stopwatch_running = True
            function()
        
    def stop_stopwatch(self):
        if self.stopwatch_running:
            self.elapsed_time += time.time() - self.start_time
            self.stopwatch_running = False  
            
    def reset_stopwatch(self):
        self.stopwatch_running = False
        self.timer_running = False
        self.elapsed_time = 0.0
        self.stopwatch_label.config(text="00:00:00")

    def start_timer(self):
        if self.timer_running:
            return  # already running, ignore extra clicks
        # If nothing left running from a previous stop, read fresh values from entries
        if self.timer_remaining <= 0:
            try:
                h = int(self.hour_entry.get() or 0) #gets time if empty set to 0
                m = int(self.minute_entry.get() or 0)
                s = int(self.second_entry.get() or 0)
                self.hour_entry.delete(0,END)
                self.minute_entry.delete(0,END)
                self.second_entry.delete(0,END)
            except ValueError:
                messagebox.showerror("Invalid input", "Please enter whole numbers.")
                return
            total = h * 3600 + m * 60 + s
            if total <= 0: #gets total seconds
                messagebox.showerror("Invalid input", "Please enter a time greater than zero.")
                return
            self.timer_remaining = total
        self.timer_end_time = time.time() + self.timer_remaining
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if not self.timer_running:
            return
        remaining = self.timer_end_time - time.time()
        if remaining <= 0:
            self.timer_remaining = 0
            self.timer_running = False
            self.display_timer(0)
            messagebox.showinfo("Time's up!", "Your timer has finished.")
            return
        self.timer_remaining = remaining
        self.display_timer(remaining)
        self.window.after(200, self.update_timer)

    def display_timer(self, seconds):
        hours = seconds/3600
        hour = int(hours)
        minutes = (hours-hour)*60
        minute = int(minutes)
        seconds = (minutes-minute)*60
        second = int(seconds)
        self.timer_label.config(text=f"{int(hour):02}:{int(minute):02}:{int(second):02}")

    def stop_timer(self):
        #pauses the timer
        if self.timer_running:
            self.timer_remaining = self.timer_end_time - time.time()
            self.timer_running = False

    def reset_timer(self):
        self.timer_running = False
        self.timer_remaining = 0.0
        self.timer_label.config(text="00:00:00")

#class that runs the main program functions and sets the windows
class Main:
    def __init__(self,root):
        self.root = root #sets the variable root as the root which is the Tk window

        #creating a main frame that holds all the other freames but the login frame
        self.main_frame = Frame(self.root,height=700,width=700,bg=main_colour)
        self.main_frame.grid(column=0,row=0)
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.grid_propagate(False)
        self.create_main_frames()
#function that creates all the main items
    def create_main_frames(self):
        #creating frame for title and user information
        self.top_frame = Frame(self.main_frame,height=60,bg=secondary_colour)
        self.top_frame.grid(row=0,column=1,columnspan=3,sticky="nsew")
        self.top_frame.grid_propagate(False) #stops the frame from resizing to the widgets inside
        self.top_frame.columnconfigure(0,weight=2)
        self.top_frame.columnconfigure(1,weight=8)
        self.top_frame.columnconfigure(2,weight=1)
        
        #creating a frame for menu buttons and image
        self.button_menu_frame = Frame(self.main_frame,width=100,bg=secondary_colour)
        self.button_menu_frame.grid(row=0,column=0,sticky="nsew",rowspan=5)

        #creating shop frame
        self.shop_frame = Frame(self.main_frame,width=350,height=700,bg=secondary_colour,highlightbackground=main_colour,highlightthickness=3,borderwidth=5)
        self.shop_frame.grid(row=1,column=1,sticky="ne",rowspan=5)
        self.shop_frame.grid_propagate(False)

        #creating the tasks grid
        self.tasks_frame = Frame(self.main_frame,borderwidth=6,bg=main_colour)
        self.tasks_frame.grid(row=1, column=1,sticky="nsew")
        self.tasks_frame.columnconfigure(3, weight=5)
        self.tasks_frame.columnconfigure(2, weight=4)
        self.tasks_frame.columnconfigure(1, weight=1)

        #adding in the user info for top frame
        self.username_lbl = Label(self.top_frame,text="username: ",bg=secondary_colour,fg=text_colour)
        self.points_lbl = Label(self.top_frame,text="points: ",bg=secondary_colour,fg=text_colour)
        self.level_lbl = Label(self.top_frame,text="level: ",bg=secondary_colour,fg=text_colour)
        self.next_level_lbl = Label(self.top_frame,text="Next lvl: ",bg=secondary_colour,fg=text_colour)
        self.username_lbl.grid(row=0,column=0,sticky="w",padx=5,pady=2)
        self.points_lbl.grid(row=0,column=2,sticky="nesw",padx=5,pady=2)
        self.level_lbl.grid(row=1,column=0,sticky="w",padx=5,pady=2)
        self.next_level_lbl.grid(row=1,column=2,sticky="w",padx=5,pady=2)

        #adding frame for user image
        image_frame = Frame(self.button_menu_frame,width=100,height=100)
        image_frame.grid(row=0,column=0,pady=5)
        self.image_label = Label(image_frame)
        self.image_label.pack()

        #creating the buttons for the menu
        self.tasks_frame_button = Button(self.button_menu_frame, text="Tasks", command=lambda: self.show_frame(0),bg=main_colour,fg=text_colour).grid(row=1,column=0,sticky="nsew",padx=5,pady=5)#button to show the tasks frame
        self.timer_frame_button = Button(self.button_menu_frame, text="timer/stopwatch", command=lambda: StopwatchTimer(self.root),bg=main_colour,fg=text_colour).grid(row=2,column=0,sticky="nsew",padx=5,pady=5)
        self.shop_frame_button = Button(self.button_menu_frame, text="shop", command=lambda: self.show_frame(1),bg=main_colour,fg=text_colour).grid(row=3,column=0,sticky="nsew",padx=5,pady=5) 
        self.logout_frame_button = Button(self.button_menu_frame, text="logout", command=self.logout,bg=main_colour,fg=text_colour).grid(row=4,column=0,sticky="nsew",padx=5,pady=5)
        self.close_button = Button(self.button_menu_frame, text="Close", command=self.close_program,bg=main_colour,fg=text_colour).grid(row=5,column=0,sticky="nsew",padx=5,pady=5) #button to close the program

    #shows frame
    def show_frame(self,frame):
        frames = [self.tasks_frame,self.shop_frame]
        frames[frame].lift()
#function that logs out of the account
    def logout(self):
        login_screen.main_login_frame.lift()
        main.tasks_frame.lift()
        login_screen.age_entry.delete(0,END)
        login_screen.signup_password_entry.delete(0,END)
        login_screen.signup_username_entry.delete(0,END)
        login_screen.login_password_entry.delete(0,END)
        login_screen.login_username_entry.delete(0,END)
        login_screen.confirm_password_entry.delete(0,END)
        global main_colour,secondary_colour,text_colour
        main_colour = DEFAULT_MAIN_COLOUR
        secondary_colour = DEFAULT_SECONDARY_COLOUR
        text_colour = "#000000"
        self.save_user_data()#save user data when loggin out
        tasks_screen.clear_task_data() #clears tasks when loggin out
        shop_screen.clear_shop() #clears all tkinter widgets form the shop
        
#saves user data to an external file
    def save_user_data(self):
        tasks_screen.save_tasks()  # Save tasks before saving user data
        with open(r"userdata.json","r") as file:
            users = json.load(file)
        users[user.username]["points"] = user.points #updating all information for saving
        users[user.username]["level"] = user.level
        users[user.username]["exp"] = user.exp
        users[user.username]["tasks"] = user.tasks_info
        users[user.username]["shop_details"] = user.shop_details
        with open(r"userdata.json","w") as file:
            json.dump(users,file,indent=4)
#function that closes the program
    def close_program(self):
        self.save_user_data()  # Save user data before closing the program
        root.destroy()
#function that calculates the next level
    def next_level_calc(self,level):
        if level >= 0:
            exp = 50 + level*50**1.1
        else:
            exp = 50
        return int(exp)
#function that updates the levels display
    def update_level(self):
        if user.exp >= self.next_level_calc(user.level):
            user.exp -= self.next_level_calc(user.level)
            user.level += 1
            main.level_lbl.config(text=f"level: {user.level}")
            main.next_level_lbl.config(text=f"Next lvl: {user.exp}/{self.next_level_calc(user.level)}")
        else:
            main.next_level_lbl.config(text=f"Next lvl: {user.exp}/{self.next_level_calc(user.level)}")
#function that updates all user info
    def update_user_info_display(self):
            self.username_lbl.config(text=f"username: {user.username}")
            self.level_lbl.config(text=f"level: {user.level}")
            self.points_lbl.config(text=f"points: {user.points}")
            self.next_level_lbl.config(text=f"Next lvl: {user.exp}/{main.next_level_calc(user.level)}")

#function that gets user data from external file
def get_user_data(username):
    global user
    with open(r"userdata.json","r") as file:
        users = json.load(file) 
    user = UserData(users[username]["username"],users[username]["password"],users)

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
    #binds the mouse to the scroll bar when over the canvas
    def bind_wheel(event=None):
        canvas.bind_all("<MouseWheel>", on_mouse_wheel)
        canvas.bind_all("<Shift-MouseWheel>", on_shift_mouse_wheel)
    #checks for when cursor is in the canvas and binds mouse to it
    canvas.bind("<Enter>", bind_wheel)
    frame.bind("<Configure>", delayed_update)
       
#setting up the root
root = Tk()
root.title("productivity manager")
root.geometry("700x700") 
#constant variables
MIN_AGE = 13
DEFAULT_POINT_REWARD =10
DEFAULT_PROFILE = r"images\default_profile.PNG"
HPRT = 1209600 # highest points rewarded time, (2weeks in seconds)
DEFAULT_MAIN_COLOUR = "#E3E1E1"
DEFAULT_SECONDARY_COLOUR = "#c9c9c9"
main_colour = DEFAULT_MAIN_COLOUR
secondary_colour = DEFAULT_SECONDARY_COLOUR
text_colour = "#000000"
root.config(bg=main_colour)
tip_messages = ["Break large, overwhelming projects down into small, easy steps.",
                "Focus on one single task at a time to improve the quality of your work and save mental energy.",
                "take short breaks, step away from your desk every 90 minutes to rest your brain",
                "study in small sessions",
                "Put your phone on silent, close extra browser tabs, and use noise-canceling tools to protect your attention."]
main = Main(root) #creating the main root
#instantiating frames
shop_screen = ShopScreen(main.shop_frame)
tasks_screen = TasksScreen(main.tasks_frame)
login_screen = LoginScreen(main.root)
root.mainloop()