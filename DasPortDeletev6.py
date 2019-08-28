from tkinter import * 
from tkinter import filedialog  
import webbrowser 
from tkinter import messagebox  
import tkinter.scrolledtext as ScrolledText

class DeleteConfig(object):
	def __init__(self, window):
		self.window = window
		self.window.title("DAS Port Delete Tool")
		self.window.geometry('500x500')  
		lbl3 = Label(self.window, text="Enter CA/CRQ Number:") 
		lbl3.grid(column=1, row=1) 
		self.txt = Entry(self.window ,width=15)
		self.txt.grid(column=2, row=1) 
		
		lbl4 = Label(self.window, text="Enter Site ID:") 
		lbl4.grid(column=1, row=2) 
		self.txt2 = Entry(self.window ,width=15)
		self.txt2.grid(column=2, row=2) 
		
		lbl5 = Label(self.window, text="Enter Device Name 1:") 
		lbl5.grid(column=1, row=3) 
		self.txt3 = Entry(self.window ,width=15)
		self.txt3.grid(column=2, row=3) 
		
		lbl6 = Label(self.window, text="Enter Device Name 2:") 
		lbl6.grid(column=1, row=4) 
		self.txt4 = Entry(self.window ,width=15)
		self.txt4.grid(column=2, row=4) 
        #self.txt4.yview(tk.END) 
		self.textArea=Text(self.window,height=5,width=15)
		self.textArea.grid(column=3, row=4)
		self.textArea2=Text(self.window,height=5,width=15)
		self.textArea2.grid(column=3, row=3)
		#btn = Button(self.window, text=" Select Interface File ", command=self.clickedSELECT)
		#btn.grid(column=3, row=3)
		btn3 = Button(self.window, text=" Build MOP ", command=self.clickedMOP)
		btn3.grid(column=1, row=10)
		btn2 = Button(self.window, text=" Help ", command=self.clickedHELP)
		btn2.grid(column=2, row=10)
		cbtn = Button(self.window, text=" Close ", command=self.window.destroy)
		cbtn.grid(row=10, column=3, pady=4) 
	def clickedHELP(self):
		messagebox.showinfo("Hello", "This Script will generate configuration for deleting the DAS ports. \n \n In the Box, interfaces should be listed as \n int g1/5 \n int g1/6 \n int g1/7 \n\n\n The MOP is saved under C Delete MOPs Folder \n\n\n Hridin - HSIE IN")
	def clickedSELECT(self):  
		#self.CA = self.txt.get()  
		#self.siteid = self.txt2.get()
		#self.deviceid = self.txt3.get()		
		self.file_path =  filedialog.askopenfilename() 
	def clickedMOP(self):  
		self.CA = self.txt.get()  
		self.siteid = self.txt2.get()
		interfaces=[]
		interfaces2=[]
		tin=self.textArea2.get(1.0,END)
		tin=tin.replace("\n",":")
		interfaces.append(tin.strip(":"))
		interfaces=interfaces[0].split(":")
		tin2=self.textArea.get(1.0,END)
		tin2=tin2.replace("\n",":")
		interfaces2.append(tin2.strip(":"))
		interfaces2=interfaces2[0].split(":")
		print (type(interfaces))
		print (type(interfaces2))
		self.deviceid = self.txt3.get().upper()
		self.deviceid2 = self.txt4.get().upper()
		#webbrowser.open(MOPFile) 
		global file2
		file2 = "C:/Delete MOPs/Delete MOP CA " + self.CA +" " + self.deviceid +".txt"
		global text2
		text2 = open(file2, "w")
		text2.write("\nCA/CRQ: " + self.CA)
		text2.write("\nSite ID: " + self.siteid)
		text2.write("\nDevice Names:  \n" + self.deviceid +" \n"+ self.deviceid2)
		text2.write("\n\n#################") 
		text2.write("\nPRE AND POSTCHECK \n")
		text2.write("#################\n\n")
		
		text2.write("\n## " + self.deviceid)
		self.preCheck(interfaces)
		print (type(self.deviceid2))
		if self.deviceid2 != '':
			text2.write("\n## " + self.deviceid2)
			self.preCheck(interfaces2)
		
		
		text2.write("\n\n#################\n")
		text2.write("EXECUTION - PHASE 1 MOP\n")
		text2.write("#################\n\n")
		text2.write("\n## " + self.deviceid)
		self.execution(interfaces)
		if self.deviceid2 != '':
			text2.write("\n## " + self.deviceid2)
			self.execution(interfaces2)	
		text2.write("\n\n#################\n")
		text2.write("ROLLBACK \n")
		text2.write("#################\n\n")	
		text2.write("\n## " + self.deviceid)
		self.rollback(interfaces)
		
		if self.deviceid2 != '':
			text2.write("\n## " + self.deviceid2)
			self.rollback(interfaces2)			
		text2.write("\n\n#################\n")
		text2.write("After 72 Hours - PHASE 2 MOP \n")
		text2.write("#################\n\n")
		text2.write("\n## " + self.deviceid)
		self.phase2(interfaces)
		
		if self.deviceid2 != '':
			text2.write("\n##" + self.deviceid2)
			self.phase2(interfaces2)	
		webbrowser.open(file2) 
		text2.close()
	def preCheck(self,interfaces):
		interfaces=interfaces
		print (interfaces) 
		#for interface in interfaces: 
			#ext2.write("\nsh " + interface + " status") 
		for interface in interfaces: 
			text2.write("\nsh " + interface + " | inc Description|line protocol|input|clear|address") 
		for interface in interfaces: 
			text2.write("\nsh run " + interface )  
		for interface in interfaces: 
			text2.write("\nsh mac address-table " + interface) 
		#for interface in interfaces: 
			#text2.write("\nsh " + interface + " | inc packet")  
		 
		text2.write("\nsh int description | inc " + self.siteid.lower() + "\n") 
		text2.write("sh int description | inc " + self.siteid.upper() + "\n")
		#text2.write("sh run | inc " + self.siteid.lower() + "\n")
		#text2.write("sh run | inc " + self.siteid.upper() + "\n")
	def execution(self,interfaces):
		interfaces=interfaces 
		text2.write("\n\nconf t" + "\n") 
		for interface in interfaces:
			text2.write(str(interface) + "\n")
			text2.write("shut" + "\n\n")
		text2.write("end" + "\n")
		text2.write("wr" + "\n")
	def rollback(self,interfaces):
		interfaces=interfaces		
		text2.write("\n\nconf t" + "\n") 
		for interface in interfaces:
			text2.write(str(interface) + "\n")
			text2.write("no shut" + "\n\n") 
		text2.write("end" + "\n")
		text2.write("wr" + "\n") 
	def phase2(self,interfaces):
		interfaces=interfaces		
		text2.write("\n\nconf t" + "\n") 
		for interface in interfaces:
			text2.write("default " + str(interface) + "\n") 
			text2.write("\n") 
			text2.write(str(interface) + "\n")
			text2.write("description Available" + "\n") 
			text2.write("storm-control broadcast level 0.50" + "\n") 
			text2.write("storm-control multicast level 0.50" + "\n") 
			text2.write("no cdp enable" + "\n") 
			text2.write("no lldp transmit" + "\n")
			text2.write("no lldp receive" + "\n")
			text2.write("shutdown" + "\n\n")
		text2.write("end" + "\n")
		text2.write("wr" + "\n") 

root = Tk()
newDelete = DeleteConfig(root)  
root.mainloop()
