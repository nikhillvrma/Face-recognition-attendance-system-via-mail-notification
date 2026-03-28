import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2, os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time
import re  # For email validation
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

############################################# FUNCTIONS ################################################

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200, tick)

def contact():
    mess._show(title='Contact us', message="Please contact us on: 'm.nikhil1138@gmail.com'")

def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Some file missing', message='Please contact us for help')
        window.destroy()

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel/psd.txt")
    if exists1:
        tf = open("TrainingImageLabel/psd.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas is None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel/psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    op = old.get()
    newp = new.get()
    nnewp = nnew.get()
    if op == key:
        if newp == nnewp:
            txf = open("TrainingImageLabel/psd.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Error', message='Confirm new password again!!!')
            return
    else:
        mess._show(title='Wrong Password', message='Please enter correct old password.')
        return
    mess._show(title='Password Changed', message='Password changed successfully!!')
    master.destroy()

def change_pass():
    global master
    master = tk.Tk()
    master.geometry("400x160")
    master.resizable(False, False)
    master.title("Change Password")
    master.configure(background="#f0f2f5")
    
    tk.Label(master, text='Enter Old Password', bg="#f0f2f5", font=('Roboto', 12)).place(x=20, y=10)
    global old
    old = tk.Entry(master, width=25, fg="black", relief='solid', 
                  font=('Roboto', 12), show='*', highlightthickness=1)
    old.place(x=180, y=10)
    old.configure(highlightbackground="#cccccc", highlightcolor="#4a6fa5")
    
    tk.Label(master, text='Enter New Password', bg="#f0f2f5", font=('Roboto', 12)).place(x=20, y=45)
    global new
    new = tk.Entry(master, width=25, fg="black", relief='solid', 
                  font=('Roboto', 12), show='*', highlightthickness=1)
    new.place(x=180, y=45)
    new.configure(highlightbackground="#cccccc", highlightcolor="#4a6fa5")
    
    tk.Label(master, text='Confirm New Password', bg="#f0f2f5", font=('Roboto', 12)).place(x=20, y=80)
    global nnew
    nnew = tk.Entry(master, width=25, fg="black", relief='solid', 
                   font=('Roboto', 12), show='*', highlightthickness=1)
    nnew.place(x=180, y=80)
    nnew.configure(highlightbackground="#cccccc", highlightcolor="#4a6fa5")
    
    tk.Button(master, text="Cancel", command=master.destroy, fg="white", bg="#e74c3c",
             font=('Roboto', 10, 'bold'), width=10).place(x=200, y=120)
    tk.Button(master, text="Save", command=save_pass, fg="white", bg="#2ecc71",
             font=('Roboto', 10, 'bold'), width=10).place(x=100, y=120)
    
    master.mainloop()

def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel/psd.txt")
    if exists1:
        tf = open("TrainingImageLabel/psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas is None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel/psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if password == key:
        TrainImages()
    elif password is None:
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')

def clear():
    txt.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)

def clear2():
    txt2.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)

def clear3():
    txt3.delete(0, 'end')

def update_registration_counter():
    """Function to accurately count and display the total number of registrations"""
    global res
    res = 0
    csv_file = "StudentDetails/StudentDetails.csv"
    
    if os.path.isfile(csv_file):
        try:
            with open(csv_file, 'r') as csvFile1:
                reader1 = csv.reader(csvFile1)
                # Skip header if it exists
                try:
                    next(reader1)  # Skip header row
                    for row in reader1:
                        # Only count rows that have at least 3 columns (ID, Name, Email)
                        if len(row) >= 3 and any(field.strip() for field in row):
                            res += 1
                except StopIteration:
                    pass  # File is empty except for header
        except Exception as e:
            print(f"Error reading CSV file: {e}")
    else:
        res = 0
    
    # Update the counter display
    message.config(
        text=f'TOTAL REGISTRATIONS: {res}',
        font=('Roboto', 12, 'bold'),
        fg='#FFFFFF',
        bg='#166088',
        padx=8,
        pady=3,
        relief='raised',
        borderwidth=1
    )
    return res

def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME', '', 'PARENT EMAIL']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")
    
    # Get the next available serial number
    serial = 0
    csv_file = "StudentDetails/StudentDetails.csv"
    
    if os.path.isfile(csv_file):
        with open(csv_file, 'r') as csvFile:
            reader = csv.reader(csvFile)
            # Skip header if it exists
            try:
                next(reader)
                # Find the highest existing serial number
                for row in reader:
                    if row and len(row) > 0:  # Check if row is not empty
                        try:
                            current_serial = int(row[0])
                            if current_serial > serial:
                                serial = current_serial
                        except (ValueError, IndexError):
                            continue
            except StopIteration:
                pass  # File is empty except for header
    else:
        # File doesn't exist, create it with header
        with open(csv_file, 'w', newline='') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
    
    serial += 1  # Next available serial number
    
    Id = txt.get().strip()
    name = txt2.get().strip()
    parent_email = txt3.get().strip()
    
    if not name.replace(' ', '').isalpha():
        mess._show(title='Error', message='Name should only contain alphabets and spaces')
        return
    
    if not is_valid_email(parent_email):
        mess._show(title='Error', message='Please enter a valid parent email address')
        return
    
    if not Id or not name or not parent_email:
        mess._show(title='Error', message='Please fill all fields')
        return
    
    if Id and name and parent_email:
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        
        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                sampleNum += 1
                cv2.imwrite(f"TrainingImage/{name}.{serial}.{Id}.{sampleNum}.jpg", gray[y:y+h, x:x+w])
                cv2.imshow('Taking Images', img)
            
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif sampleNum > 100:
                break
        
        cam.release()
        cv2.destroyAllWindows()
        
        res = f"Images Taken for ID: {Id}"
        row = [serial, '', Id, '', name, '', parent_email]
        
        # Write to CSV file
        with open(csv_file, 'a', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        
        message1.configure(text=res)
        update_registration_counter()  # Update the counter display
    else:
        mess._show(title='Error', message='Please fill all fields')

def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face.LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register someone first!!!')
        return
    
    recognizer.save("TrainingImageLabel/Trainner.yml")
    res = "Profile Saved Successfully"
    message1.configure(text=res)
    update_registration_counter()  # Update the counter display

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    Ids = []
    
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(ID)
    
    return faces, Ids

def send_absence_notification(parent_email, student_name, date):
    # Email configuration - replace with your actual credentials
    sender_email = "m.nikhil1138@gmail.com"
    sender_password = "gslh vbjl xzfn tdsx"
    
    # Create message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = parent_email
    message["Subject"] = f"Absence Notification for {student_name}"
    
    # Email body
    body = f"""
    Dear Parent/Guardian,
    
    This is to inform you that your child, {student_name}, was absent from college on {date}.
    
    If this absence was not planned, please contact the college office to clarify the reason.
    
    Sincerely,
    College Administration
    """
    
    message.attach(MIMEText(body, "plain"))
    
    try:
        # Send email (using Gmail SMTP as example)
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, parent_email, message.as_string())
        print(f"Notification sent to {parent_email} for {student_name}")
    except Exception as e:
        print(f"Failed to send email to {parent_email}: {str(e)}")

def mark_absent_students():
    """Function to mark absent students and send notifications"""
    today = datetime.datetime.now().strftime('%d-%m-%Y')
    attendance_file = f"Attendance/Attendance_{today}.csv"
    
    if not os.path.isfile(attendance_file):
        mess._show(title='No Attendance', message='No attendance taken today!')
        return
    
    # Read all student details to get emails
    student_details = {}
    if os.path.isfile("StudentDetails/StudentDetails.csv"):
        df = pd.read_csv("StudentDetails/StudentDetails.csv")
        for _, row in df.iterrows():
            student_id = str(row['ID']).strip()
            student_name = str(row['NAME']).strip()
            parent_email = str(row['PARENT EMAIL']).strip()
            if student_id and student_name and parent_email:
                student_details[student_id] = {
                    'name': student_name,
                    'email': parent_email
                }
    
    # Read attendance file and find absent students
    absent_students = []
    with open(attendance_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            if len(row) >= 3:  # Ensure row has enough columns
                student_id = row[0].strip()
                status = row[2].strip() if len(row) > 2 else ''
                
                # Only consider students marked as absent
                if status == 'Absent' and student_id in student_details:
                    student_name = student_details[student_id]['name']
                    parent_email = student_details[student_id]['email']
                    if is_valid_email(parent_email):
                        absent_students.append((student_name, parent_email))
    
    if not absent_students:
        mess._show(title='No Absences', message='All students are present today!')
        return
    
    # Ask for confirmation before sending emails
    confirm = mess.askyesno(
        'Confirm Notification',
        f'Send absence notifications for {len(absent_students)} students?'
    )
    if not confirm:
        return
    
    # Send notifications
    sent_count = 0
    for student_name, parent_email in absent_students:
        try:
            send_absence_notification(parent_email, student_name, today)
            sent_count += 1
        except Exception as e:
            print(f"Failed to send email to {parent_email}: {str(e)}")
    
    mess._show(
        title='Notifications Sent',
        message=f'Absence notifications sent for {sent_count} students'
    )

def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")
    
    for k in tv.get_children():
        tv.delete(k)
    
    # Initialize variables
    recognizer = cv2.face.LBPHFaceRecognizer.create()
    exists3 = os.path.isfile("TrainingImageLabel/Trainner.yml")
    
    if exists3:
        recognizer.read("TrainingImageLabel/Trainner.yml")
    else:
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return
    
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # Get current date
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    
    # Read all student details
    exists1 = os.path.isfile("StudentDetails/StudentDetails.csv")
    if exists1:
        df = pd.read_csv("StudentDetails/StudentDetails.csv")
    else:
        mess._show(title='Details Missing', message='Students details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
        return
    
    # Initialize attendance_dict by loading existing attendance if available
    attendance_file = f"Attendance/Attendance_{date}.csv"
    attendance_dict = {}
    
    # If attendance file exists, load it first
    if os.path.isfile(attendance_file):
        with open(attendance_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                if len(row) >= 5:  # Ensure row has all columns
                    student_id = row[0].strip()
                    attendance_dict[student_id] = {
                        'name': row[1].strip(),
                        'status': row[2].strip(),
                        'time': row[3].strip(),
                        'date': row[4].strip()
                    }
    
    # For any students not already in attendance_dict, initialize them as Absent
    for _, row in df.iterrows():
        student_id = str(row['ID']).strip()
        if student_id not in attendance_dict:
            attendance_dict[student_id] = {
                'name': str(row['NAME']).strip(),
                'status': 'Absent',
                'time': 'N/A',
                'date': date
            }
    
    # Column names for attendance file
    col_names = ['ID', 'Name', 'Status', 'Time', 'Date']
    
    # Start video capture for attendance
    start_time = time.time()
    duration = 30  # Set duration for attendance taking (30 seconds)
    
    while (time.time() - start_time) < duration:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            
            if conf < 50:
                ts = time.time()
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                try:
                    # Get student details
                    aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values[0]
                    ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values[0]
                    ID = str(ID).strip()
                    
                    # Update attendance dictionary only for recognized students
                    attendance_dict[ID]['status'] = 'Present'
                    attendance_dict[ID]['time'] = timeStamp
                    attendance_dict[ID]['date'] = date
                    
                    # Display recognized student
                    bb = str(aa)
                    cv2.putText(im, bb, (x, y + h), font, 1, (255, 255, 255), 2)
                except:
                    pass  # Skip if recognition fails
        
        cv2.imshow('Taking Attendance', im)
        if cv2.waitKey(1) == ord('q'):
            break
    
    # Release camera
    cam.release()
    cv2.destroyAllWindows()
    
    # Save attendance to CSV
    with open(attendance_file, 'w', newline='') as csvFile1:
        writer = csv.writer(csvFile1)
        writer.writerow(col_names)
        
        for student_id, data in attendance_dict.items():
            writer.writerow([
                student_id,
                data['name'],
                data['status'],
                data['time'],
                data['date']
            ])
    
    # Display attendance in the treeview
    with open(attendance_file, 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        next(reader1)  # Skip header
        for lines in reader1:
            if len(lines) >= 5:  # Ensure we have all columns
                iidd = str(lines[0]) + '   '
                status = lines[2]
                # Color coding based on status
                if status == 'Present':
                    tag = 'present'
                else:
                    tag = 'absent'
                
                tv.insert('', 'end', text=iidd, values=(
                    str(lines[1]),  # Name
                    str(lines[2]),  # Status
                    str(lines[3]),  # Time
                    str(lines[4])   # Date
                ), tags=(tag,))

    # Configure tag colors
    tv.tag_configure('present', background='#d4edda')  # Light green for present
    tv.tag_configure('absent', background='#f8d7da')   # Light red for absent

######################################## USED STUFFS ############################################

global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day, month, year = date.split("-")

mont = {
    '01': 'January', '02': 'February', '03': 'March', '04': 'April',
    '05': 'May', '06': 'June', '07': 'July', '08': 'August',
    '09': 'September', '10': 'October', '11': 'November', '12': 'December'
}

######################################## GUI FRONT-END ###########################################

# Main window setup
window = tk.Tk()
window.geometry("1280x720")
window.resizable(True, True)
window.title("Attendance System")
window.configure(background='#f0f2f5')

# Custom font styles
title_font = ('Roboto', 30, 'bold')
heading_font = ('Roboto', 18, 'bold')
label_font = ('Roboto', 14)
entry_font = ('Roboto', 12)
button_font = ('Roboto', 12, 'bold')

# Color palette
primary_color = "#4a6fa5"  # Muted blue
secondary_color = "#166088"  # Darker blue
accent_color = "#4fc3f7"  # Light blue
success_color = "#66bb6a"  # Green
warning_color = "#ffa726"  # Orange
danger_color = "#ef5350"  # Red
light_bg = "#ffffff"  # White
dark_text = "#333333"  # Dark gray
light_text = "#f5f5f5"  # Light gray

# Header
header = tk.Frame(window, bg=primary_color, height=80)
header.pack(fill='x')

# Title in header
title = tk.Label(header, text="Face Recognition Based Attendance System", 
                fg="white", bg=primary_color, font=title_font)
title.pack(pady=20)

# Time and date display
time_date_frame = tk.Frame(header, bg=primary_color)
time_date_frame.pack(side='right', padx=20)

datef = tk.Label(time_date_frame, text=f"{day}-{mont[month]}-{year}  |  ", 
                fg="white", bg=primary_color, font=('Roboto', 14))
datef.pack(side='left')

clock = tk.Label(time_date_frame, fg="white", bg=primary_color, font=('Roboto', 14))
clock.pack(side='left')
tick()

# Main content area
content = tk.Frame(window, bg='#f0f2f5')
content.pack(fill='both', expand=True, padx=20, pady=10)

# Left panel (Registered users)
frame1 = tk.Frame(content, bg=light_bg, bd=2, relief='groove')
frame1.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

frame1_header = tk.Label(frame1, text="For Already Registered", 
                        bg=secondary_color, fg="white", font=heading_font)
frame1_header.pack(fill='x', pady=(0, 15))

# Attendance section
lbl3 = tk.Label(frame1, text="Attendance", width=20, fg=dark_text, 
               bg=light_bg, font=heading_font)
lbl3.pack(pady=(8, 4))

trackImg = tk.Button(frame1, text="Take Attendance", command=TrackImages, 
                    fg="white", bg=primary_color, width=25, height=1, 
                    font=button_font, activebackground=accent_color)
trackImg.pack(pady=8)

# Mark Absent button
markAbsent = tk.Button(frame1, text="Mark Absent Students", command=mark_absent_students, 
                      fg="white", bg=warning_color, width=25, height=1, 
                      font=button_font, activebackground="#ffcc80")
markAbsent.pack(pady=8)

# Attendance table
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background=light_bg, fieldbackground=light_bg, 
               foreground=dark_text, font=('Roboto', 11))
style.configure("Treeview.Heading", background=secondary_color, 
               foreground="white", font=('Roboto', 12, 'bold'))
style.map("Treeview", background=[('selected', accent_color)])

tv = ttk.Treeview(frame1, height=13, columns=('name', 'status', 'time', 'date'))
tv.column('#0', width=100, anchor='center')
tv.column('name', width=150, anchor='center')
tv.column('status', width=100, anchor='center')
tv.column('time', width=100, anchor='center')
tv.column('date', width=100, anchor='center')
tv.heading('#0', text='ID', anchor='center')
tv.heading('name', text='NAME', anchor='center')
tv.heading('status', text='STATUS', anchor='center')
tv.heading('time', text='TIME', anchor='center')
tv.heading('date', text='DATE', anchor='center')
tv.pack(pady=(8, 0))

scroll = ttk.Scrollbar(frame1, orient='vertical', command=tv.yview)
scroll.pack(side='right', fill='y')
tv.configure(yscrollcommand=scroll.set)

quitWindow = tk.Button(frame1, text="Quit", command=window.destroy, 
                      fg="white", bg=danger_color, width=25, height=1, 
                      font=button_font, activebackground="#ff8a80")
quitWindow.pack(pady=15)

# Right panel (New registrations)
frame2 = tk.Frame(content, bg=light_bg, bd=2, relief='groove')
frame2.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

frame2_header = tk.Label(frame2, text="For New Registrations", 
                        bg=secondary_color, fg="white", font=heading_font)
frame2_header.pack(fill='x', pady=(0, 15))

# Registration form
form_frame = tk.Frame(frame2, bg=light_bg)
form_frame.pack(fill='both', padx=20, pady=(5, 0))

# ID field
lbl = tk.Label(form_frame, text="Enter ID", fg=dark_text, 
              bg=light_bg, font=label_font, anchor='w')
lbl.pack(fill='x', pady=(3, 0))

txt = tk.Entry(form_frame, width=32, fg=dark_text, font=entry_font, 
              highlightthickness=1, relief='solid')
txt.pack(fill='x', pady=(0, 5))
txt.configure(highlightbackground="#cccccc", highlightcolor=accent_color)

clearButton = tk.Button(form_frame, text="Clear", command=clear, 
                       fg="white", bg=warning_color, width=10, 
                       font=button_font, activebackground="#ffcc80")
clearButton.pack(pady=(0, 8))

# Name field
lbl2 = tk.Label(form_frame, text="Enter Name", fg=dark_text, 
               bg=light_bg, font=label_font, anchor='w')
lbl2.pack(fill='x', pady=(3, 0))

txt2 = tk.Entry(form_frame, width=32, fg=dark_text, font=entry_font, 
               highlightthickness=1, relief='solid')
txt2.pack(fill='x', pady=(0, 5))
txt2.configure(highlightbackground="#cccccc", highlightcolor=accent_color)

clearButton2 = tk.Button(form_frame, text="Clear", command=clear2, 
                        fg="white", bg=warning_color, width=10, 
                        font=button_font, activebackground="#ffcc80")
clearButton2.pack(pady=(0, 8))

# Parent Email field
lbl3 = tk.Label(form_frame, text="Parent Email", fg=dark_text, 
               bg=light_bg, font=label_font, anchor='w')
lbl3.pack(fill='x', pady=(3, 0))

txt3 = tk.Entry(form_frame, width=32, fg=dark_text, font=entry_font, 
               highlightthickness=1, relief='solid')
txt3.pack(fill='x', pady=(0, 5))
txt3.configure(highlightbackground="#cccccc", highlightcolor=accent_color)

clearButton3 = tk.Button(form_frame, text="Clear", command=clear3, 
                        fg="white", bg=warning_color, width=10, 
                        font=button_font, activebackground="#ffcc80")
clearButton3.pack(pady=(0, 10))

# Instructions
message1 = tk.Label(form_frame, text="1)Take Images  >>>  2)Save Profile", 
                   bg=light_bg, fg=secondary_color, width=39, height=1, 
                   font=('Roboto', 13, 'bold'))
message1.pack(pady=(5, 10))

# Action buttons
button_frame = tk.Frame(form_frame, bg=light_bg)
button_frame.pack(fill='x', pady=5)

takeImg = tk.Button(button_frame, text="Take Images", command=TakeImages, 
                   fg="white", bg=primary_color, width=15, height=1, 
                   font=button_font, activebackground=accent_color)
takeImg.pack(side='left', padx=5)

trainImg = tk.Button(button_frame, text="Save Profile", command=psw, 
                    fg="white", bg=success_color, width=15, height=1, 
                    font=button_font, activebackground="#81c784")
trainImg.pack(side='left', padx=5)

# Registration counter
message = tk.Label(frame2)
message.pack(side='bottom', pady=5)
update_registration_counter()  # Initialize and display the counter

##################### MENUBAR #################################

menubar = tk.Menu(window, relief='ridge', bg=light_bg, fg=dark_text)

# File menu
filemenu = tk.Menu(menubar, tearoff=0, bg=light_bg, fg=dark_text, 
                  activebackground=accent_color, activeforeground="white")
filemenu.add_command(label='Change Password', command=change_pass)
filemenu.add_command(label='Contact Us', command=contact)
filemenu.add_separator()
filemenu.add_command(label='Exit', command=window.destroy)

menubar.add_cascade(label='Help', menu=filemenu)
window.configure(menu=menubar)

##################### END ######################################

# Configure grid weights
content.grid_columnconfigure(0, weight=1)
content.grid_columnconfigure(1, weight=1)
content.grid_rowconfigure(0, weight=1)

window.mainloop()