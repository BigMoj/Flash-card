import random
from tkinter import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}


try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_word():
    global current_card, flip_timer
    root.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(title_word, text="French", fill="black")
    canvas.itemconfig(french_word, text=current_card["French"], fill="black")
    canvas.itemconfig(front_card, image=front_img)
    flip_timer = root.after(3000, flip_card)


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_word()


def flip_card():
    canvas.itemconfig(title_word, text="English", fill="white")
    canvas.itemconfig(french_word, text=current_card["English"], fill="white")
    canvas.itemconfig(front_card, image=back_img)


root = Tk()
root.title("Flashy")
root.config(padx=50, pady=50, bg=BACKGROUND_COLOR, highlightthickness=0)

flip_timer = root.after(3000, flip_card)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
front_img = PhotoImage(file="images/card_front.png")
back_img = PhotoImage(file="images/card_back.png")
front_card = canvas.create_image(400, 265, image=front_img)
title_word = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"), fill="Black")
french_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"), fill="Black")
canvas.grid(column=0, row=0, columnspan=2)

right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, highlightthickness=0, command=is_known)
right_button.grid(column=1, row=1)

wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, command=next_word)
wrong_button.grid(column=0, row=1)

next_word()


root.mainloop()
