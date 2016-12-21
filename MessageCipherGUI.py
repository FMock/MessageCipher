from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
import tkinter.messagebox
from KnapsackCipher import KnapsackCipher
import tkinter.simpledialog
from random import shuffle
import hashlib

# MessageCipherGUI.py
# Frank Mock December 2016
# Coded in Python 3.4
#
# This program uses the Knapsack Cipher to encrypt
# plaintext and decrypt the ciphertext. I used
# Tkinter to build a GUI for this program.
# The encryption process uses a reduced charater set,
# RCS, to improve performance encrypting large
# chucks of plaintext. The program allows the user to
# save the ciphertext to a file that can later be
# re-loaded into the program and decrypted. To prevent
# just anybody from opening and decrypting a saved
# ciphertext file, a password is used secure the file.
#
# Currently, this program is not complete
# and requires much more work to make it a polished.
# Even though, the main feature (encrypt plaintext 
# and decrypt ciphertext) is operational, I would 
# like to make many improvements. One improvement 
# would be to increase the obfuscation of the key
# in the saved cipher files. Anothr would be to
# use the full ASCII character set.
#
# MessageCipherGUI is the entry class for this application
class MessageCipherGUI:
    def __init__(self):
        window = Tk()
        window.title("Message Cipher")
        
        #Strings to hold plaintext and ciphertext
        self.pText = ""
        self.cText = ""
        self.kc = KnapsackCipher()
        
        # Create a menu bar
        menubar = Menu(window)
        window.config(menu = menubar) # Display the menu bar
        
        # create a pulldown menu, and add it to the menu bar
        operationMenu = Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "File", menu = operationMenu)
        operationMenu.add_command(label = "Open",  
            command = self.openFile)
        operationMenu.add_command(label = "Open Encrypted",  
            command = self.openEncryptedFile)
        operationMenu.add_command(label = "Save", 
            command = self.saveFile)
        operationMenu.add_command(label = "Save Encrypted", 
            command = self.saveAsCiphertextFile)
        
        optionsmenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label = "Options", menu=optionsmenu)
        optionsmenu.add_command(label = "Settings", command = self.optionsMenu)        
        
        
        editmenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label = "Help", menu=editmenu)
        editmenu.add_command(label = "About", command = self.aboutMenu)
        
        
        # Add a tool bar frame 
        frame0 = Frame(window) # Create and add a frame to window
        frame0.grid(row = 1, column = 1, sticky = W)
        
        # Create icons
        openImage = PhotoImage(file = "images/open.gif")
        saveImage = PhotoImage(file = "images/save.gif")
        optionsImage = PhotoImage(file = "images/options.png")
        helpImage = PhotoImage(file = "images/help.png")
        searchImage = PhotoImage(file = "images/search.png")
        knapsackImage = PhotoImage(file = "images/knapsack-cipher.gif")
        encryptImage = PhotoImage(file = "images/Encrypt.png")
        decryptImage = PhotoImage(file = "images/Decrypt.png")
        clearImage = PhotoImage(file = "images/clear.png")
        
        Button(frame0, image = openImage, command = 
            self.openFile).grid(row = 1, column = 1, sticky = W)
        Button(frame0, image = saveImage,
            command = self.saveFile).grid(row = 1, column = 2)
        Button(frame0, image = optionsImage,
            command = self.optionsMenu).grid(row = 1, column = 3)
        Button(frame0, image = searchImage,
            command = None).grid(row = 1, column = 4)
        Button(frame0, image = helpImage,
            command = self.aboutMenu).grid(row = 1, column = 5)
        self.encryptButton = Button(frame0, image = encryptImage,
            command = self.encrypt)
        self.encryptButton.grid(row = 1, column = 6)        
        self.decryptButton = Button(frame0, image = decryptImage,
            command = self.decrypt)
        self.decryptButton.config(state='disabled')
        self.decryptButton.grid(row = 1, column = 7)
        self.clearButton = Button(frame0, image = clearImage,
            command = self.clear)
        self.clearButton.grid(row = 1, column = 8)
        Button(frame0, image = knapsackImage,
            command = None).grid(row = 1, column = 9)

        # Create frame to text area for user messages
        frame1 = Frame(window)
        frame1.grid(row= 3, column = 1)
        userMsgBgColor = '#ecdfce'
        self.userMessage = "\nEnter plaintext below and then press 'Encrypt' button."
        msgScrollbar = Scrollbar(frame1)
        self.userMsg = Text(frame1, width = 100, height = 4, 
            wrap = WORD, yscrollcommand = msgScrollbar.set)   
        self.userMsg.configure(bg = userMsgBgColor)
        self.userMsg.insert(END, self.userMessage)
        self.userMsg.pack()
        msgScrollbar.config(command = self.userMsg.yview)
                
        # Create frame to hold text area for encrypt/decrypt text
        frame2 = Frame(window)
        frame2.grid(row = 4, column = 1)
        scrollbar = Scrollbar(frame2)
        scrollbar.pack(side = RIGHT, fill = Y)
        self.text = Text(frame2, width = 100, height = 30, 
            wrap = WORD, yscrollcommand = scrollbar.set)
        self.text.pack()
        scrollbar.config(command = self.text.yview)
        
        
        window.mainloop() # Create an event loop
    
    # Open File dialog
    # Allows the user to open a text file to import into
    # the program
    def openFile(self): 
        filenameforReading = askopenfilename()
        infile = open(filenameforReading, "r")
        self.text.insert(END, infile.read()) # Read all from the file
        infile.close()  # Close the input file
    
    # Open Encrypted File
    # Allows the user to open a previously saved
    # ciphertext file. The ciphertext in the file
    # will not be displayed to the user unless they
    # enter the password that was used to save the
    # file (the password hashes must match)    
    def openEncryptedFile(self):
        filenameforReading = askopenfilename()
        infile = open(filenameforReading, "r")
        #Get the password hash from the first line of the file
        pwHash = infile.readline().strip()
        
        # Get the MultiInv, SIK_sum, and n values from file
        stuff = infile.readline().strip()
        
        # Get the SIK from the file
        theSIK = infile.readline().strip()
        
        # Get the GK from the file
        theGK = infile.readline().strip()
        
        # Prompt user to enter password
        correctPassword = FALSE
        errMsg = ""
        while correctPassword == FALSE:
            pw = tkinter.simpledialog.askstring("Enter Password","Only users that enter the correct "+\
                                                "password can decrypt the ciphertext." + errMsg)
            # Hash the password entered.
            m = hashlib.md5()
            pBytes = bytes(pw, 'utf-8')
            m.update(pBytes)
            p = m.hexdigest()
            
            # Check that the password hashes match
            if p == pwHash:
                self.encryptButton.config(state='disabled')
                self.decryptButton.config(state='normal')
                
                # Extract the multiInv from stuff list
                stuffAsList = stuff.split()
                stuffAsInts = []
                for u in stuffAsList:
                    stuffAsInts.append(int(u))
                # Change the multiInv value of the KnapsackCipher
                self.kc.setMultiInverse(stuffAsInts[0])
                # Change the SIK sum value of the KnapsackCipher
                self.kc.setSIKSum(stuffAsInts[1])
                # Change the n value of the KnapsackCipher
                self.kc.setN(stuffAsInts[2])
                
                # Turn SIK into list
                aSIKList = theSIK.split()
                # The SIK needs to be a list of ints
                sikAsInts = []
                for u in aSIKList:
                    sikAsInts.append(int(u))
                # Sort the elements of the SIK
                sikAsInts.sort()
                
                # Change the value of the current SIK
                self.kc.setSIK(sikAsInts)
                
                # Turn GK into list
                aGKList = theGK.split()
                # The GK needs to be a list of ints
                gkAsInts = []
                for u in aGKList:
                    gkAsInts.append(int(u))
                # Sort the elements of the GK
                gkAsInts.sort()
                
                # Change the value of the current GK
                self.kc.setGK(gkAsInts)
                
                # Break out of the loop
                correctPassword = True
            else:
                errMsg = "\n ***Incorrect Password***"
        
        self.text.delete(1.0, END) # Clear the text       
        self.text.insert(END, infile.read()) #Display ciphertext from file
        # Set the KnapsackCiphers encrypted string
        self.kc.setEncrypted(self.text.get(1.0, END).strip())
        
        self.userMsg.delete(1.0, END)
        self.userMsg.insert(1.0,"\nClick 'Decrypt' button to get the plaintext.")
                
        infile.close()  # Close the input file
        ##### Now the user can click 'Decrypt' button to get plaintext
    
    # Allows the user to save the text displayed to a file
    # Note, saving ciphertext this way does not allow you to
    # use this program to decrypt it later. You must use the
    # 'saveAsCiphertextFile' to do that
    def saveFile(self):
        filenameforWriting = asksaveasfilename()
        outfile = open(filenameforWriting, "w")
        # Write to the file
        outfile.write(self.text.get(1.0, END)) 
        outfile.close() # Close the output file
    
    # This method will save the ciphertext and all object data needed to
    # encrypt and decrypt using the current KnapsackCipher object to file.
    # This allows a user to save the ciphertext and at a later date any
    # instance of a KnapsackCipher can decrypt it. This allows for sharing of
    # ciphertext files between users of this program. There is a password
    # hash placed into the file that allows for a small level of security.    
    def saveAsCiphertextFile(self):
        correctPassword = FALSE
        errMsg = "DO NOT FORGET THIS PASSWORD"
        while correctPassword == FALSE:
            #### Prompt user for password
            
            pw = tkinter.simpledialog.askstring("Enter Password", \
                                                "Enter a password to secure the file.\n" +\
                                                "The password must include at least one "+\
                                                "number and a capital \n"+\
                                                "letter and be at least 6 digits. You will "+\
                                                "need to enter this password \n before you "+\
                                                "are allowed to decrypt the ciphertext.\n\n"+\
                                                 errMsg)
            # Check that password is in correct form
            # Contains at least one digit and one capital
            # and is at least 6 characters long
            regex = '(?=.{6,})\d.*[A-Z]|(?=.{6,})[A-Z].*\d'
            match1 = re.match(regex, pw)
            if match1 != None:
                # password is valid so hash it
                m = hashlib.md5()
                pBytes = bytes(pw, 'utf-8')
                m.update(pBytes)
                p = m.hexdigest()
                
                # Where does user want to save ciphertext file?
                filenameforWriting = asksaveasfilename()
                outfile = open(filenameforWriting, "w")
                
                # Put all information needed to decrypt and encrypt into the
                # ciphertext so instance variables in the KnapsackCipher
                # will work together moving forward.
                # Put the multi inverse, SIK sum and n value is string
                l = [str(self.kc.getMultiInverse()), str(self.kc.getSIKSum()), str(self.kc.getN())]
                s = " ".join(l)
                
                # Get the SIK, shuffle elements and turn into string
                theSIK = self.kc.getSIK()
                shuffle(theSIK) # mix up elements of SIK
                sik = " ".join(str(i) for i in theSIK)
                
                # Get the GK, shuffle elements and turn into string
                theGK = self.kc.getGK()
                shuffle(theGK)
                gk = " ".join(str(i) for i in theGK)
                
                # Get the ciphertext that's displayed in text area
                # Add password hash to first line of ciphertext
                c = p + "\n" + s + "\n" + sik + "\n" + gk + "\n" +self.text.get(1.0, END)
                
                outfile.write(c)

                outfile.close() # Close the output file
                # Exit loop
                correctPassword = True
            else:
                errMsg = "*** INVALID PASSWORD ***\n"
        
    
    # A dialog that displayes information about this program    
    def aboutMenu(self):
        tkinter.messagebox.showinfo("Frank's Knapsck Cipher", 
                                    "CS166 Extra Credit Assignment by Frank Mock")
        
    # An options menu that lets the user change settings
    # I planned to give the user the option to switch between using
    # the reduced character set and the normal set of ASCII characters
    # Hopefully, this will be done in the future
    def optionsMenu(self):
        tkinter.messagebox.showinfo("Options", "Nothing here yet!")    
    
    # Event-handler that the 'Encrypt' button calls when clicked
    # Changes the user message displayed
    # Grabs the text in the text area and uses an instance of
    # KnapsackCipher to encrypt it.
    # The ciphertext is then inserted into the text area    
    def encrypt(self):
        self.encryptButton.config(state='disabled')
        self.decryptButton.config(state='normal')
        self.userMsg.delete(1.0, END)
        self.userMsg.insert(1.0,"\nClick 'Decrypt' button to get plaintext back.")
        self.pText = self.text.get(1.0, END)
        # Reset the KnapsackCipher object
        self.kc = KnapsackCipher()
        self.cText = self.kc.encryptMsg(self.pText)
        self.text.delete(1.0, END)
        self.text.insert(END, self.cText)
    
    # Event-handler that the 'Decrypt' button calls when clicked.
    # The user message is changed
    # The text in the text area is grabbed. An instance of
    # KnapsackCipher is used to decrypt the text
    # The result is displayed in the text area.    
    def decrypt(self):
        self.encryptButton.config(state='normal')
        self.decryptButton.config(state='disabled')
        self.userMsg.delete(1.0, END)
        self.userMsg.insert(1.0,"\nEnter plaintext below and click 'Encrypt' button to turn it into ciphertext.")
        self.cText = self.text.get(1.0, END)
        self.pText = self.kc.decryptMsg(self.cText)
        self.text.delete(1.0, END)
        self.text.insert(END, self.pText)
    
    # Clear the text from the text area    
    def clear(self):
        self.text.delete(1.0, END)

if __name__ == '__main__':
    MessageCipherGUI() # Create GUI
