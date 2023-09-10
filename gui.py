#!/usr/local/bin/python3
"""
gui.py - provides the interface for the GUI
 
Written by Bruce Fuda for Intermediate Programming
Python RPG Assignment 2014

Modified with permission by Edwin Griffin
"""

# Text/Graphics Library
from tkinter import *

# Python Libraries
import sys
from PIL import ImageTk

# Class that creates an object which if the Window and GUI for our game
class simpleapp_tk(Tk): # Our app inherits from the Tk module
  
  # Initialising method, mostly to start the parent module (the Tk module)
  def __init__(self,parent):
    
    # What starts Tkinter (specifically the Tk module)
    Tk.__init__(self,parent)
    self.parent = parent
    
    # Creating the window by calling our custom method
    self.initialize()

  # Used to create the window
  def initialize(self):
    
    # Setting up a grid to place objects into on the screen
    self.grid()

    # used for polling for user input only
    # i.e. wait variable
    self.inputVariable = StringVar()

    # Setting up the side scroll bar
    scrollbar = Scrollbar(self)
    # Placing the side scroll bar on the right and stretching and sticking it to the top and bottom of the window
    scrollbar.grid(row=0, column=2, sticky=N+S)

    # Setting up self.text which will be the way we draw text and perhaps images to the screen
    self.text = Text(self, wrap=WORD, yscrollcommand=scrollbar.set)
    
    # Aligning the text to the left side and filling the grid square
    self.text.grid(column=0,row=0,columnspan=2,sticky='NSEW')
    # Disabliling the ability to alter the text after it has been printed (It makes the window 'read only')
    self.text.config(state=DISABLED)
    
    # Allows communication between the text grid cell and the scrollbar 
    # so the text can tell the scollbar where it is so it can actually work
    scrollbar.config(command=self.text.yview)

    # Is what the entry variable will be changing
    # This gives us access to the value self.entry produces
    self.entryVariable = StringVar()
    
    # Setting up the text bar down the bottom of the screen for the user to type into
    # To have access to the value self.entry produces we set it to update the string variable above
    self.entry = Entry(self,textvariable=self.entryVariable)
    
    # Aligning it to the bottom of the screen
    self.entry.grid(column=0,row=1,sticky='SEW')
    
    # Setting the self.OnPressEnter to automatically run whenever the self.entry variable 
    # recieves <Return> which is when the enter key is pressed
    self.entry.bind("<Return>", self.OnPressEnter)

    # Creating an 'Enter' button for the user
    button = Button(self,text=u"Enter", command=self.OnButtonClick) # Button name, What the button triggers
    # Aligning it to the bottom of the screen, right of the input box
    button.grid(column=1,row=1)

    # Allows resizing and prioritisation of cells on our grid
    # We are saying let the top left cell take up 1 unit of width and height 
    # (it takes up all the avalible space, wherever there is a blank column)
    self.grid_columnconfigure(0,weight=1)
    self.grid_rowconfigure(0,weight=1)
    # Allowing the window to be resizeable
    self.resizable(False, False)
    
    # map_game_image = Label(self.canvas, image=map_image, borderwidth=0).place(x = 0, y = 0)  
    
    # Running all tasks just created in the code above, including running any functions, 
    # (re)drawing widgets, configuring all the widgets, and
    # dealing with geometry management (placing things where they need to go and dividing up the grid)
    self.update()
    
    # Setting the size of the window
    self.geometry('980x800')    
    # Sets the application to 'focus' on the player input box (self.entry)
    # This means the widget accepting input at the moment is self.entry
    self.entry.focus_set()
    # Select all of what is in self.entry (select everything the player has typed)
    # END is the position after the last charcter of text
    self.entry.selection_range(0, END)

  # When the enter button (on screen) is clicked set our detected player input (self.inputVariable) 
  # to whatever the player typed last
  def OnButtonClick(self):
    self.inputVariable.set( self.entryVariable.get() )

  # When the enter button (keyboard) is pressed set our detected player input (self.inputVariable) 
  # to whatever the player typed last
  def OnPressEnter(self,event):
    self.inputVariable.set( self.entryVariable.get() )

  # The write function simulates the behaviour of the print method
  # but uses the input textfield and text display instead of the usual
  # standard input/output we're used to from our previous programs
  def write(self,msg): # msg is message
    
    # Set the text in the window to be configurable
    self.text.config(state=NORMAL)
    
    # Drawing the text to the first cell, first drawing the message, then a newline character
    # Inserts the string at index END
    # END is the position after the last charcter of text
    self.text.insert(END, msg)
    self.text.insert(END, "\n")

    # Same as the previous update block, in this case the udpdate method is used to redraw the 
    # first grid cell with the new lines of text and update the size of the scrollbar accordingly
    self.update()
    
    # Disabliling the ability to alter the text after it has been printed (It makes the window 'read only')
    self.text.config(state=DISABLED)
    
    # END is the position after the last charcter of text
    # Returns true if the value at the end of the text is visible
    self.text.see(END)
    
    # Clearing the input line so it's blank
    self.entryVariable.set('')
    # Sets the application to 'focus' on the player input box (self.entry)
    # This means the widget accepting input at the moment is self.entry
    self.entry.focus_set()
    
    # Same as the previous update block, in this case the udpdate method is used to redraw the 
    # first grid cell with the new lines of text and update the size of the scrollbar accordingly
    self.update()
    
    # Disabliling the ability to alter the text after it has been printed (It makes the window 'read only')
    self.text.config(state=DISABLED)
    
  
  def map_focus(self):
    
    self.canvas.focus_set()
    
  # Function to quit the window
  def quit(self):
    # Closes the window
    sys.exit(0)