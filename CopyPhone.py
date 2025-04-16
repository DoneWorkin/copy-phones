#!/usr/bin/python3
import tkinter as tk
import subprocess
import platform
import os
from datetime import datetime
# constants that contain likely changing stuff -------------------------------------------------------------

# application version for display at the top
APPLICATION_VERSION = 'v2025-04-16.1'

# used to check if the memory card is in the computer - this directory is checked for
BLOG_CHECK_LOC_LINUX = r"/media/rick/BlogSD/Original Photos"
BLOG_CHECK_LOC_WIN = r"D:\Original Photos"

# locations of the images on the phone for ADB
SOURCE_LOCATION_PHOTOS = r"/sdcard/DCIM"
SOURCE_LOCATION_CAPTURES = r"/sdcard/Pictures"

# location and path to SD card
DESTINATION_LOCATION_RICK_LINUX = r"/media/rick/BlogSD/Original Photos/Rick Phone"
DESTINATION_LOCATION_RICK_WIN = r"D:\Original Photos\Rick Phone"

DESTINATION_LOCATION_JULIE_LINUX = r"/media/rick/BlogSD/Original Photos/Julie Phone"
DESTINATION_LOCATION_JULIE_WIN = r"D:\Original Photos\Julie Phone"

# phone ID for ADB so we can check the proper phone is connected
PHONE_ID_RICK = '35121JEHN13600'
PHONE_ID_JULIE = '39290DLJG002V8'

image_data = "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"
# end constants ----------------------------------------------------------------------------------

def check_connection():
    global connectionOK
    global destinationLocation
    global isLinux

    connectionOK = False

    if isLinux:
        directory_path = BLOG_CHECK_LOC_LINUX
    else:
        directory_path = BLOG_CHECK_LOC_WIN

    if os.path.isdir(directory_path):
        txt_edit.insert(tk.END, 'Blog memory card found\n','tag_green')
    else:
        txt_edit.insert(tk.END, 'BLOG MEMORY CARD MISSING - FIX AND TRY AGAIN\n','tag_red')
        return
 
    # find the device
    result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE)
    res = str(result)
    #print (str)
    #startIndex = res.index('devices attached') + len('devices attached')
    #phoneID = res[startIndex+2:startIndex+16]
    #phoneID = phoneID.strip()
    #phoneID = phoneID.strip('\n\r')
    #print (len(phoneID))
    
    if ('unauthorized' in res):
        txt_edit.insert(tk.END, "LOOK AT PHONE AND AUTHORIZE CONNECTION - FIX AND TRY AGAIN\n",'tag_red')
        return

    if (PHONE_ID_RICK in res):
        txt_edit.insert(tk.END, "Rick's phone found\n",'tag_green')
        if isLinux:
            destinationLocation = DESTINATION_LOCATION_RICK_LINUX
        else:
            destinationLocation = DESTINATION_LOCATION_RICK_WIN
    elif (PHONE_ID_JULIE in res):
        txt_edit.insert(tk.END, "Julie's phone found\n",'tag_green')
        if isLinux:
            destinationLocation = DESTINATION_LOCATION_JULIE_LINUX
        else:
            destinationLocation = DESTINATION_LOCATION_JULIE_WIN
    else:
        txt_edit.insert(tk.END, "UNKNOWN OR MISSING PHONE - FIX AND TRY AGAIN\n",'tag_red')
        print(res)
        return
    
    # test to make sure computer and phone are on same time
    result = subprocess.run(['adb', 'shell', "date +'%Y-%m-%d %H:%M:%S'"], stdout=subprocess.PIPE)
    res = str(result)
    #print (res)
    
    if isLinux:
        res = res[res.find("=b'")+3:res.rfind("n")-1]
    else:
        res = res[res.find("=b'")+3:res.rfind("n")-3]
        
    phoneTime = datetime.strptime(res, '%Y-%m-%d %H:%M:%S')
    
    # Get current date and time
    now = datetime.now()
    computerTime = now
    timeDiff = computerTime - phoneTime

    
    if (abs(timeDiff.total_seconds()) > 600):
        txt_edit.insert(tk.END, "TIME ON PHONE / COMPUTER DON'T MATCH - FIX, RESTART, AND TRY AGAIN\n",'tag_red')
        print (timeDiff.total_seconds())
        return
        
    connectionOK = True

def test_copy():
    global isLinux
    global copyReady
    global destinationLocation
    global sourceLocation
    global workingOnCaptures
    
    txt_edit.insert(tk.END, "Please wait while things are compared . . .\n\n",'tag_green')
    txt_edit.update()
    
    # query the phone with a dryrun to diplay what will happen
    # do a dryrun of screencaptures to see what needs to be done
    #adbsync --dry-run --exclude *.trashed*  --exclude *.thumbnails* --del pull /sdcard/Pictures "/media/rick/BlogSD/Original Photos/Rick Phone"
    #needed to pipe stderr to the output to see what is going on
    result = subprocess.run(
    ['adbsync', 
    '--dry-run',
    '--exclude',
    '*.trashed*',
    '--exclude',
    '*.thumbnails*',
    '--del',
    'pull',
    sourceLocation,
    destinationLocation
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    res = str(result)
    
    # strip out all the stuff except the end
    res = res[res.find('SYNCING') + len('SYNCING'):-2]
    if not isLinux:
        res = res.replace("\\r","")
        res = res.replace("[INFO] ","")
    res = res.split(sep='\\n')

    emptyCopy = False
    emptyDelete = False
    step = 0
    totalDelete = 0
    totalCopy = 0
    deleteItems = ''
    copyItems = ''
    for item in res:
        #print(item)
        if item.strip() != '':
            if 'delete tree' in item:
                step = 1
            if 'unaccounted tree' in item:
                step = 2
                if 'Empty' in item:
                    emptyDelete = True
                    #print ("no delete")
            if 'copy tree' in item:
                step = 3
                if 'Empty' in item:
                    emptyCopy = True
                    #print ("no copy")
            if (step == 2) and not emptyDelete:
                totalDelete = totalDelete + 1
                deleteItems = deleteItems + item.strip() + '\n'
            if (step == 3) and not emptyCopy:
                totalCopy = totalCopy + 1
                copyItems = copyItems + item.strip() + '\n'
    
    if totalDelete > 0 or totalCopy > 0:
        txt_edit.insert(tk.END, 'Comparison details\n')
        txt_edit.insert(tk.END, '------------------\n')

    if totalDelete > 0:
        txt_edit.insert(tk.END, deleteItems + '\n')
    if totalCopy > 0:
         txt_edit.insert(tk.END, copyItems + '\n')

    #color code the lines based upon how many to copy
    if totalDelete < 20:
        tagDelete = 'tag_green'   
    elif totalDelete < 50:
        tagDelete = 'tag_orange'
    else:
        tagDelete = 'tag_red'
        
    if totalCopy < 100:
        tagCopy = 'tag_green'   
    elif totalCopy < 200:
        tagCopy = 'tag_orange'
    else:
        tagCopy = 'tag_red'

    txt_edit.insert(tk.END, 'Summary\n','tag_orange')
    txt_edit.insert(tk.END, '------------------\n','tag_orange')

    if totalDelete == 0:
        txt_edit.insert(tk.END, 'DELETE: No ' + imageType + ' to delete from the blog\n','tag_green')
    else:
        txt_edit.insert(tk.END, 'DELETE: Going to delete ' + str(totalDelete -1) + ' ' + imageType + ' from the blog\n',tagDelete)              
 
    if totalCopy == 0:
        txt_edit.insert(tk.END, 'COPY: No ' + imageType + 's to copy to the blog\n','tag_green')
    else:
        txt_edit.insert(tk.END, 'COPY: Going to copy ' + str(totalCopy - 1) + ' ' + imageType + ' to the blog\n',tagCopy)
   
    txt_edit.insert(tk.END, '------------------\n','tag_orange')

    if emptyCopy and emptyDelete:
        txt_edit.insert(tk.END, '\nYOU ARE DONE NOW - NOTHING TO DO!\n','tag_green')
        return
        
    if (totalDelete > 100) or (totalCopy > 300):
        txt_edit.insert(tk.END, '\nWARNING: This looks really big - ARE YOU SURE????\n','tag_red')
    
    txt_edit.insert(tk.END, '\nIf everything above looks fine then click the "Execute" button\n','tag_green')
    txt_edit.see('end')
    copyReady = True
    if workingOnCaptures:
        btn_capture_execute.config(state="normal")
    else:
        btn_photo_execute.config(state="normal")

def real_copy():
    global isLinux
    
    txt_edit.insert(tk.END, "\n\nPlease wait while everything runs for real. . .\n\n",'tag_green')
    txt_edit.see('end')
    txt_edit.update()

    # now go ahead and do the action
    #adbsync --dry-run --exclude *.trashed*  --exclude *.thumbnails* --del pull /sdcard/Pictures "/media/rick/BlogSD/Original Photos/Rick Phone"
    #needed to pipe stderr to the output to see what is going on
    result = subprocess.run(
    ['adbsync', 
    #'--dry-run',
    '--exclude',
    '*.trashed*',
    '--exclude',
    '*.thumbnails*',
    '--del',
    'pull',
    sourceLocation,
    destinationLocation
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    res = str(result)
    if not isLinux:
        res = res.replace("\\r","")
        res = res.replace("[INFO] ","")
    if 'SYNCING' not in res:
        txt_edit.insert(tk.END, "SOMETHING WENT WRONG - CHECK BELOW FOR ERROR\n\n",'tag_green')
        txt_edit.see('end')
        txt_edit.insert(tk.END, res + '\n','tag_red')
        return

    # strip out all the stuff except the end
    res = res[res.find('SYNCING'):-2]
    res = res.split(sep='\\n')
    
    for item in res:
        txt_edit.insert(tk.END, item.strip() + '\n')
    
    txt_edit.insert(tk.END, "ALL DONE!\n",'tag_green')
    txt_edit.see('end')

#-----------------------------------------------------------------------------------------------------

def test_screencapture():
  
    global imageType
    global destinationLocation
    global sourceLocation
    global connectionOK
    global workingOnCaptures

    btn_photo_execute.config(state="disabled")
    btn_capture_execute.config(state="disabled")    
    
    copyReady = False
    workingOnCaptures = True
     # clear the window
    txt_edit.delete("1.0","end")
    txt_edit.insert(tk.END, "Preparing to copy screencaptures\n",'tag_green')

    check_connection()
    if connectionOK:
 
        sourceLocation = SOURCE_LOCATION_CAPTURES
        imageType = "screencaptures"

        test_copy()
 


def copy_screencapture():
    global copyReady
    global workingOnCaptures

    txt_edit.insert(tk.END, "Copying screencaptures\n",'tag_green')

    if not copyReady or not workingOnCaptures:
        txt_edit.insert(tk.END, 'THE SCREENCAPTURE PREPARATION STEP WAS NOT COMPLETED SUCCESSFULLY\n','tag_red')
        txt_edit.insert(tk.END, 'Press the screencapture prepare button first - then try again\n','tag_red')
        txt_edit.see('end')
        return

    real_copy()
    copyReady = False
    btn_photo_execute.config(state="disabled")
    btn_capture_execute.config(state="disabled")

def test_photo():
    global imageType
    global destinationLocation
    global sourceLocation
    global connectionOK
    global workingOnCaptures

    copyReady = False
    workingOnCaptures = False
    
    btn_photo_execute.config(state="disabled")
    btn_capture_execute.config(state="disabled") 
      
     # clear the window
    txt_edit.delete("1.0","end")
    txt_edit.insert(tk.END, "Preparing to copy photos\n",'tag_green')

    check_connection()
    if connectionOK:

        sourceLocation = SOURCE_LOCATION_PHOTOS
        imageType = "photos"

        test_copy()

def copy_photo():
    global copyReady
    global workingOnCaptures
    
    txt_edit.insert(tk.END, "Copying photos\n")

    if not copyReady or workingOnCaptures:
        txt_edit.insert(tk.END, 'THE PHOTO PREPARATION STEP WAS NOT COMPLETED SUCCESSFULLY\n','tag_red')
        txt_edit.insert(tk.END, 'Press the photo prepare button first - then try again\n','tag_red')
        txt_edit.see('end')
        return

    real_copy()
    copyReady = False
    btn_photo_execute.config(state="disabled")
    btn_capture_execute.config(state="disabled")

#-----------------------------------------------------------------------------------------------------

window = tk.Tk()
window.minsize(width=500, height=500)
window.title("Copy photos from phone to blog memory stick (" + APPLICATION_VERSION + ")")
window.rowconfigure(0, minsize=700, weight=1)
window.columnconfigure(1, minsize=100, weight=1)
window.geometry("1500x700+0+0")

the_image = tk.PhotoImage(data=image_data)
window.tk.call('wm', 'iconphoto', window._w, the_image)

copyReady = False
workingOnCaptures = False
connectionOK = False
destinationLocation = ''
sourceLocation = ''
imageType = ''

txt_edit = tk.Text(window)


    
# Create scrollbar
txt_edit.tag_configure("tag_red", foreground = "red",font=("Arial", 12, 'bold'))
txt_edit.tag_configure("tag_green", foreground = "green",font=("Arial", 12, 'bold'))
txt_edit.tag_configure("tag_orange", foreground = "DarkOrange1",font=("Arial", 12, 'bold'))

scrollbar = tk.Scrollbar(window, command=txt_edit.yview)
scrollbar.config (width = 30)
#scrollbar.pack(side="right", fill="y")

# Configure text box to use scrollbar
txt_edit.config(yscrollcommand=scrollbar.set)

frm_buttons = tk.Frame(window, relief=tk.RAISED,bg='gray95', bd=2)

lbl_screencapture = tk.Label(frm_buttons, text="Screen Captures",bg='gray95')
btn_capture_prepare = tk.Button(frm_buttons, text="Prepare", command=test_screencapture)
btn_capture_execute = tk.Button(frm_buttons, text="Execute", command=copy_screencapture)

lbl_screencapture.grid(row=0, column=0, sticky="ew", padx=10, pady=(25,10))
btn_capture_prepare.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
btn_capture_execute.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

lbl_photo = tk.Label(frm_buttons, text="Photos",bg='gray95')
btn_photo_prepare = tk.Button(frm_buttons, text="Prepare", command=test_photo)
btn_photo_execute = tk.Button(frm_buttons, text="Execute", command=copy_photo)

lbl_photo.grid(row=3, column=0, sticky="ew", padx=10, pady=(50,10))
btn_photo_prepare.grid(row=4, column=0, sticky="ew", padx=10, pady=10)
btn_photo_execute.grid(row=5, column=0, sticky="ew", padx=10, pady=10)

frm_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")
scrollbar.grid(row=0, column=2, sticky="ns")

os_name = platform.system()
isLinux = ('Linux' in os_name)

txt_edit.insert(tk.END, 'Press one of the buttons on the left to get started!\n',"tag_green")

# disable the execute buttons until the prepare step is completed
btn_photo_execute.config(state="disabled")
btn_capture_execute.config(state="disabled")

# put the icon into the terminal window
# with open("camera-photo-2.ico", "rb") as image:
     # a = image.read()
# print(repr(a))

window.mainloop()


