from Tkinter import *
from tkSimpleDialog import askstring
from tkFileDialog   import asksaveasfilename
from tkFileDialog   import askopenfile

from tkMessageBox import askokcancel

from corpus import *
from witten_bell import *

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
    def __init__(self, parent=None, text='', binding=None, disabled=False, file=None):
        Frame.__init__(self, parent)
        self.makewidgets(binding)
        if disabled:
            self.text.config(state=DISABLED)
        self.settext(text, file)

    def makewidgets(self, binding):
        sbar = Scrollbar(self)
        text = Text(self, relief=SUNKEN)

        if binding:
            (key, function) = binding
            text.bind(key, function)

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
        # n dropdown
        var = StringVar()
        var.set("2")
        self.n = 2
        OptionMenu(frm, var, "2","3", command=self.get_n).pack()
        # input textbox
        self.inputText = ScrolledText(parent, binding=("<space>", self.predictNextWord),  file=file)
        self.inputText.pack(expand=YES, fill=BOTH)
        # separator
        Frame(height=2, bd=1, relief=SUNKEN).pack(fill=X, padx=5, pady=5)
        # control textbox
        self.outputText = ScrolledText(parent, disabled=False)
        self.outputText.pack(expand=YES, fill=BOTH)
        # set inputText and outputText size
        self.inputText.text.config(height=20)
        self.outputText.text.config(height=8)
        # set focus on inputText
        self.inputText.text.focus()

    def onSave(self):
        filename = asksaveasfilename()
        if filename:
            alltext = self.inputText.gettext()
            open(filename, 'w').write(alltext)

    def onLoad(self):
        self.filename = askopenfile()
        self.wb = Witten_Bell()
        self.wb.train(self.filename, self.n)
    
    def get_n(self, event):
		self.n = event

    def predictNextWord(self, event):
        text = self.inputText.gettext()
        text = text.split()

        if len(text) < self.n:
            return

        sequence = (str(text[-2]), str(text[-1]))
        self.outputText.settext(self.wb.get_next_word(sequence))       


if __name__ == '__main__':
    try:
        master = Tk()
        master.wm_title("Predictive Typing System")

        editor = SimpleEditor(parent=master, file=sys.argv[1])
        editor.mainloop()
    except IndexError:
        SimpleEditor().mainloop()

