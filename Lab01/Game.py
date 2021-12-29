from tkinter import *
import random
import time
from PIL import ImageTk

#level_choice = int(input("Qual nível você gostaria de jogar? 1/2/3/4/5 \n"))
level_choice = 10
length_bar = level_choice*10

root = Tk()
root.title("Ping Pong")
root.resizable(0,0)

background= ImageTk.PhotoImage(file="./fundo.jpg")

canvas = Canvas(root, width=800, height=600, bd=0, highlightthickness=0)
canvas.pack()
canvas.create_image(0, 0, image=background, anchor="nw")

root.update()

count = 0
lost = False

class Bola:
    def __init__(self, canvas, Barra, color):
        self.canvas = canvas
        self.Barra = Barra
        self.ball = canvas.create_oval(0, 0, 30, 30, fill=color)
        self.canvas.move(self.ball, 245, 200)

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
                score()

        if position[3] <= self.canvas_height:
            self.canvas.after(10, self.draw)
        else:
            game_over()
            global lost
            lost = True

class Barra:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.bar = canvas.create_rectangle(0, 0, length_bar, 20, fill=color)
        self.canvas.move(self.bar, 200, 400)

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
    score()
    canvas.itemconfig(end_game, text=" ")

    time.sleep(1)
    Barra.draw()
    Bola.draw()

def score():
    canvas.itemconfig(score_now, text="Pontuação: " + str(count))

def game_over():
    canvas.itemconfig(end_game, text="Você Perdeu!")

Barra = Barra(canvas, "gold")
Bola = Bola(canvas, Barra, "blue")

score_now = canvas.create_text(80, 20, text="Pontuação: " + str(count), fill="black", font=("Arial", 16))
end_game = canvas.create_text(400, 300, text="Clique para começar!", fill="red", font=("Arial", 40))

canvas.bind_all("<Button-1>", start_game)

root.mainloop()