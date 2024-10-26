from tkinter import *
from tkinter import messagebox as mb
import random
import pyperclip
import json

from idna.codec import search_function


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    # for char in range(nr_letters):
    #   password_list.append(random.choice(letters))
    [password_list.append(random.choice(letters)) for _ in range(nr_letters)]

    # for char in range(nr_symbols):
    #   password_list += random.choice(symbols)
    [password_list.append(random.choice(symbols)) for _ in range(nr_symbols)]

    # for char in range(nr_numbers):
    #   password_list += random.choice(numbers)
    [password_list.append(random.choice(numbers)) for _ in range(nr_numbers)]

    random.shuffle(password_list)

    password = "".join(password_list)
    # for char in password_list:
    #     password += char

    # print(f"Your password is: {password}, {len(password)}")
    password_input.insert(0, password)
    pyperclip.copy(password)




# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_password():
    # print("Password added")
    email = email_input.get()
    password = password_input.get()
    website = website_input.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }
    if len(email) < 2 or len(password) < 5:
        mb.showinfo(title="Error", message="Please type the correct information!")
        return


    is_ok = mb.askokcancel(title="This Data will be saved",
                           message=f"Website: {website}\n Email: {email}\n Password: {password}")
    if is_ok:
        try:
            with open("data.json", "r") as f:
                # f.write(f"{website}, {email}, {password}\n")
                data = json.load(f)
                data.update(new_data)
            with open("data.json", "w") as f:
                json.dump(data, f, indent=4)
        except FileNotFoundError:
            with open("data.json", "w") as f:
                json.dump(new_data, f, indent=4)


        password_input.delete(0, END)
        website_input.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.minsize(250, 250)
window.config(padx=50, pady=50,)

canvas = Canvas(width=230, height=230, highlightthickness=0)
image = PhotoImage(file="logo4.png")
canvas.create_image(115, 115, image= image)
# canvas.config(highlightthickness=0)
# timer_text = canvas.create_text(115, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=2, row=1)

#..........................LABELS.................................
website_label = Label(text="Website:")
website_label.grid(column= 1, row=2)
website_label.config(padx=5, pady=5)

email_label = Label(text="Email/Username:")
email_label.grid(column= 1, row=3)
email_label.config(padx=5, pady=5)

password_label = Label(text= "Password:")
password_label.grid(column= 1, row=4)
password_label.config(padx=5, pady=7)



#............................INPUT FIELDS...............................
website_input = Entry(width=56)
website_input.grid(column= 2, row=2, columnspan= 3)
website_input.focus()
email_input = Entry(width=56)
email_input.grid(column= 2, row=3, columnspan= 4)
email_input.insert(0, "example@gmail.com")

password_input = Entry(width=37)
password_input.grid(column= 2, row=4)


# ------------------------SEARCH DATA-----------------------------------
def search_function():
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
            search_item = website_input.get()
            if search_item in data:
                password_for_copy = data[search_item]["password"]
                pyperclip.copy(password_for_copy)
                mb.showinfo(title="Data Found",
                            message=f"Website: {search_item}\n "
                                    f"Email: {data[search_item]["email"]}\n "
                                    f"Password: {data[search_item]["password"]}")
            else:
                mb.showinfo(title="Error", message=f"No details for the {search_item} exits")
    except FileNotFoundError:
        mb.showinfo(title="Error", message="No Data File Found")




#..........................BUTTONS...............
generate_password_button = Button(text="Generate Password", command=password_generator)
generate_password_button.grid(column= 3, row=4)

add_button = Button(text="Add Password", width=48, command=add_password)
add_button.grid(column= 2, row=5, columnspan= 5)

search_button = Button(text="Search", width=14, command=search_function)
search_button.grid(column= 3, row=2)


window.mainloop()
