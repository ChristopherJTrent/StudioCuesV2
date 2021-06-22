from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog
import screeninfo
import configparser
import collections
from SQItem import SQItem
from ENUM import enum as e
class masterWindow:
	configuration = ""
	version = "2.0.0"	

	def __init__(this,master=None):
		this.SlaveWindowDanceLists = {
							    'current':{'content': StringVar(),'locked':False},
								'next1':{'content':StringVar(),'locked':False},
								'next2':{'content':StringVar(),'locked':False},
								'next3':{'content':StringVar(),'locked':False},
								'next4':{'content': StringVar(),'locked':False}}

		this.defaultConfigOptions = {'UI_UX':{
							'font_family':'Helvetica',
							'font_size':'110',
							'font_size_small':'80',
							'listbox_font_size':'12',
							'tablet_listbox_font_size':'40',
							'slave_window_background':'#300A24',
							'slave_window_foreground':'#FFFFFF',
							'slave_window_active_background':'#300A24',
							'slave_window_active_foreground':'#FFC83D',
							'master_window_background':'#300A24',
							'master_window_foreground':'#FFFFFF',
							'data_entry_background':'#55113F',
							'data_entry_foreground':'#FFFFFF',
							'currently_playing':'Now Playing:'
						},'startup':{
							'defaultqueue':'none'
						},'keybindings':{
							'savequeue':'<Control-s>',
							'openqueue':'<Control-o>',
							'enqueue':'<Key-q>',
							'enqueuetimer': '<Key-e>',
							'enqueuetop':'<Key-t>',
							'advancequeue':'<Key-n>',
							'additem':'<Control-a>'
						},'modules':{
							'tablet_mode_enabled':'false'}}
		master.title("StudioCues")
		this.doConfigRead()
		this.writeDefaultConfigValuesIfNotPresent()
		this.doStyleSetup()
		this.SlaveWindow = Toplevel(master)
		this.SlaveWindow.title("StudioCues Slave Window")
		this.danceQueue = collections.deque()
		this.MasterDanceList = this.getDanceStylesFromFile()
		this.initSlaveWindow()
		this.prep(master)

	def doStyleSetup(this):
		style = ttk.Style()
		style.configure(".", 				  
				  background=this.configuration[e.UX][e.SBG], 
				  foreground=this.configuration[e.UX][e.SFG])
		style.configure("TFrame",
				  background=this.configuration[e.UX][e.SBG], 
				  foreground=this.configuration[e.UX][e.SFG])
		style.configure("SW.TFrame",
				  font=(this.configuration[e.UX][e.FF],this.configuration[e.UX][e.FS]))		
		style.configure("SW.TLabel", 
				  font=(this.configuration[e.UX][e.FF],this.configuration[e.UX][e.FS]),
				  					justify=CENTER,
									anchor=CENTER)
		style.configure("T.SW.TLabel",
				  foreground=this.configuration[e.UX]['slave_window_active_foreground'])
		style.configure("TButton",
				  relief=GROOVE,
				  background=this.configuration[e.UX][e.MBG],
				  foreground=this.configuration[e.UX][e.MFG])
	def doConfigRead(this):
		configFile = open('StudioCues.configuration', 'r+')
		this.configuration = configparser.ConfigParser()
		this.configuration.read_file(configFile)
		#for sect in this.configuration.keys():
		#	print(sect,":")
		#	for opt in this.configuration[sect].keys():
		#		print(' '+opt+': '+this.configuration[sect][opt])
		configFile.close()

	def writeDefaultConfigValuesIfNotPresent(this): 
		for k1 in this.defaultConfigOptions:
			if not this.configuration.has_section(k1):	
				this.configuration.add_section(k1)
			for k2 in this.defaultConfigOptions[k1]:
				if not this.configuration.has_option(k1, k2):
					this.configuration.set(k1, k2, this.defaultConfigOptions[k1][k2])
		this.writeConfiguration()

	def initSlaveWindow(this):
		this.SlaveWindow.geometry("500x500")
		this.CurrentDance = StringVar()
		this.CurrentDanceLabel = ttk.Label(this.SlaveWindow,
									style="T.SW.TLabel",
									textvariable=this.CurrentDance)
		this.nextDance1 = StringVar()
		this.nextDance2 = StringVar()
		this.nextDance3 = StringVar()
		this.nextDance4 = StringVar()
		this.NextDanceLabel1 = ttk.Label(this.SlaveWindow,
									textvariable=this.nextDance1,
									style = "SW.TLabel")		
		this.NextDanceLabel2 = ttk.Label(this.SlaveWindow,
									style='SW.TLabel',
									textvariable=this.nextDance2)		
		this.NextDanceLabel3 = ttk.Label(this.SlaveWindow,
									style='SW.TLabel',
									textvariable=this.nextDance3)		
		this.NextDanceLabel4 = ttk.Label(this.SlaveWindow,
									style='SW.TLabel',
									textvariable=this.nextDance4)
		this.CurrentDanceLabel.pack(side=TOP,fill=BOTH,expand=1)
		this.NextDanceLabel1.pack(side=TOP,fill=BOTH, expand=1)
		this.NextDanceLabel2.pack(side=TOP,fill=BOTH, expand=1)
		this.NextDanceLabel3.pack(side=TOP,fill=BOTH, expand=1)
		this.NextDanceLabel4.pack(side=TOP,fill=BOTH, expand=1)
		attemptAutoSize = messagebox.askyesno("StudioCues V2", "Would you like to let the software automatically determine the size and position of your display?")
		if(attemptAutoSize):
			for mon in screeninfo.screeninfo.get_monitors():
				if mon.x > 0:
					#print(str(mon.x) + " " + str(mon.y) + " " + str(mon.height) + " " + mon.name)
					this.SlaveWindow.geometry(f"{mon.width}x{mon.height}+{mon.x}+{mon.y}")
					this.SlaveWindow.overrideredirect(1)
		else:
			for mon in screeninfo.screeninfo.get_monitors():
				if mon.x > 0:
					if messagebox.askyesno("StudioCues", f"Is {mon.name} the correct monitor?"):
						width = simpledialog.askinteger("StudioCues", f"What is the width of {mon.name} in pixels?")
						height = simpledialog.askinteger("StudioCues",f"What is the height of {mon.name} in pixels?")
						this.SlaveWindow.geometry(f"{width}x{height}+{mon.x}+0")
						this.SlaveWindow.overrideredirect(1)
						break

	def writeConfiguration(self, location='StudioCues.configuration'):
		with open(location, 'w+') as configFile:
			self.configuration.write(configFile)

	def getDanceStylesFromFile(self, file='DanceStyles.list') -> dict:
		outDictionary = {}
		iterator = 0
		dances = open(file,'r')
		danceList = dances.read().split('\n')
		for dance in danceList:
			outDictionary[iterator] = dance
			iterator += 1
		dances.close()
		return outDictionary
	def updateSlaveDanceLabels(this):
		width = len(this.danceQueue)
		if width >= 5:
			this.nextDance4.set(this.danceQueue[4].Title)
		else:
			this.nextDance4.set("")
		
		if width >= 4:
			this.nextDance3.set(this.danceQueue[3].Title)
		else:
			this.nextDance3.set("")
		
		if width >= 3:
			this.nextDance2.set(this.danceQueue[2].Title)
		else:
			this.nextDance2.set("")

		if width >= 2:
			this.nextDance1.set(this.danceQueue[1].Title)
		else:
			this.nextDance1.set("")

		if width >= 1:
			this.CurrentDance.set(this.danceQueue[0].Title)
		else:
			this.CurrentDance.set("")
	def addDanceToQueue(this, Dance:SQItem):
		this.danceQueue.append(Dance)
		if len(this.danceQueue) == 1 and this.danceQueue[0].TimerIsEnabled:
			this.danceQueue[0].startTimer(this.advanceDanceQueue)
		this.updateSlaveDanceLabels()
		this.updateMasterWindowDanceQueueLabel()
	def addDanceToTop(this, Dance:SQItem):
		if Dance.TimerIsEnabled:
			Dance.startTimer(this.advanceDanceQueue)
		this.danceQueue.appendleft(Dance)
		this.updateSlaveDanceLabels()
		this.updateMasterWindowDanceQueueLabel()

	def advanceDanceQueue(this):
		t = this.danceQueue.popleft()
		t.Skip()
		if len(this.danceQueue) > 0 and this.danceQueue[0].TimerIsEnabled:
			this.danceQueue[0].startTimer(this.advanceDanceQueue)
		this.updateSlaveDanceLabels()
		this.updateMasterWindowDanceQueueLabel()

	def removeLastAddedDance(this):
		dance :SQItem = this.danceQueue.pop()	
		dance.Skip()
		this.updateSlaveDanceLabels()
		this.updateMasterWindowDanceQueueLabel()

	def createQueueLabelText(this) -> str:
		outputString = ""
		outputString+= this.configuration['UI_UX']['currently_playing'] + '\n'
		for dance in this.danceQueue:
			outputString+=dance.Title + '\n'
		return outputString

	def updateMasterWindowDanceQueueLabel(this):
		this.danceQueueLabelText.set(this.createQueueLabelText())

	def registerNewDance(this, Dance:str):
		this.registerNewDanceTemp(Dance)
		with (open('DanceStyles.list','a')) as listFile:
			listFile.write('\n' + Dance)

	def registerNewDanceTemp(this, Dance:str):
		index = max(this.MasterDanceList.keys()) + 1
		this.MasterDanceList[index] = Dance
		this.DanceListbox.insert(index, Dance)

	def doFileOpenPopup(self, startDir:str='/', title:str='Select a file...', fileTypes:tuple=(('StudioCues Queue files','*.sc'),('All Files','*.*'))) -> str:
		return filedialog.askopenfilename(initialdir=startDir, title=title,filetypes=fileTypes)	

	def doFileSavePopup(self, startDir:str='/', title:str='Select a file...', fileTypes:tuple=(('StudioCues Queue files','*.sc'),('All Files','*.*'))) -> str:
		return filedialog.asksaveasfilename(initialdir=startDir, title=title,filetypes=fileTypes)
	def saveCurrentQueue(this):
		location = this.doFileSavePopup()
		if not location.endswith(('.sc','.SC','.Sc','.sC')):
			location+='.sc'
		with open(location, 'w') as queueFile:
			for v in this.danceQueue:
				queueFile.write(f"{v.Title},{v.TimerSecondsRemaining}\n")
	def readQueueFile(this):
		location = this.doFileOpenPopup()
		with open(location,'r') as IOFile:
			this.danceQueue.clear()
			this.updateSlaveDanceLabels()
			for line in IOFile:
				Title, Secs = line.split(',')
				this.addDanceToQueue(SQItem(Title, Secs))
			this.updateSlaveDanceLabels()


	def updateDanceList(this):
		location = this.doFileOpenPopup()
		this.MasterDanceList = this.getDanceStylesFromFile(location)
		this.DanceListbox.delete(0,END)
		for key in this.MasterDanceList.keys():
			this.DanceListbox.insert(key, this.MasterDanceList[key])

	def clearDanceQueue(this):
		this.CurrentDance.set('')
		this.nextDance1.set('')
		this.nextDance2.set('')
		this.nextDance3.set('')
		this.nextDance4.set('')
		for d in this.danceQueue:
			d.TimerIsEnabled = False
			d.ItemSkipped = True
		this.danceQueue.clear()

	def createMenuBar(this, root:Tk):
		this.menuBar = Menu(root)
		this.FileMenu = Menu(this.menuBar, tearoff=0)
		this.FileMenu.add_command(label='Save Queue (CTRL+S)',underline=1,command=this.saveCurrentQueue)
		this.FileMenu.add_command(label='Open Queue (CTRL+O)',underline=1, command=this.readQueueFile)
		this.menuBar.add_cascade(label="File",menu=this.FileMenu)
		root.config(menu=this.menuBar)

	def createDanceRegistrationArea(this, root:Tk):
		this.RegisterDanceArea = Frame(root)
		this.RegisterDanceActionArea = Frame(this.RegisterDanceArea)
		this.RegisterDanceTextBox = Entry(this.RegisterDanceArea)
		this.RegisterDancePermanentButton = Button(this.RegisterDanceActionArea,
												text="Add dance\n(Permanent)",
												command=lambda:this.registerNewDance(this.RegisterDanceTextBox.get()))
		this.RegisterDanceTemporaryButton = Button(this.RegisterDanceActionArea,
												text="Add dance \n(Temp)",
												command=lambda:this.registerNewDanceTemp(this.RegisterDanceTextBox.get()))
		this.RegisterDancePermanentButton.pack(side=TOP, fill=BOTH, expand=1)
		this.RegisterDanceTemporaryButton.pack(side=TOP, fill=BOTH, expand=1)
		this.RegisterDanceTextBox.pack(side=LEFT, fill=BOTH, expand=1)
		this.RegisterDanceActionArea.pack(side=LEFT, fill=BOTH, expand=1)
		this.RegisterDanceArea.pack(side=TOP, fill=X, expand=0)

	def createTimerSetupArea(this, root:Tk):
		this.TimerSetupArea = Frame(root)
		this.MinuteArea = Frame(this.TimerSetupArea)
		this.SecondArea = Frame(this.TimerSetupArea)
		this.TimerMinuteInput:IntVar = IntVar(this.MinuteArea, 0)
		this.TimerSecondInput:IntVar = IntVar(this.SecondArea, 0)
		this.TimerMinuteInputBox = Spinbox(this.MinuteArea,
								  from_=0,
								  to=60,
								  textvariable=this.TimerMinuteInput)
		this.TimerSecondInputBox = Spinbox(this.SecondArea,
								  from_=0,
								  to=60,
								  textvariable=this.TimerSecondInput)
		this.MinuteLabel = Label(this.MinuteArea, text='Minutes')		
		this.SecondLabel = Label(this.SecondArea, text='Seconds')
		this.TimerMinuteInputBox.pack(side=TOP, fill=BOTH, expand=1)
		this.TimerSecondInputBox.pack(side=TOP, fill=BOTH, expand=1)
		this.MinuteLabel.pack(side=TOP, fill=BOTH, expand=1)
		this.SecondLabel.pack(side=TOP, fill=BOTH, expand=1)
		this.MinuteArea.pack(side=LEFT, fill=X, expand=0)
		this.SecondArea.pack(side=LEFT, fill=X, expand=0)
		this.TimerSetupArea.pack(side=TOP, fill=X, expand=0)

	def createDanceListArea(this, root:Tk):
		this.listArea = Frame(root)
		this.DanceListboxScroll = Scrollbar(this.listArea)
		this.DanceListboxScroll.pack(side=LEFT,fill=Y)
		this.DanceListbox = Listbox(this.listArea,
								yscrollcommand=this.DanceListboxScroll.set)
		this.DanceListboxScroll.config(command=this.DanceListbox.yview)
		this.danceQueueLabelText = StringVar(root)
		this.danceQueueLabelText.set(this.createQueueLabelText())
		this.danceQueueLabel = Label(this.listArea, textvariable=this.danceQueueLabelText)
		for key in this.MasterDanceList.keys():
			this.DanceListbox.insert(key, this.MasterDanceList[key])
		this.DanceListbox.pack(side=LEFT, fill=BOTH,expand=1)
		this.danceQueueLabel.pack(side=LEFT,fill=BOTH,expand=0)
		this.listArea.pack(side=TOP,fill=BOTH,expand=1)

	def createDanceControlArea(this, root:Tk):
		this.controlArea :Frame = Frame(root)
		this.addDanceArea :Frame = Frame(this.controlArea)
		this.addTimerDanceArea :Frame = Frame(this.controlArea)
		this.AddDanceButton :Button = Button(this.addDanceArea,
							   text="Add to Queue",
							   command=lambda:this.addDanceToQueue(this.createDanceEntryForCurrentSelection()))		
		this.AddDanceToTopButton :Button = Button(this.addDanceArea,
							   text="Add to top \nof Queue",
							   command=lambda:this.addDanceToTop(this.createDanceEntryForCurrentSelection()))
		this.AddDanceTimerButton :Button = Button(this.addTimerDanceArea,
										   text="Add to Queue\n(Timer)",
										   command=lambda:this.addDanceToQueue(this.createDanceEntryWithTimerForCurrentSelection()))
		this.addDanceTimerToTopButton :Button = Button(this.addTimerDanceArea,
												text="Add to top\nof Queue (Timer)",
												command=lambda:this.addDanceToTop(this.createDanceEntryWithTimerForCurrentSelection()))
		this.AdvanceDanceButton = Button(this.controlArea,
								  text="Next Dance",
								command=this.masterWindowNextDanceCallback)
		this.RemoveLastDanceButton = Button(this.controlArea,
										text="Remove the \nLast Dance",
										command=this.masterWindowRemoveLastAddedDanceCallback)
		this.AddDanceToTopButton.pack(side=TOP,fill=BOTH, expand=0)
		this.AddDanceButton.pack(side=TOP,fill=BOTH, expand=1)
		this.addDanceTimerToTopButton.pack(side=TOP, fill=BOTH, expand=1)
		this.AddDanceTimerButton.pack(side=TOP, fill=BOTH, expand=1)
		this.addDanceArea.pack(side=LEFT, fill=BOTH, expand=1)
		this.addTimerDanceArea.pack(side=LEFT,fill=BOTH, expand=1)
		this.AdvanceDanceButton.pack(side=LEFT, fill=BOTH, expand=1)
		this.RemoveLastDanceButton.pack(side=LEFT, fill=BOTH, expand=1)
		this.controlArea.pack(side=TOP,fill=BOTH,expand=0)

	def createDanceEntryForCurrentSelection(this) -> SQItem:
		return SQItem(this.DanceListbox.get(this.DanceListbox.curselection()))
	def createDanceEntryWithTimerForCurrentSelection(this) -> SQItem:
		output = SQItem(this.DanceListbox.get(this.DanceListbox.curselection()))
		output.TimerSecondsRemaining = this.TimerMinuteInput.get() * 60 + this.TimerSecondInput.get()
		output.TimerIsEnabled = True
		return output
	def prep(this, root:Tk):
		this.createMenuBar(root)
		#this.createDanceRegistrationArea(root)
		this.createTimerSetupArea(root)
		this.createDanceListArea(root)
		this.createDanceControlArea(root)
		this.registerKeyCommands(root)

	def registerKeyCommands(this, root:Tk):
		root.bind(this.configuration['keybindings']['openqueue'], lambda event: this.readQueueFile())
		root.bind(this.configuration['keybindings']['savequeue'], lambda event: this.saveCurrentQueue())
		root.bind(this.configuration['keybindings']['enqueue'], lambda event:this.addDanceToQueue(this.createDanceEntryForCurrentSelection()))		
		root.bind(this.configuration['keybindings']['enqueuetop'], lambda event:this.addDanceToTop(this.createDanceEntryForCurrentSelection()))
		root.bind(this.configuration['keybindings']['advanceQueue'], lambda event:this.advanceDanceQueue())
		this.TimerMinuteInputBox.unbind("<key>")


	def masterWindowAddDanceCallback(this, index:int):

		this.addDanceToQueue(index)

	def masterWindowNextDanceCallback(this):
		this.advanceDanceQueue()

	def masterWindowRemoveLastAddedDanceCallback(this):
		this.removeLastAddedDance()
	
	def changeDanceListCallback(this):
		pass
	def __TextBoxOverrideCallback(this, event):
		#print(__name__)
		if type(event.widget) == type(Entry()):
			event.widget.insert(len(event.widget.get()), event.char)
		return 'break'

def main():
	root = Tk()
	master = masterWindow(root)
	root.mainloop()
	master.writeConfiguration()

main()