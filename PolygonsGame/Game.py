from tkinter import *
import random
import time
from PIL import ImageTk

count = 0
lost = False

root = Tk()
root.title("Polygons Game")
root.resizable(0,0)

background = ImageTk.PhotoImage(file="./Background.png")
canvas = Canvas(root, width=800, height=600, bd=0, highlightthickness=0)
canvas.pack()
canvas.create_image(0, 0, image=background, anchor="nw")

root.update()

class MainPlygon:
    def __init__(self, canvas, Barra, color):
        self.canvas = canvas
        self.Barra = Barra
        self.ball = canvas.create_rectangle(0, 0, 30, 30, fill=color, outline=color)
        self.canvas.move(self.ball, 150, 100)

        starts_x = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts_x)

        self.x = starts_x[0]
        self.y = -3

        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()

    def draw(self):
        self.canvas.move(self.ball, self.x, self.y)

        position = self.canvas.coords(self.ball)

        if position[1] <= 0:
            self.y = 3

        if position[3] >= self.canvas_height:
            self.y = -3

        if position[0] <= 0:
            self.x = 3
            
        if position[2] >= self.canvas_width:
            self.x = -3

        self.Barra_position = self.canvas.coords(self.Barra.bar)

        if position[2] >= self.Barra_position[0] and position[0] <= self.Barra_position[2]:
            if position[3] >= self.Barra_position[1] and position[3] <= self.Barra_position[3]:
                self.y = -3
                global count
                count +=1
                score_count()

        if position[3] <= self.canvas_height:
            self.canvas.after(10, self.draw)
        else:
            game_over()
            global lost
            lost = True

class Barra:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.bar = canvas.create_rectangle(0, 0, 100, 20, fill=color, outline=color)
        self.canvas.move(self.bar, 100, 400)

        self.x = 0

        self.canvas_width = self.canvas.winfo_width()

        self.canvas.bind_all("<KeyPress-Left>", self.move_left)
        self.canvas.bind_all("<KeyPress-Right>", self.move_right)

    def draw(self):
        self.canvas.move(self.bar, self.x, 0)

        self.pos = self.canvas.coords(self.bar)

        if self.pos[0] <= 0:
            self.x = 0
        
        if self.pos[2] >= self.canvas_width:
            self.x = 0
        
        global lost
        
        if lost == False:
            self.canvas.after(10, self.draw)

    def move_left(self, event):
        if self.pos[0] >= 0:
            self.x = -3
    
    def move_right(self, event):
        if self.pos[2] <= self.canvas_width:
            self.x = 3

def start_game(event):
    global lost, count
    lost = False
    count = 0
    score_count()
    canvas.itemconfig(game_status, text=" ")

    time.sleep(1)
    Barra.draw()
    MainPlygon.draw()

def score_count():
    canvas.itemconfig(score_now, text="Pontuação: " + str(count))

def game_over():
    canvas.itemconfig(game_status, text="Você Perdeu!")

game_status = canvas.create_text(400, 300, text="Clique para começar!", fill="black", font=("Arial", 24))
score_now = canvas.create_text(80, 20, text=" ", fill="black", font=("Arial", 16))
canvas.bind_all("<Button-1>", start_game)

Barra = Barra(canvas, "#BC6B6A")
MainPlygon = MainPlygon(canvas, Barra, "#944DDC")

root.mainloop()