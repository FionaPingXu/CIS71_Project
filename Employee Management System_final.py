################################################################
#                          Class: CISP 71                      #
#                         Author: Ping Xu                      #
#               Project: Employee Management System            #
################################################################

################################################################
#                    import required libraries                 #
################################################################

# from tkinter import everything
from tkinter import *

# for creating images
from PIL import ImageTk, Image

# for message boxes
import tkinter.messagebox as mb

# for treeview
import tkinter.ttk as ttk

# for filedialog
from tkinter import filedialog

# sqlite is built in Python
import sqlite3

# create the main window
root = Tk()
# give the window a title
root.title("Employee Management System")

# declare a variable to save the path of all the files

# path="/Users/xuping/Downloads/CISD 71 Programming in Python/Employee Management System/"
path="/Users/xuping/Downloads/CISD 71 Programming in Python/Employee Management System/"
# changing the icon of the window
# root.iconbitmap(path+'employee.png')

# change the size of the window
root.geometry("1000x550")

# create a database
# declare a variable for the path
conn = sqlite3.connect(path + "Employee_Information.db")
try:
    # create a cursor to send orders to the database
    c = conn.cursor()

    # create a table - columns and rows
    # use triple quotes to write on more than one line
    # sqlite has five data types: text, null, integer, real, blob(image files, video files)

    c.execute(
        """CREATE TABLE employees (
        employeeID  integer,
        Name  text,
        Birthday integer,
        Gender text, 
        Email  text,
        ContactNo integer,
        City text,
        state text);"""
    )
    print("Table created successfully")
except:
    print("Table already exists")
    conn.rollback()
# commit changes
conn.commit()
# close connection
conn.close()

##################################################################
#                            Functions                           #
##################################################################

# Function to clear the entry boxes
def clearRecords():
    if idEn.get() == "":
        mb.showinfo("Information", "Please select a record to clear")
        return  
    idEn.delete(0, END)
    nameEn.delete(0, END)
    birthEn.delete(0, END)
    gender_var.set(" ")
    emailEn.delete(0, END)
    contactNoEn.delete(0, END)
    cityEn.delete(0, END)
    selected.set(statesList[0])


# Function to add records
def addRecord():
    if idEn.get() == "":
        mb.showinfo("Information", "Please select a record to add")
        return  
    # connect to database
    conn = sqlite3.connect(path + "Employee_Information.db")
    try:
        c = conn.cursor()
        c.execute(
            "INSERT INTO employees VALUES (:a,:b,:c,:d,:e,:f,:g,:h)",
            {
                "a": idEn.get(),
                "b": nameEn.get(),
                "c": birthEn.get(),
                "d": gender_var.get(),
                "e": emailEn.get(),
                "f": contactNoEn.get(),
                "g": cityEn.get(),
                "h": selected.get(),
            },
        )
        # Commit changes to SQL
        conn.commit()
        print("One record added successfully")

    except:
        print("Error in add operation")
        conn.rollback()
    # Close the connection
    conn.close()
    # Clear the texts in the boxes
    clearRecords()
    displayRecords()


# Function to display records
def displayRecords():
    # Clear the treeview
    for row in tvEmployee.get_children():
        tvEmployee.delete(row)
    # Create a database or connection
    conn = sqlite3.connect(path + "Employee_Information.db")
    # Create cursor and send orders to database
    c = conn.cursor()
    # Insert into table
    c.execute("SELECT *, oid FROM employees")
    records = c.fetchall()
    # Show result by looping
    for row in records:
        employeeID = row[0]
        name = row[1]
        birthday = row[2]
        gender = row[3]
        email = row[4]
        contactNo = row[5]
        city = row[6]
        state = row[7]
        tvEmployee.insert(
            "",
            "end",
            text=id,
            values=(
                employeeID,
                name,
                birthday,
                gender,
                email,
                contactNo,
                city,
                state,
                id,
            ),
        )
    # Commite changes
    conn.commit()
    # Close connection
    conn.close()


# Function for updating record
def updateRecord():
    if idEn.get() == "":
        mb.showinfo("Information", "Please select a record to update")
        return  
    # Create a database or connection
    conn = sqlite3.connect(path + "Employee_Information.db")
    # SQL format and replacing current values with c.execute values, values match respectively
    qry = "update employees set name=?, birthday=?, gender=?, email=?, contactNo=?, city=?, state=? where employeeID=?"
    try:
        # create cursor, send orders to database
        c = conn.cursor()
        c.execute(
            qry,
            (
                nameEn.get(),
                birthEn.get(),
                gender_var.get(),
                emailEn.get(),
                contactNoEn.get(),
                cityEn.get(),
                selected.get(),
                idEn.get(),
            ),
        )
        conn.commit()
        print("One record updated successfully")
    except:
        print("Error in update operation")
        conn.rollback()

    conn.close()
    clearRecords()
    displayRecords()


# Function for showing the specific record a user clicks on
def show_selected_record(event):
    clearRecords()
    for selection in tvEmployee.selection():
        item = tvEmployee.item(selection)
        global id
        employeeID, name, birth, gender, email, contactNo, city, state = item["values"][
            0:8
        ]
        idEn.insert(0, employeeID)
        nameEn.insert(0, name)
        birthEn.insert(0, birth)
        gender_var.set(gender)
        emailEn.insert(0, email)
        contactNoEn.insert(0, contactNo)
        cityEn.insert(0, city)
        selected.set(state)
    return id


# Function to delete record
def deleteRecord():
    if idEn.get() == "":
        mb.showinfo("Information", "Please select a record to delete")
        return  
    MsgBox =mb.askyesno("Delete Confirmation", "Are you sure you want to delete record?", icon="warning")
    if MsgBox == 1: 
        conn = sqlite3.connect(path + "Employee_Information.db")
        qry = "DELETE from employees where employeeID=?;"
        try:    # try delete
            c = conn.cursor()
            c.execute(qry, (idEn.get(),))
            conn.commit()
            print("{} deleted successfully".format(idEn.get()))
        except: # try delete error 
            # print("Error in delete operation")
            print("Error in delete operation")
            conn.rollback()
        conn.close()
    clearRecords()
    displayRecords()

# Function to search from database
def searchdb_rows(keyword):
    conn = sqlite3.connect(path + "Employee_Information.db")
    c = conn.cursor()
    c.execute(
        "SELECT * FROM employees WHERE employeeID LIKE ? OR name LIKE ? or email LIKE ?",
        ("%" + keyword + "%", "%" + keyword + "%", "%" + keyword + "%"),
    )
    rows = c.fetchall()
    return rows


# Function to search database and show the result in treeview
def searchdb():
    if searchdbEn.get() != '':
        for item in tvEmployee.get_children():
            tvEmployee.delete(item)
        count = 0
        for row in searchdb_rows(searchdbEn.get()):
            employeeID = row[0]
            name = row[1]
            birth = row[2]
            gender = row[3]
            email = row[4]
            contactNo = row[5]
            city = row[6]
            state = row[7]
            tvEmployee.insert(
                "",
                "end",
                text="employeeID",
                values=(employeeID,
                name,
                birth,
                gender,
                email,
                contactNo,
                city,
                state,
                ),
            )
        count += 1
        print ("Search result is displayed")
    else:
        print("No input in entry")
        

###################################################
#                 Widgets of app                  #
###################################################
# title for main window
mainTitleLb = Label(
    root, text="Employee Management System", font=("Cambria", 20, 'bold'), fg="#696969", pady=10
)

# create label widgets
idLb = Label(root, text="Employee ID")
nameLb = Label(root, text="Name")
birthLb = Label(root, text="D.O.B")
genderLb = Label(root, text="Gender")
cityLb = Label(root, text="City")
stateLb = Label(root, text="State")
contactNoLb = Label(root, text="Contact No")
emailLb = Label(root, text="Email")

# Create labels for treeview select and search
tvLb = Label(root, text="Please select one record below to update or delete")
searchLb = Label(root, text="Enter Employee ID, Name or Contact NO to search:")

# create entry and dropdown widgets
idEn = Entry(root)
nameEn = Entry(root)
birthEn = Entry(root)
ageEn = Entry(root)
cityEn = Entry(root)
contactNoEn = Entry(root)
emailEn = Entry(root)
searchdbEn=Entry(root)


# create a list of states
statesList = [
    " ",
    "AL",
    "AK",
    "AZ",
    "AR",
    "CA",
    "CO",
    "CT",
    "DC",
    "DE",
    "FL",
    "GA",
    "HI",
    "ID",
    "IL",
    "IN",
    "IA",
    "KS",
    "KY",
    "LA",
    "ME",
    "MD",
    "MA",
    "MI",
    "MN",
    "MS",
    "MO",
    "MT",
    "NE",
    "NV",
    "NH",
    "NJ",
    "NM",
    "NY",
    "NC",
    "ND",
    "OH",
    "OK",
    "OR",
    "PA",
    "RI",
    "SC",
    "SD",
    "TN",
    "TX",
    "UT",
    "VT",
    "VA",
    "WA",
    "WV",
    "WI",
    "WY",
]
# define the selected variable for our drop down list of states
selected = StringVar()

# set the default value for the option menu to the first item in the list
selected.set(statesList[0])

# create an OptionMenu widget - drop down list for the states
stateListOp = OptionMenu(root, selected, *statesList)

# create button widgets
addBt = Button(root, text="Add", command=addRecord)
updateBt = Button(root, text="Update", command=updateRecord)
deleteBt = Button(root, text="Delete", command=deleteRecord)
clearBt = Button(root, text="Clear", command=clearRecords)
showAllBt = Button(root, text="Show All", command=displayRecords)
exitBt = Button(root, text="Exit", command=exit)
ptrBt=Button(root, text='Choose Portrait', command=open)

# button to search database
searchdbBt = Button(root, text="Search", command=searchdb)
searchdbEn.bind("<Return>", lambda event: searchdb())



# Radio buttons
# initialize the variable gender_var so that all the radio buttons are not selected by default
gender_var = StringVar()

# Create a frame for gender radio buttons
frmGender = Frame()

# Create radio buttons for gender
rbtn_male = Radiobutton(
    frmGender,
    text="Male",
    font=("Cambria", 10),
    variable=gender_var,
    value="Male",
)
rbtn_female = Radiobutton(
    frmGender,
    text="Female",
    font=("Cambria", 10),
    variable=gender_var,
    value="Female",
    padx=5,
)
rbtn_other = Radiobutton(
    frmGender,
    text="Other",
    font=("Cambria", 10),
    variable=gender_var,
    value="Other",
    padx=5,
)
# Pack the radio buttons
rbtn_male.pack(side=LEFT)
rbtn_female.pack(side=LEFT, ipadx=10)
rbtn_other.pack(side=LEFT, ipadx=10)

######################################################################
#                                Tree view                           #
######################################################################

# Treeview columns and setting headings, and column details
columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7", "8")
tvEmployee = ttk.Treeview(root, show="headings", height="8", columns=columns)

# Scrollbar side of treeview
vsb = ttk.Scrollbar(root, orient='vertical', command=tvEmployee.yview)
#hsb = ttk.Scrollbar(root, orient=HORIZONTAL, command=tvEmployee.xview)
tvEmployee.configure(yscrollcommand=vsb.set)
#tvEmployee.configure(xscrollcommand=hsb.set)

tvEmployee.heading("#1", text="Employee ID", anchor="center")
tvEmployee.column("#1", width=80, anchor="center", stretch=True)

tvEmployee.heading("#2", text="Name", anchor="center")
tvEmployee.column("#2", width=120, anchor="center", stretch=True)

tvEmployee.heading("#3", text="D.O.B", anchor="center")
tvEmployee.column("#3", width=100, anchor="center", stretch=True)

tvEmployee.heading("#4", text="Gender", anchor="center")
tvEmployee.column("#4", width=80, anchor="center", stretch=True)

tvEmployee.heading("#5", text="Email", anchor="center")
tvEmployee.column("#5", width=160, anchor="center", stretch=True)

tvEmployee.heading("#6", text="Contact No", anchor="center")
tvEmployee.column("#6", width=80, anchor="center", stretch=True)

tvEmployee.heading("#7", text="City", anchor="center")
tvEmployee.column("#7", width=60, anchor="center", stretch=True)

tvEmployee.heading("#8", text="State", anchor="center")
tvEmployee.column("#8", width=60, anchor="center", stretch=True)

tvEmployee.bind("<<TreeviewSelect>>", show_selected_record)

##################################################################
#                      Placements of widgets                     #
##################################################################

# X-Y placements with label widgets
mainTitleLb.place(x=350)
idLb.place(x=115, y=50, height=25, width=100)
nameLb.place(x=118, y=78, height=25, width=100)
birthLb.place(x=110, y=106, height=25, width=100)
genderLb.place(x=105, y=134, height=25, width=100)
emailLb.place(x=520, y=50, height=25, width=100)
contactNoLb.place(x=510, y=78, height=25, width=100)
cityLb.place(x=520, y=106, height=25, width=100)
stateLb.place(x=520, y=134, height=25)
tvLb.place(x=270, y=205, height=25)
tvEmployee.place(x=58, y=240, height=200, width=880)
searchLb.place(x=80, y=460, height=25, width=350)

# Place entry widgets and drop down menu widgets
idEn.place(x=215, y=50, height=25, width=200)
nameEn.place(x=215, y=78, height=25, width=200)
birthEn.place(x=215, y=106, height=25, width=200)
emailEn.place(x=640, y=50, height=25, width=200)
contactNoEn.place(x=640, y=78, height=25, width=200)
cityEn.place(x=640, y=106, height=25, width=200)
stateListOp.place(x=640, y=134, width=200)
searchdbEn.place(x=550, y=460, width=300)

# Place button widgets
frmGender.place(x=210, y=135)
addBt.place(x=250, y=170)
updateBt.place(x=330, y=170)
deleteBt.place(x=420, y=170)
clearBt.place(x=510, y=170)
showAllBt.place(x=600, y=170)
exitBt.place(x=450, y=500)
searchdbBt.place(x=450, y=460)

# Place Scrollbar
vsb.place(x=938, y=240, height=200)
#hsb.place(x=58, y=440, width=880)

# main loop
root.mainloop()
