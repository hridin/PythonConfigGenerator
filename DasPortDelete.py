from tkinter import * 
from tkinter import filedialog  
import webbrowser 
from tkinter import messagebox 

class DeleteConfig(object):
	def __init__(self, window):
		self.window = window
		self.window.title("DAS Port Delete Tool")
		self.window.geometry('350x200')  
		lbl3 = Label(self.window, text="Enter CA/CRQ Number:") 
		lbl3.grid(column=0, row=1) 
		self.txt = Entry(self.window ,width=15)
		self.txt.grid(column=1, row=1) 
		btn = Button(self.window, text=" Select Interface File ", command=self.clickedSELECT)
		btn.grid(column=1, row=7) 
		btn3 = Button(self.window, text=" Build MOP ", command=self.clickedMOP)
		btn3.grid(column=1, row=10)
		btn2 = Button(self.window, text=" Help ", command=self.clickedHELP)
		btn2.grid(column=2, row=10)
		cbtn = Button(self.window, text=" Close ", command=self.window.destroy)
		cbtn.grid(row=10, column=3, pady=4) 
	def clickedHELP(self):
		messagebox.showinfo("Hello", "This Script will generate configuration for deleting the DAS ports. \n \n In the Interface file, interfaces should be listed as \n int g1/5 \n int g1/6 \n int g1/7 \n\n\n The MOP is saved under C folder \n\n\n Hridin - HSIE IN")
	def clickedSELECT(self):  
		self.CA = self.txt.get() 
		self.file_path =  filedialog.askopenfilename() 
	def clickedMOP(self):  
		self.CA = self.txt.get() 
		MOPFile = self.readInterfaceFile(self.file_path) 
		webbrowser.open(MOPFile)
	def readInterfaceFile(self,file_path): 
		file = file_path
		text = open(file, "r")
		interfaces = text.readlines() 
		file2 = "C:/DeleteConfig" + self.CA + ".txt"
		text2 = open(file2, "w")
		
		for interface in interfaces:
			text2.write("sh run " + str(interface).strip('\n') + "\n")
		text2.write("\n")	
		for interface in interfaces:
			text2.write("sh " + str(interface).strip('\n') + " status \n")
		text2.write("\n")	
		for interface in interfaces:
			text2.write("sh mac address-table " + str(interface).strip('\n') + "\n")
		text2.write("\n")
		for interface in interfaces:
			text2.write("sh " + str(interface).strip('\n') + " | inc packet\n")
		
		text2.write("\n\n#################\n")
		text2.write("Execution \n")
		text2.write("#################\n\n")
		for interface in interfaces:
			text2.write(str(interface).strip('\n') + "\n")
			text2.write("shut" + "\n\n")
		
		text2.write("\n\n#################\n")
		text2.write("After 72 Hours \n")
		text2.write("#################\n\n")
		for interface in interfaces:
			text2.write("default " + str(interface).strip('\n') + "\n")
		
		text2.write("\n")
		for interface in interfaces:
			text2.write(str(interface).strip('\n') + "\n")
			text2.write("description Available" + "\n\n")
		text.close() 
		text2.close()
		return file2
root = Tk()
newDelete = DeleteConfig(root)
root.mainloop()