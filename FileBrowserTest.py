from tkinter import *
from tkinter import filedialog 

class DeleteConfig(object):
	def __init__(self, window):
		self.window = window
		self.window.title("Delete Configuration Tool")
		self.window.geometry('350x200') 
		lbl = Label(self.window, text="Hello, Please select the txt file which contains interfaces to delete") 
		lbl.grid(column=0, row=0) 
		lbl3 = Label(self.window, text="Enter CA/CRQ Number:") 
		lbl3.grid(column=0, row=1) 
		self.txt = Entry(self.window ,width=15)
		self.txt.grid(column=0, row=2) 
		btn = Button(self.window, text="Select Interface File", command=self.clicked)
		btn.grid(column=0, row=4)
		btn2 = Button(self.window, text="Prepare MOP", command=self.clickedMOP)
		btn2.grid(column=1, row=4)
		self.lbl2 = Label(self.window, text="In the file, interfaces should be listed as \n int g1/5 \n int g1/6 \nint g1/7") 
		self.lbl2.grid(column=0, row=6)
        
	def clicked(self):  
		self.CA = self.txt.get()
		print (self.CA)
		self.file_path =  filedialog.askopenfilename()
		print (self.file_path)  
	def clickedMOP(self):  
		self.CA = self.txt.get() 
		self.readInterfaceFile(self.file_path)
	def readInterfaceFile(self,file_path):
		print (file_path)
		self.lbl2.configure(text=file_path)
		file = file_path
		text = open(file, "r")
		interfaces = text.readlines()
		for interface in interfaces:
			print (interface)
			self.lbl2.configure(text=interface)
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
root = Tk()
newDelete = DeleteConfig(root)
root.mainloop()