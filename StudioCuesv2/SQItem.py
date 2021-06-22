from threading import Timer
class SQItem:
	Title:str
	TimerSecondsRemaining:int
	TimerIsEnabled:bool
	ItemSkipped:bool
	TimerObj:Timer = None
	def __init__(this, Title, TimerSeconds = 210, TimerEnabled = False, Skipped = False):
		this.Title = Title
		this.TimerSecondsRemaining = TimerSeconds
		this.TimerIsEnabled = TimerEnabled
		this.ItemSkipped = Skipped
	def startTimer(this, timerCallback):
		this.TimerObj = Timer(float(this.TimerSecondsRemaining), timerCallback)
		this.TimerObj.start()
	def Skip(this):
		if this.TimerObj is not None:
			this.TimerObj.cancel()
		this.ItemSkipped = True