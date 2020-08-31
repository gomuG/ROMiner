
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import os
import CustomLogger
import gUtil
import logging
import time

logging.basicConfig(level=logging.DEBUG, datefmt='%d-%m-%Y %H:%M:%S')
logger = CustomLogger.logger
#logger = logging.getLogger(__name__)


# Layout
# Patch Link: [Patch ID]                           [Combo Server list][Checkbox]
# 1. APK Path:                      [Textbox]      [BrowseBtn][Checkbox]
# 2. Unity Folder Path:             [Textbox]      [BrowseBtn][Checkbox]
# 3. Decrypted Unity Folder Path:   [Textbox]      [BrowseBtn][Checkbox]
#
# [Start Btn]         [Help Btn]                    
# [Logs]
# [Logs]
#                                                   [Credit]

# Declare Variables
winHeight = 480
winWidth = 680
pathTBChWidth = 60
apkFilePath = ""
unityFolderPath = ""
decUtFolderPath = ""
patchLinkID = ""
# apkBool = tkinter.IntVar()
# unityBool  = tkinter.IntVar()
# decUtBool = tkinter.IntVar()





# Callback functions for buttons
# Browse and copy to text label, specialised for apk
def BrowseFileFunc(label:str, labelobj):
    filename = tkinter.filedialog.askopenfilename(initialdir=os.getcwd(),title = "Select APK",filetypes = (("apk files","*.apk"),("all files","*.*")),multiple=0)
    label=filename
    labelobj.delete(0,"end")
    labelobj.insert(0, label)

def BrowseDirFunc(label:str,labelobj):
    directory = tkinter.filedialog.askdirectory(initialdir=os.getcwd(),mustexist=1)
    label = directory
    labelobj.delete(0,"end")
    labelobj.insert(0, label)

def ValidateURL(url:str, checkboxObj:tkinter.Checkbutton):
    if not gUtil.validateURL(url):
        ErrorMessage("Invalid Url/server!")
        checkboxObj.deselect()

def SetWidgetState(widget,p_bool:bool, isReadOnly:bool=False):
    if p_bool:
        widget.configure(state="normal")
        if isReadOnly:
            widget.configure(state="readonly")
    else:
        widget.configure(state="disabled")
    
def ToggleSelfPL(p_bool):
    SetWidgetState(patchLink_TBox, p_bool)
    SetWidgetState(patchLink_CBBtn, p_bool, True)


def ToggleAPK(p_bool):
    SetWidgetState(apkPath_BwBtn, p_bool)
    SetWidgetState(apkPath_TBox, p_bool)
    SetWidgetState(apkPath_ChBtn, p_bool)

    
def TogglePL(p_bool):
    SetWidgetState(patchLink_TBox, p_bool)
    SetWidgetState(patchLink_CBBtn, p_bool, True)
    SetWidgetState(patchLink_ChBtn, p_bool)

def ToggleUT(p_bool):
    SetWidgetState(unityPath_TBox, p_bool)
    SetWidgetState(unityPath_BwBtn, p_bool)
    
def ToggleDecUT(p_bool):
    SetWidgetState(decUtPath_TBox, p_bool)
    SetWidgetState(decUtPath_BwBtn, p_bool)


def PLCB():
    ValidateURL(gUtil.GetPatchLink(patchLink_CBBtn.get(), patchLink_TBox.get()),patchLink_ChBtn)
    ToggleAPK(not patchBool.get())
    ToggleUT(not patchBool.get())
    ToggleDecUT(not patchBool.get())
    ToggleSelfPL(not patchBool.get())

    
def APKCB():
    TogglePL(not apkBool.get())
    ToggleUT(not apkBool.get())
    ToggleDecUT(not apkBool.get())


################################################################################
# Start window creation

# Main Window
window = tkinter.Tk()
window.title("ROM Extractor GUI")
window.geometry(str(winWidth)+'x'+str(winHeight))
window.resizable(False, False)

apkBool = tkinter.IntVar()
unityBool  = tkinter.IntVar()
decUtBool = tkinter.IntVar()
patchBool = tkinter.IntVar()

def ErrorMessage(p_msg:str):
    #tkinter.messagebox.showwarning(title="Warning!", message=p_msg)
    logger.error(p_msg)
    return

# Credit
creditLabel = tkinter.Label(window, text="Discord: Gomu#4730\n#TeamLeaks", justify="right")
creditLabel.place(x=winWidth-120, y=winHeight-40)

spacer = tkinter.Label(window, text="")    #add space
spacer.grid(column=0,row=0)


patchLink_Lbl = tkinter.Label(window, text="Patch Link:",justify="left")
patchLink_Lbl.grid(column=0,row=1,sticky="w")
patchLink_TBox = tkinter.Entry(window, exportselection=0,justify="left",textvariable=patchLinkID, width=pathTBChWidth)
patchLink_TBox.grid(column=1,row=1)
patchLink_CBBtn = tkinter.ttk.Combobox(window, values=["SEA", "CN", "GLOBAL", "Others"], width = 7, state="readonly")
patchLink_CBBtn.grid(column=2,row=1)
patchLink_ChBtn = tkinter.Checkbutton(window, variable=patchBool, command=lambda:PLCB(),width=5 )
patchLink_ChBtn.grid(column=3,row=1)



# Line 1
line1row = 2
apkPath_Lbl = tkinter.Label(window, text="1. APK File Path:",justify="left")
apkPath_Lbl.grid(column=0,row=line1row,sticky="w")
apkPath_TBox = tkinter.Entry(window, exportselection=0,justify="left",textvariable=apkFilePath, width=pathTBChWidth)
apkPath_TBox.grid(column=1,row=line1row)
apkPath_BwBtn = tkinter.Button(window, text="Browse",command=lambda: BrowseFileFunc(apkFilePath,apkPath_TBox))
apkPath_BwBtn.grid(column=2,row=line1row)
apkPath_ChBtn = tkinter.Checkbutton(window, variable=apkBool, command=lambda:APKCB())
apkPath_ChBtn.grid(column=3,row=line1row)

# Line 2
unityPath_Lbl = tkinter.Label(window, text="2. Unity Folder Path:",justify="left")
unityPath_Lbl.grid(column=0,row=line1row+1,sticky="w")
unityPath_TBox = tkinter.Entry(window, exportselection=0,justify="left",textvariable=unityFolderPath, width=pathTBChWidth)
unityPath_TBox.grid(column=1,row=line1row+1)
unityPath_BwBtn = tkinter.Button(window, text="Browse",command=lambda: BrowseDirFunc(unityFolderPath,unityPath_TBox))
unityPath_BwBtn.grid(column=2,row=line1row+1)
unityPath_ChBtn = tkinter.Checkbutton(window, variable=unityBool)
unityPath_ChBtn.grid(column=3,row=line1row+1)

# Line 3
decUtPath_Lbl = tkinter.Label(window, text="3. Bytes Folder Path:",justify="left")
decUtPath_Lbl.grid(column=0,row=line1row+2,sticky="w")
decUtPath_TBox = tkinter.Entry(window, exportselection=0,justify="left",textvariable=decUtFolderPath, width=pathTBChWidth)
decUtPath_TBox.grid(column=1,row=line1row+2)
decUtPath_BwBtn = tkinter.Button(window, text="Browse",command=lambda: BrowseDirFunc(decUtFolderPath,decUtPath_TBox))
decUtPath_BwBtn.grid(column=2,row=line1row+2)
decUtPath_ChBtn = tkinter.Checkbutton(window, variable=decUtBool)
decUtPath_ChBtn.grid(column=3,row=line1row+2)

spacer = tkinter.Label(window, text="") ## add space
spacer.grid(column=0,row=line1row+3)

status_btn = tkinter.Label(window, text="Status: Waiting for input")
status_btn.grid(column=1, row=line1row+5,sticky="w")

def SetStatus(string):
    status_btn.configure(text="Status: "+string)
    window.update()

# Run Extractor
def StartBtnCB():
    noneSelected = patchBool.get() + apkBool.get()+ unityBool.get()+decUtBool.get()
    if not noneSelected:
        ErrorMessage("No action selected!")
        return
    tempFolder = gUtil.GetOutputFolder(os.getcwd())
    apkFilePath = apkPath_TBox.get()
    unityFolderPath = unityPath_TBox.get()
    decUtFolderPath = decUtPath_TBox.get()

    # either get patch file or apk
    if patchBool.get() == 1:
        SetStatus("Downloading patch")
        zfPath = gUtil.DownloadPatchFile(patchLink_CBBtn.get(),patchLink_TBox.get(), tempFolder)
        zfName = gUtil.UnloadZip(zfPath, tempFolder)
        unityFolderPath = os.path.join(tempFolder,zfName)
    elif apkBool.get() == 1:
        logger.info("ApkFilePath: %s" %apkFilePath)
        gUtil.UnloadAPK(apkFilePath, tempFolder)

    if unityBool.get() == 1:
        SetStatus("Unpacking unity file into bytes file")
        logger.info("unity: %s" %unityFolderPath)
        gUtil.unpack_all_assets(unityFolderPath, tempFolder)
        decUtFolderPath = tempFolder
    if decUtBool.get() == 1:
        SetStatus("Decrypting bytes file")
        logger.info("decrypt: %s" %decUtFolderPath)
        rsp = gUtil.DecryptLuaFiles(decUtFolderPath, window)
        if not rsp:
            logger.error("Make sure ROMEncryption.exe/unluac.jar is in the same folder as this file")
        
    SetStatus('Waiting for input')
    logger.info('Completed downloading patch: %s'%patchLink_TBox.get())

start_btn = tkinter.Button(window, text="Extract", command=StartBtnCB,height=2,width=15)
start_btn.grid(column=0, row=line1row+5,sticky="w")


spacer = tkinter.Label(window, text="") ## add space
spacer.grid(column=0,row=line1row+6)
warning_label = tkinter.Label(window, text="Warning! Programming may freeze while decrypting. Do not close the program!", fg='red')
warning_label.grid(column=1, row=line1row+6,sticky="w")
# Console ==============

console_frame = tkinter.LabelFrame(window, text="Console")
console_frame.grid(column=0,row=line1row+7,columnspan=8)
console = CustomLogger.ConsoleUi(console_frame)
gUtil.ValidateJava();

sCount = 0
if not os.path.exists(os.path.join(os.getcwd(),"RomEncryption.exe")):
    logger.error("Cannot find RomEncryption.exe.")
else:
    sCount +=1
    logger.info("Located RomEncryption.exe")
if not os.path.exists(os.path.join(os.getcwd(),"Unluac.jar")):
    logger.error("Cannot find unluac.jar.")
else:
    sCount +=1
    logger.info("Located unluac.jar")

if sCount == 2:
    logger.info("Loaded successfully")
else:
    logger.info("Ensure the missing files are in the same folder as this file")

window.mainloop()