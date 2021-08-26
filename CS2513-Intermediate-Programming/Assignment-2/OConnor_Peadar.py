import tkinter as tk
from time import *
import random


class Game(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        self.points = 0
        self.squarecolour = "#16E2CD"
        self.squaresize = 60
        self.randomfix = 540
        self.timer = 2

    def incrementPoints(self):
        self.points = self.points + 1
        self.pointlabel = tk.Label(self.frame, text="Points = %i" % self.points, fg="white", bg="black", padx=5, pady=5,
                                   height=2)
        self.pointlabel.grid(column=0, row=1)

    def minusPoints(self, event):
        self.points = self.points - 1
        self.pointlabel = tk.Label(self.frame, text="Points = %i" % self.points, fg="white", bg="black", padx=5, pady=5,
                                   height=2)
        self.pointlabel.grid(column=0, row=1)

    def createWidgets(self):
        self.points = 0
        self.c = tk.Canvas(self, width=600, height=600)
        self.c.pack(side=tk.TOP)
        self.bg = self.c.create_rectangle(0,0,600,600, fill="#AB8880")
        self.frame = tk.Frame(self)
        self.start = tk.Button(self.frame, command=self.gameStart, text="START GAME", fg="white", bg="black", padx=6,
                               pady=5, height=2)
        self.start.grid(column=3, row=1)
        self.easy = tk.Button(self.frame, command=self.easyMode, text="Easy", fg="white", bg="#0244C8", padx=6, pady=5,
                              height=2)
        self.easy.grid(column=0, row=1)
        self.normal = tk.Button(self.frame, command=self.normalMode, text="Normal", fg="white", bg="#AB8880", padx=6, pady=5,
                              height=2)
        self.normal.grid(column=1, row=1)
        self.hard = tk.Button(self.frame, command=self.hardMode, text="Hard", fg="white", bg="#DCC700", padx=6, pady=5,
                              height=2)
        self.hard.grid(column=2, row=1)
        self.frame.pack(side=tk.BOTTOM)

    def gameStart(self):
        self.start.grid_forget()
        self.easy.grid_forget()
        self.normal.grid_forget()
        self.hard.grid_forget()
        self.pointlabel = tk.Label(self.frame, text="Points = %i" % self.points, fg="white", bg="black", padx=6,
                                   pady=5,
                                   height=2)
        self.pointlabel.grid(column=0, row=1)
        self.x = random.randint(0, self.randomfix)
        self.y = random.randint(0, self.randomfix)
        self.square = self.c.create_rectangle(self.x, self.y, self.x + self.squaresize, self.y + self.squaresize, fill=self.squarecolour)
        self.time1 = time()
        self.c.tag_bind(self.square, '<ButtonPress-1>', self.squareClicked)

    def squareClicked(self, event):
        self.time2 = time()
        if (self.time2 - self.time1) < self.timer:
            self.incrementPoints()
        self.c.delete(self.square)
        self.x = random.randint(0, self.randomfix)
        self.y = random.randint(0, self.randomfix)
        self.square = self.c.create_rectangle(self.x, self.y, self.x + self.squaresize, self.y + self.squaresize, fill=self.squarecolour)
        self.time1 = time()
        self.c.tag_bind(self.square, '<ButtonPress-1>', self.squareClicked)

    def easyMode(self):
        self.bg = self.c.create_rectangle(0, 0, 600, 600, fill="#0244C8")
        self.squarecolour = "#FFA70E"
        self.squaresize = 80
        self.randomfix = 520
        self.timer = 3

    def normalMode(self):
        self.bg = self.c.create_rectangle(0, 0, 600, 600, fill="#AB8880")
        self.squarecolour = "#16E2CD"
        self.squaresize = 60
        self.randomfix = 540
        self.timer = 2

    def hardMode(self):
        self.bg = self.c.create_rectangle(0, 0, 600, 600, fill="#DCC700")
        self.c.tag_bind(self.bg, '<ButtonPress-1>', self.minusPoints)
        self.squarecolour = "#7F00DC"
        self.squaresize = 40
        self.randomfix = 560
        self.timer = 1

game = Game()
game.master.title("Clicking Game")
game.master.geometry("650x600")
game.master.configure(bg="grey")
game.master.minsize(height=650, width=600)
game.master.maxsize(height=650, width=600)
game.mainloop()

'''
Extra Functionality: I have added difficulty options to be selected before the game starts. Normal Mode is the default 
mode, and has the two second timer as asked in the assignment. Clicking on either Easy or Hard will change a few things.
Each mode has its own colour scheme, changing the background of the canvas and the squares. On Easy mode, the squares 
are bigger and the time allowed for the user to click the square and get the point is 3 seconds. On Hard mode, the
squares are smaller and the user only has one second to click the square to get the point. The user can switch between
these difficulty modes as much as they want until the game is started, which will cause the difficulty buttons to 
disappear. On Hard mode only, Clicking on the canvas and not on the square will take a point away from the user. 
'''