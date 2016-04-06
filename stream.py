from Tkinter import *
from tkFileDialog import *
import sys
import csv
import os
from time import strftime, gmtime, sleep, time
from socket import *
import thread
import threading


def loadFile():
	fname = askopenfilename(parent=root)
	dialogTextBox.insert(0, os.path.split(fname)[0])

def testConnection():
	newSocket = socket(AF_INET, SOCK_STREAM)
	try:
		newSocket.connect((Entry.get(serverTextBox),int(Entry.get(portTextBox))))
		testConn['text'] = 'Success'
	except:
		testConn['text'] = 'Failed'
	newSocket.shutdown(0)
	newSocket.close()

def stream(filePath):
	newSocket = socket(AF_INET, SOCK_STREAM)
	newSocket.connect((Entry.get(serverTextBox),int(Entry.get(portTextBox))))

	dataSent = 0
	while True:
		csvFile = open(filePath, 'rb')
		csvReader = csv.reader(csvFile)
		if skip.get() == 1:
		 	next(csvReader)

		for item in csvReader:
			if Entry.get(timeFieldIndexTextBox): 
			 	item[int(Entry.get(timeFieldIndexTextBox))] = strftime("%d-%b-%Y %H:%M:%S", gmtime())
			else:
				item.insert(0,strftime("%d-%b-%Y %H:%M:%S", gmtime()))
			values = ','.join(item)
			newSocket.send(values + '\n')
			dataSent += 1
			if dataSent == int(Spinbox.get(eventsPerSecond)):
				sleep(int(Entry.get(timeTextBox))/1000.0)
				dataSent = 0

		if checked.get() == 0:
			break

	newSocket.shutdown(0)
	newSocket.close()

def threadStream():
	csvList = []
	dirPath = Entry.get(dialogTextBox)
	for dirn, dirnames, filenames in os.walk(dirPath):
		for filename in filenames:
			if filename.endswith('.csv'):
				csvList.append(os.path.join(dirPath, filename))
	seeStream.set("Streaming data....")

	for csvs in csvList:
		sleep(.1)
		lock = threading.Lock()
		with lock:
			thread.start_new_thread(stream,(csvs,))

def stop():
	sys.exit()
	

root = Tk()
root.wm_title("CSV Data Steam")

topFrame = Frame(root, bd=1, relief=SUNKEN, padx=10, pady=10)
topFrame.grid(row=0)
serverLabel = Label(topFrame, text='Server:  ')
serverLabel.grid(row=0, sticky=E)
defaultServer = StringVar()
serverTextBox = Entry(topFrame, width=40, textvariable=defaultServer)
defaultServer.set('localhost')
serverTextBox.grid(row=0, column=1)

defaultPort = StringVar()
portTextBox = Entry(topFrame, width=10, textvariable=defaultPort)
defaultPort.set('5577')
portTextBox.grid(row=0, column=2, padx=(5,5))

testConn = Button(topFrame, text='Test Conection', width=15, command=testConnection)
testConn.grid(row=0, column=3)

dialogButton = Button(topFrame, text='Open Dialog',width=15, command=loadFile)
dialogButton.grid(row=1, column=3, padx=(5,5))
dialogLabel = Label(topFrame, text='CSV Path:  ')
dialogLabel.grid(row=1)
dialogTextBox = Entry(topFrame, width=50)
dialogTextBox.grid(row=1, columnspan=3, sticky=E)

containerFrame = Frame(root)
containerFrame.grid(row=3)

eventsFrame = Frame(containerFrame, relief=SUNKEN, padx=10, pady=10)
eventsFrame.grid(row=3)
events = StringVar()
#eventsPerSecond = Entry(eventsFrame, width=4, textvariable=events, justify=CENTER)
eventsPerSecond = Spinbox(eventsFrame, from_=0, to=1000, width=5)
eventsPerSecond.grid(row=0)
events.set(1)
eventsPerSecLabel = Label(eventsFrame, text='Events Per')
eventsPerSecLabel.grid(row=0, column=1)

time = StringVar()
timeTextBox = Entry(eventsFrame, width=5, textvariable=time, justify=CENTER)
timeTextBox.grid(row=0, column=2)
time.set(1000)
timeLabel = Label(eventsFrame, text='ms')
timeLabel.grid(row=0, column=3)
timeFieldIndexTextBox = Entry(eventsFrame, width=7, justify=CENTER)
timeFieldIndexTextBox.grid(row=1, columnspan=3, sticky=W, pady=5)
timeFieldIndexLabel = Label(eventsFrame, text='Time Field #')
timeFieldIndexLabel.grid(row=1, column=1)

continueFrame = Frame(containerFrame, bd=1, padx=10, pady=10)
continueFrame.grid(row=3, column=1)
checked = IntVar()
continuousLoop = Checkbutton(continueFrame, text='Continuous Loop', variable=checked)
continuousLoop.grid(row=0)
skip = IntVar()
skipFirstLine = Checkbutton(continueFrame, text='Skip First Line', variable=skip)
skipFirstLine.grid(row=1, sticky=W)

controlFrame = Frame(containerFrame, relief=SUNKEN, padx=25, pady=5)
controlFrame.grid(row=3, column=2, rowspan=2)
playButton = Button(controlFrame, text='Play', width=5, command=threadStream)
playButton.grid(row=0, padx=(10,10))
stopButtom = Button(controlFrame, text='Exit', width=5, command=stop)
stopButtom.grid(row=0, column=1, padx=(5,5))

seeStream = StringVar()
seeStreamTextBox = Entry(root, width=80, justify=LEFT, textvariable=seeStream)
seeStreamTextBox.grid(row=4, padx=25, pady=5)

root.mainloop()