from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
all_words = {}
showing_name = True  # New variable to track if the card is showing the name

try:
    data = pd.read_csv("data/Words_to_learn.csv")
    original_data = pd.read_csv("data/Biology_Phrases.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/Biology_Phrases.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")
    all_words = original_data.to_dict(orient="records")


def select_word_set(choice):
    global to_learn
    if choice == "Review All":
        to_learn = all_words
    else:
        try:
            data = pd.read_csv("data/Words_to_learn.csv")
            to_learn = data.to_dict(orient="records")
        except FileNotFoundError:
            to_learn = original_data.to_dict(orient="records")

    next_card()


def next_card():
    global current_card, flip_timer, showing_name
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_text, text=current_card["Name"], fill="black", font=("Abolition", 40, "bold"))
    canvas.itemconfig(card_background, image=card_front_img)
    showing_name = True  # Ensure we start by showing the name


def flip_card():
    global showing_name
    if showing_name:
        canvas.itemconfig(card_text, text=current_card["Explanation"], fill="white", font=("Abolition", 40, "bold"))
        canvas.itemconfig(card_background, image=card_back_img)
    else:
        canvas.itemconfig(card_text, text=current_card["Name"], fill="black", font=("Abolition", 40, "bold"))
        canvas.itemconfig(card_background, image=card_front_img)
    showing_name = not showing_name  # Toggle the state


def is_known():
    to_learn.remove(current_card)
    next_card()
    data = pd.DataFrame(to_learn)
    data.to_csv("data/Words_to_learn.csv", index=False)


window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

# The Canvas functions allow me to write on the background
canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")

card_background = canvas.create_image(400, 263, image=card_front_img)
card_text = canvas.create_text(400, 263, text="", font=("Abolition", 40), width=700)

# Bind the click event to the card_text
canvas.tag_bind(card_text, "<Button-1>", lambda event: flip_card())

# Changing the background color to be the same as the canvas.
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=1, column=0, columnspan=2)

cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=2, column=0)

success_image = PhotoImage(file="images/right.png")
known_button = Button(image=success_image, highlightthickness=0, command=is_known)
known_button.grid(row=2, column=1)

# Dropdown menu for selecting word set
options = ["Review Known", "Review All"]
variable = StringVar(window)
variable.set(options[0])  # Default option

menu = OptionMenu(window, variable, *options, command=select_word_set)
menu.config(width=20)
menu.grid(row=2, column=0, columnspan=2)

next_card()
window.mainloop()
