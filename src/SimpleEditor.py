from Tkinter import *
from tkSimpleDialog import askstring
from tkFileDialog   import asksaveasfilename
from tkFileDialog   import askopenfile

from tkMessageBox import askokcancel

from witten_bell import get_next_word_witten_bell

class Quitter(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()
        widget = Button(self, text='Quit', command=self.quit)
        widget.pack(expand=YES, fill=BOTH, side=LEFT)

    def quit(self):
        ans = askokcancel('Quit', "Do you really want to quit?")
        if ans:
            Frame.quit(self)

class ScrolledText(Frame):
    def __init__(self, parent=None, text='', disabled=False, file=None):
        Frame.__init__(self, parent)
        self.makewidgets()
        #if disabled:
        #    self.text.config(state=DISABLED)
        self.settext(text, file)

    def makewidgets(self):
        sbar = Scrollbar(self)
        text = Text(self, relief=SUNKEN)
        sbar.config(command=text.yview)
        text.config(yscrollcommand=sbar.set, font=('monospace', 12, 'normal'))
        sbar.pack(side=RIGHT, fill=Y)
        text.pack(side=LEFT, expand=YES, fill=BOTH)
        self.text = text

    def settext(self, text='', file=None):
        if file:
            text = open(file, 'r').read()
        self.text.delete('1.0', END)
        self.text.insert('1.0', text)
        self.text.mark_set(INSERT, '1.0')

    def gettext(self):
        return self.text.get('1.0', END+'-1c')

class SimpleEditor(Frame):
	def __init__(self, parent=None, file=None):
		Frame.__init__(self, parent)

		# frame for save and quit buttons
		frm = Frame(parent)
		frm.pack(fill=X)
		# save button
		Button(frm, text='Save',  command=self.onSave).pack(side=LEFT)
		# Load button
		Button(frm, text='Load',  command=self.onLoad).pack(side=LEFT)
		# quit button
		Quitter(frm).pack(side=LEFT)
		# input textbox
		self.inputText = ScrolledText(parent, file=file)
		self.inputText.pack(expand=YES, fill=BOTH)
		# separator
		Frame(height=2, bd=1, relief=SUNKEN).pack(fill=X, padx=5, pady=5)
		# control textbox
		self.outputText = ScrolledText(parent, disabled=True)
		self.outputText.pack(expand=YES, fill=BOTH)
		# set inputText and outputText size
		self.inputText.text.config(height=20)
		self.outputText.text.config(height=8)
		# set focus on inputText
		self.inputText.text.focus()
		
		# TODO bindati na space i na inputText
		frm.bind("<Button-1>", self.predictNextWord)

	def onSave(self):
		filename = asksaveasfilename()
		if filename:
			alltext = self.inputText.gettext()
			open(filename, 'w').write(alltext)

	def onLoad(self):
		self.filename = askopenfile()
		
	def predictNextWord(self, event):
		text = self.inputText.gettext()
		text = text.split()
		sequence = (str(text[-2]), str(text[-1]))
		self.outputText.settext(get_next_word_witten_bell(self.filename, sequence))
		#print get_next_word_witten_bell(self.filename, sequence)

		
if __name__ == '__main__':
	try:
		master = Tk()
		master.wm_title("Predictive Typing System")

		editor = SimpleEditor(parent=master, file=sys.argv[1])
		editor.mainloop()
	except IndexError:
		SimpleEditor().mainloop()

