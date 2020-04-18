import tkinter as tk
from tkinter import *
from tkinter.messagebox import showinfo
from PIL import Image
from PIL import ImageTk
from lock_functions import *
from sql_functions import *
from email_functions import *

# compare the employee_pin with the table on the SQL table and return true if it exists #
def authenticate_pin(employee_pin):
    myarray = storeEmployeePin()
    myarraylen = len(myarray)
    InsertEmployeeIDEmployeeAccess(employee_pin)
    employee = ReadEmployeeIDEmployeeAccess()
    return compareEmployeePin(employee_pin, myarray)

def authenticate_order(order_id):
    myarray = storeOrderID()
    myarraylen = len(myarray)
    InsertOrderIDEmployeeAccess(order_id)
    order = ReadOrderIDEmployeeAccess()
    return compareOrderID(order_id, myarray)

def BuildEmail(order_id):
    customer_email = ExtractEmail(int(order_id))
    unlock_code = GenerateUnlockCode()
    GenerateQRCode(order_id, unlock_code)

    lock_id = GetWorkingLockerID()
    employee_id = ReadEmployeeIDEmployeeAccess()
    tuple = CreateOrdersStocked(employee_id, order_id, unlock_code, lock_id)
    InsertOrdersStocked(tuple)

    SendEmail(customer_email, order_id, unlock_code)
    
def archive_order(unlock_code):
    SwitchOrdersStockToArchive(unlock_code)

def authenticate_unlockcode(unlock_code):
    myarray = storeUnlockCode()
    myarraylen = len(myarray)
    return compareUnlockCode(unlock_code, myarray)

class srsApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(Home)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class Home(tk.Frame):
    def __init__(self, master):
        DeleteEmployeeAccess()
        DeleteWorkingLockerID()
        tk.Frame.__init__(self, master)
        tk.Frame.pack(self, side="top", fill="both", expand=True)
        tk.Frame.grid_rowconfigure(self, 0, weight=12)
        tk.Frame.grid_columnconfigure(self, 0, weight=12)
        tk.Frame.configure(self, bg="dark red")
        
        load = Image.open("srs1.png")
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.pack(side=TOP)

        label = tk.Label(self, text="Welcome to SRS!", borderwidth=4, bd=4, relief="flat", font="Times 44", fg="white")
        label.config(bg="dark red", )
        label.pack(side="top")

        # labels can be text or images
        tk.Button(self, text="Customer Entry",
                  command=lambda: master.switch_frame(customerPage)).pack()
        tk.Button(self, text="Employee Entry",
                  command=lambda: master.switch_frame(employeeID)).pack()


class customerPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.pack(self, side="top", fill="both", expand=True)
        tk.Frame.grid_rowconfigure(self, 0, weight=12)
        tk.Frame.grid_columnconfigure(self, 0, weight=12)
        tk.Frame.configure(self, bg="dark red")

        self.load = Image.open("srs1.png")
        self.render = ImageTk.PhotoImage(self.load)
        self.img = Label(self, image=self.render)
        self.img.image = self.render
        self.img.pack(side=TOP)

        self.label = tk.Label(self, text="Enter unlock code.", borderwidth=4, bd=4, relief="flat", font="Times 44",
                              fg="white")
        self.label.config(bg="dark red", )
        self.label.pack(side="top")

        self.name = Label(self, text="Your Code: ")
        self.name.place(x=190, y=230)

        self.entry = tk.Entry(self)
        self.entry.place(x=270, y=230)
        self.entry.focus_set()

        self.submit = tk.Button(self, text="Submit")
        self.submit.config(command=lambda: self.ob(master))
        self.submit.place(x=280, y=260)

        self.submit2 = tk.Button(self, text="Help", command=lambda: helpCustomer())
        self.submit2.place(x=360, y=260)

        self.submit3 = tk.Button(self, text="Home", command=lambda: master.switch_frame(Home))
        self.submit3.place(x=565, y=120)

    def ob(self, master):
        v = (self.entry.get())
        if v != "" and authenticate_unlockcode(v):
            try:
                locker_id = GetLockerID(v)
                order_id = GetOrderIDOfUnlockCode(v)
                DeleteQRCodeFile(order_id)
                archive_order(v)
                user_num = int(v)
                working_locker = Lock(locker_id)
                working_locker.close_locker()
                working_locker.open_locker()
                ChangeLockerState(locker_id, "FALSE")
                SetWorkingLockerID(locker_id)
                master.switch_frame(lockerOpen)
                return user_num
            except ValueError:
                self.entry.delete(first=0,last=100)
                popUp()
        else:
            self.entry.delete(first=0,last=100)
            popUp()

def close_locker_popup():
    showinfo("Locker is open.", "Please close the locker before sending email.")

def close_locker_popup_customer():
    showinfo("Locker is open.", "Please close the locker.")

def popUp():
    showinfo("Incorrect code.", "Could not find a match. Please enter the correct code.")

def noFreeLockersPopUp():
    showinfo("No free lockers.", "No lockers are available. Unable to stock new order.")

def helpCustomer():
    showinfo("Helpful Information", "Enter your unlock code or scan the QR code you received from your email")

class lockerOpen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.pack(self, side="top", fill="both", expand=True)
        tk.Frame.grid_rowconfigure(self, 0, weight=12)
        tk.Frame.grid_columnconfigure(self, 0, weight=12)
        tk.Frame.configure(self, bg="dark red")

        self.load = Image.open("srs1.png")
        self.render = ImageTk.PhotoImage(self.load)
        self.img = Label(self, image=self.render)
        self.img.image = self.render
        self.img.pack(side=TOP)

        self.label = tk.Label(self, text="Retrieve items and close locker.", borderwidth=4, bd=4,
                              relief="flat", font="Times 30", fg="white")
        self.label.config(bg="dark red", )
        self.label.pack(side="top")

        self.submit = tk.Button(self, text="Done")
        self.submit.config(command=lambda: self.ob(master))
        self.submit.place(x=280, y=225)

    def ob(self, master):
        locker_id = GetWorkingLockerID()
        working_locker = Lock(locker_id)
        if not working_locker.is_locker_open():
            try:
                master.switch_frame(thankCustomer)
            except ValueError:
                close_locker_popup_customer()
        else:
            close_locker_popup_customer()

class thankCustomer(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.pack(self, side="top", fill="both", expand=True)
        tk.Frame.grid_rowconfigure(self, 0, weight=12)
        tk.Frame.grid_columnconfigure(self, 0, weight=12)
        tk.Frame.configure(self, bg="dark red")

        self.load = Image.open("srs1.png")
        self.render = ImageTk.PhotoImage(self.load)
        self.img = Label(self, image=self.render)
        self.img.image = self.render
        self.img.pack(side=TOP)

        self.label = tk.Label(self, text="Thank you for shopping with SRS!", borderwidth=4, bd=4, relief="flat",
                              font="Times 30", fg="white")
        self.label.config(bg="dark red", )
        self.label.pack(side="top")

        self.submit = tk.Button(self, text="Home")
        self.submit.config(command=lambda: master.switch_frame(Home))
        self.submit.place(x=280, y=225)

class employeeID(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.pack(self, side="top", fill="both", expand=True)
        tk.Frame.grid_rowconfigure(self, 0, weight=12)
        tk.Frame.grid_columnconfigure(self, 0, weight=12)
        tk.Frame.configure(self, bg="dark red")

        self.load = Image.open("srs1.png")
        self.render = ImageTk.PhotoImage(self.load)
        self.img = Label(self, image=self.render)
        self.img.image = self.render
        self.img.pack(side=TOP)

        self.label = tk.Label(self, text="Enter employee ID pin", borderwidth=4, bd=4, relief="flat", font="Times 44",
                              fg="white")
        self.label.config(bg="dark red", )
        self.label.pack(side="top")

        self.name = Label(self, text="Employee Code:")
        self.name.place(x=155, y=250)

        self.entry = tk.Entry(self)
        self.entry.place(x=260, y=250)
        self.entry.focus_set()

        self.homeButton = tk.Button(self, text="Home", command=lambda: master.switch_frame(Home))
        self.homeButton.place(relx=.90, rely=.25)

        self.submit = tk.Button(self, text="Submit")
        self.submit.config(command=lambda: self.ob(master))
        self.submit.place(x=265, y=280)

        self.submit3 = tk.Button(self, text="Home", command=lambda: master.switch_frame(Home))
        self.submit3.place(x=700, y=160)

    def ob(self, master):
        v = (self.entry.get())
        if v != "" and authenticate_pin(v):
            try:
                user_num = int(v)
                master.switch_frame(employeeEntry)
                return user_num
            except ValueError:
                popUp()
        else:
            self.entry.delete(first=0,last=100)
            popUp()

class employeeEntry(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.pack(self, side="top", fill="both", expand=True)
        tk.Frame.grid_rowconfigure(self, 0, weight=12)
        tk.Frame.grid_columnconfigure(self, 0, weight=12)
        tk.Frame.configure(self, bg="dark red")

        self.load = Image.open("srs1.png")
        self.render = ImageTk.PhotoImage(self.load)
        self.img = Label(self, image=self.render)
        self.img.image = self.render
        self.img.pack(side=TOP)

        self.label = tk.Label(self, text="Scan order barcode", borderwidth=4, bd=4, relief="flat", font="Times 44",
                              fg="white")
        self.label.config(bg="dark red")
        self.label.pack(side="top", fill="x")

        self.homeButton = tk.Button(self, text="Home", command=lambda: master.switch_frame(Home))
        self.homeButton.place(relx=.90, rely=.25)

        self.text = Text(self)

        self.text.place(x=160, y=270, width=300, height=75)
        self.text.focus_set()

        self.ope = tk.Button(self, text='Open Locker', command=lambda: self.ob(master))
        self.ope.place(x=250, y=350)

    def ob(self, master):
        v = (self.text.get("1.0", "end"))
        if OpenLockersExist():
            try:
                locker_id = FindOpenLocker()
                SetWorkingLockerID(locker_id)
                working_locker = Lock(locker_id)
                working_locker.close_locker()
                working_locker.open_locker()
                #update Lockers table with open status
                if v != "" and authenticate_order(v):
                    try:
                        user_num = int(v)
                        master.switch_frame(reStock)
                        return user_num
                    except ValueError:
                        self.text.delete("1.0", "end")
                        self.text.update()
                        popUp()
                else:
                    self.text.delete("1.0", "end")
                    self.text.update()
                    popUp()
            except ValueError:
                self.text.delete("1.0", "end")
                self.text.update()
                noFreeLockersPopUp()
        else:
            self.text.delete("1.0", "end")
            self.text.update()
            noFreeLockersPopUp()
            master.switch_frame(Home)


class reStock(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.pack(self, side="top", fill="both", expand=True)
        tk.Frame.grid_rowconfigure(self, 0, weight=12)
        tk.Frame.grid_columnconfigure(self, 0, weight=12)
        tk.Frame.configure(self, bg="dark red")

        self.load = Image.open("srs1.png")
        self.render = ImageTk.PhotoImage(self.load)
        self.img = Label(self, image=self.render)
        self.img.image = self.render
        self.img.pack(side=TOP)

        self.label = tk.Label(self, text="Place customer order in locker.", borderwidth=4, bd=4, relief="flat",
                              font="Times 32",
                              fg="white")
        self.label.config(bg="dark red")
        self.label.pack(side="top", fill="x")

        self.finished = tk.Button(self, text="Send confirmation code.",
                                  command=lambda: self.ob(master))
        
        self.finished.place(relx=.35, rely=.50, width=200, height=50)

        self.notFinished = tk.Button(self, text="Reopen locker.",
                                  command=lambda: self.openlocker(master))
        self.notFinished.place(relx=.35, rely=.60, width=200, height=50)

    def ob(self, master):
        locker_id = GetWorkingLockerID()
        working_locker = Lock(locker_id)
        if not working_locker.is_locker_open():
            try:
                order_id = ReadOrderIDEmployeeAccess()
                BuildEmail(str(order_id))
                working_locker.close_locker()
                ChangeLockerState(locker_id, "TRUE")
                master.switch_frame(orderStocked)
            except ValueError:
                close_locker_popup()
        else:
            close_locker_popup()

    def openlocker(self, master):
        locker_id = GetWorkingLockerID()
        working_locker = Lock(locker_id)
        if not working_locker.is_locker_open():
            working_locker.close_locker()
            working_locker.open_locker()
        #update state in table

class orderStocked(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.pack(self, side="top", fill="both", expand=True)
        tk.Frame.grid_rowconfigure(self, 0, weight=12)
        tk.Frame.grid_columnconfigure(self, 0, weight=12)
        tk.Frame.configure(self, bg="dark red")

        self.load = Image.open("srs1.png")
        self.render = ImageTk.PhotoImage(self.load)
        self.img = Label(self, image=self.render)
        self.img.image = self.render
        self.img.pack(side=TOP)

        self.label = tk.Label(self, text="Order stocked.", borderwidth=4, bd=4, relief="flat", font="Times 32",
                              fg="white")
        self.label.config(bg="dark red")
        self.label.pack(side="top", fill="x")

        self.label = tk.Label(self, text="Confirmation email and text sent.", borderwidth=4, bd=4, relief="flat",
                              font="Times 32",
                              fg="white")
        self.label.config(bg="dark red")
        self.label.pack(side="top", fill="x")

        self.home = tk.Button(self, text="Home", command=lambda: master.switch_frame(Home))
        self.home.place(relx=.44, rely=.62)

if __name__ == "__main__":
    app = srsApp()
    app.geometry("900x600")
    app.attributes('-fullscreen', True)
    app.mainloop()
