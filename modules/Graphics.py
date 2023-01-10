# Import module
import tk
from helpingFunctions import HelpingFunction

class GraphicsManager:
	frame = None
	lat = None
	long = None
	validInput = None
	def __init__(self,frame_):
		self.frame = frame_
		self.frame.title("TextBox Input")
		self.frame.geometry('800x800')
		validInput = False
		# Top level window
		# Function for getting Input
		# from textbox and printing it 
		# at label widget
		# Add image file
		bg = tk.PhotoImage(file = "../src/pso_logo.png")

		# Show image using label
		label1 = tk.Label(self.frame, image = bg)
		label1.place(x = 0,y = 0)

		# Label
		lbl2 = tk.Label(self.frame,text="Enter Coordinates: (latitude, longitude)")
		lbl2.place(x = 305,y= 380)

		# TextBox Creation
		inputtxt = tk.Text(self.frame, height = 2,width = 50)
		inputtxt.place(x=250,y=400)

		# Button Creation
		printButton = tk.Button(self.frame,
		text = "Explore", 
		command = getInput(inputtxt,self.frame,lbl2,self.lat,self.long))
		printButton.place(x=380,y=431)
		self.frame.mainloop()

	def returnInput(self):
		if self.lat != None and self.long != None:
			return self.lat,self.long
		else:
			return None

	def inputValid(self):
		if self.validInput == True:
			return True
		else:
			return False


def getInput(inputtxt,frame,lbl2,lat,long):
	inp = inputtxt.get(1.0, "end-1c") 
	# Label Creation
	lbl = tk.Label(frame, text = "")
	lbl.place(x=300,y=400)
	lbl2.destroy()
	inputtxt.destroy()
	if HelpingFunction.internet() == True:
		inp.strip()
		lst_ = inp.split(",")
		if len(lst_) > 1:
			validInput = True
			lat,long = lst_[0],lst_[1]
			lbl.config(text = "Exploration Started :)\nPlease Wait!",fg='#21E1E1',font=('Arial', 20))  
		else:
			lbl.config(text = "Please Enter Valid Input!",fg='#C21010',font=('Arial', 20))  
	else:
			lbl.config(text = "NO INTERNET CONNECTION! :(\nPlease Check Internet",fg='#C21010',font=('Arial', 20))


