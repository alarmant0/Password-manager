import random
import string
import tkinter as tk
from tkinter import messagebox
import webbrowser

from Options import Options
from PasswordStrengthChecker import PasswordStrengthChecker
from Safe import Safe


def generate_random_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def get_help():
    link = "https://github.com/alarmant0/Password-manager/blob/main/README.md"
    webbrowser.open_new_tab(link)


class PasswordManager:
    def __init__(self):

        self.passwords_window = None
        self.current_entry = None

        self.file_menu = None
        self.edit_menu = None
        self.help_menu = None
        self.menu_bar = None

        self.button_generate = None
        self.button_options = None

        self.password_var = None
        self.passwords = None

        self.button_get_all = None

        self.entry_username = None
        self.label_username = None

        self.button_add = None

        self.entry_service = None
        self.label_service = None

        self.strength_bar = None

        self.frame = None
        self.login_frame = None

        self.entry_password = None
        self.label_password = None

        self.button_login = None

        self.safe = Safe()
        self.options = Options(self, self.update_ui)

        self.root = tk.Tk()
        self.root.title("Password Manager")

        self.login_window()

    def update_ui(self, text_size, text_color, bg_color):
        self.label_service.config(font=("Arial", text_size), fg=text_color)
        self.entry_service.config(font=("Arial", text_size), fg=text_color)

        self.label_username.config(font=("Arial", text_size), fg=text_color)
        self.entry_username.config(font=("Arial", text_size), fg=text_color)

        self.label_password.config(font=("Arial", text_size), fg=text_color)
        self.entry_password.config(font=("Arial", text_size), fg=text_color)

        self.button_generate.config(font=("Arial", text_size), fg=text_color, bg=bg_color)
        self.button_add.config(font=("Arial", text_size), fg=text_color, bg=bg_color)
        self.button_get_all.config(font=("Arial", text_size), fg=text_color, bg=bg_color)
        self.button_options.config(font=("Arial", text_size), fg=text_color, bg=bg_color)

        self.options.background_color = bg_color
        self.options.text_color = text_color
        self.options.text_size_scale = text_size

        self.frame.config(bg=bg_color)

    def login_window(self):
        self.options.load_file()

        self.login_frame = tk.Frame(self.root, bg=self.options.background_color)
        self.login_frame.pack(padx=10, pady=10)

        self.label_password = tk.Label(self.login_frame, text="Enter Password:",
                                       fg=self.options.text_color, bg=self.options.background_color)

        self.label_password.grid(row=0, column=0, sticky="w")
        self.entry_password = tk.Entry(self.login_frame, show="*",
                                       fg=self.options.text_color, bg=self.options.background_color)

        self.entry_password.grid(row=0, column=1)
        self.entry_password.bind("<Return>", lambda event: self.login())
        self.entry_password.focus_set()

        self.button_login = tk.Button(self.login_frame, text="Login", command=self.login,
                                      fg=self.options.text_color, bg=self.options.background_color)
        self.button_login.grid(row=1, column=0, columnspan=2, pady=5)

    def login(self):
        password = self.entry_password.get()
        # hashlib thing
        if password == "123":
            self.login_frame.destroy()
            self.initialize_main_app()

    def initialize_main_app(self):
        self.frame = tk.Frame(self.root, name="main_frame")
        self.frame.pack(padx=10, pady=10)

        self.options.load_file()
        self.menu_bar = tk.Menu(self.root, name="menu")

        icon_img = tk.PhotoImage(file="./assets/icon.ico")
        self.root.iconphoto(False, icon_img)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0, name="file_menu")
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0, name="edit_menu")
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        self.help_menu = tk.Menu(self.menu_bar, tearoff=0, name="help_menu")
        self.help_menu.add_command(label="About", command=get_help)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        self.root.config(menu=self.menu_bar)

        self.label_service = tk.Label(self.frame, text="Service:",
                                      fg=self.options.text_color, bg=self.options.background_color
                                      , name="label_service")
        self.label_service.grid(row=0, column=0, sticky="w")
        self.entry_service = tk.Entry(self.frame, name="entry_service")
        self.entry_service.grid(row=0, column=1)
        self.entry_service.focus_set()
        self.current_entry = self.entry_service
        self.entry_service.bind("<Down>", lambda event: self.down_handler())
        self.entry_service.bind("<Up>", lambda event: self.up_handler())
        self.entry_service.bind("<Return>", lambda event: self.add_password())

        self.label_username = tk.Label(self.frame, text="Username:",
                                       fg=self.options.text_color, bg=self.options.background_color,
                                       name="label_username")
        self.label_username.grid(row=1, column=0, sticky="w")
        self.entry_username = tk.Entry(self.frame, name="entry_username")
        self.entry_username.grid(row=1, column=1)
        self.entry_username.bind("<Down>", lambda event: self.down_handler())
        self.entry_username.bind("<Up>", lambda event: self.up_handler())
        self.entry_username.bind("<Return>", lambda event: self.add_password())

        self.label_password = tk.Label(self.frame, text="Password:",
                                       fg=self.options.text_color, bg=self.options.background_color
                                       , name="label_password")
        self.label_password.grid(row=2, column=0, sticky="w")

        self.entry_password = tk.Entry(self.frame, textvariable=self.password_var, name="entry_password")
        self.entry_password.grid(row=2, column=1)
        self.entry_password.bind("<Down>", lambda event: self.down_handler())
        self.entry_password.bind("<Up>", lambda event: self.up_handler())
        self.entry_password.bind("<Return>", lambda event: self.add_password())

        self.strength_bar = tk.Label(self.frame, text=" ", name="strength", width=17, height=1,
                                     bg="red")
        self.strength_bar.grid(row=2, column=5)

        self.entry_password.bind("<KeyRelease>", lambda event: self.update_strength_bar())

        self.button_generate = tk.Button(self.frame, text="Generate Password", command=self.generate_password)
        self.button_generate.grid(row=4, column=5, padx=10)

        self.button_add = tk.Button(self.frame, text="Add Password", command=self.add_password)
        self.button_add.grid(row=3, column=0, columnspan=2, pady=5)

        self.button_get_all = tk.Button(self.frame, text="Retrieve All Passwords", command=self.get_passwords)
        self.button_get_all.grid(row=4, column=0, columnspan=2)

        self.button_options = tk.Button(self.frame, text="Options", command=self.open_options_window)
        self.button_options.grid(row=5, column=0, columnspan=2, pady=5)

        self.options.load_file()

    def update_strength_bar(self):
        password = self.entry_password.get()
        strength = PasswordStrengthChecker.check_strength(password)
        self.strength_bar.config(bg=strength)

    def add_password(self):
        service = self.entry_service.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        if len(service) == 0 or len(username) == 0 or len(password) == 0:
            messagebox.showerror("Error", "Please fill in all fields.")
        else:
            self.safe.save_pass(service, username, password)
            self.entry_service.delete(0, tk.END)
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            self.update_strength_bar()

    def generate_password(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Password Length")
        dialog.configure(bg=self.options.background_color)
        label = tk.Label(dialog, text="Enter password length:",
                         fg=self.options.text_color, bg=self.options.background_color)
        label.pack()
        entry = tk.Entry(dialog, fg=self.options.text_color, bg=self.options.background_color)
        entry.pack()
        entry.bind("<Return>", lambda event: ok_button_click())

        def ok_button_click():
            length = entry.get()

            if length.isdigit():
                if int(length) <= 0 or int(length) > 20:
                    messagebox.showerror("Error", "Between 1 and 20")
                    return
                password = generate_random_password(int(length))
                self.entry_password.delete(0, tk.END)
                self.entry_password.insert(0, password)
                dialog.destroy()
                self.update_strength_bar()

        ok_button = tk.Button(dialog, text="OK", command=ok_button_click,
                              fg=self.options.text_color, bg=self.options.background_color)
        ok_button.pack()

        entry.focus_set()

        dialog.grab_set()
        self.root.wait_window(dialog)

    def get_passwords(self):
        lines = self.safe.get_passwords()

        self.passwords_window = tk.Toplevel(self.root, bg=self.options.background_color)
        self.passwords_window.title("All Passwords")

        filter_var = tk.StringVar()
        tk.Label(self.passwords_window, text="Filter by Service:", bg=self.options.background_color).grid(row=0, column=0)
        filter_entry = tk.Entry(self.passwords_window, textvariable=filter_var, bg=self.options.background_color)
        filter_entry.grid(row=0, column=1)

        def delete_password(service, username):
            self.safe.delete_pass(service, username)
            filter_passwords()
            for widget in self.passwords_window.winfo_children():
                print(widget.cget("text"))
                self.passwords_window.winfo_children.destroy()
                widget.grid_forget()
                widget.destroy()

                filter_passwords()
                break

        def filter_passwords():
            filter_text = filter_var.get().lower()
            row = 1
            max_passwords = 10
            passwords_displayed = 0
            for line in lines:
                if passwords_displayed >= max_passwords:
                    break
                elements = line.split(":")
                if len(elements) == 3:
                    service, username, encrypted_password = elements
                    plain_password = self.safe.decrypt(encrypted_password)
                    if filter_text in service.lower():
                        tk.Label(self.passwords_window,
                                 text=f"Service: {service}, Username: {username}, Password: {plain_password}",
                                 bg=self.options.background_color).grid(row=row, column=0, columnspan=2)
                        tk.Button(self.passwords_window, text="Delete",
                                  command=lambda s=service, u=username: delete_password(s, u)).grid(row=row, column=2)
                        row += 1
                        passwords_displayed += 1

        filter_passwords()

        tk.Button(self.passwords_window, text="Filter", command=filter_passwords, bg=self.options.background_color).grid(
            row=0, column=2)

        filter_entry.bind("<Return>", lambda event: filter_passwords())

    def open_options_window(self):
        self.options.show_options_window()

    def run(self):
        self.root.mainloop()

    def down_handler(self):
        if self.current_entry == self.entry_service:
            self.entry_username.focus_set()
            self.current_entry = self.entry_username
        elif self.current_entry == self.entry_username:
            self.entry_password.focus_set()
            self.current_entry = self.entry_password
        else:
            pass

    def up_handler(self):
        if self.current_entry == self.entry_password:
            self.entry_username.focus_set()
            self.current_entry = self.entry_username
        elif self.current_entry == self.entry_username:
            self.entry_service.focus_set()
            self.current_entry = self.entry_service
        else:
            pass


if __name__ == "__main__":
    password_manager = PasswordManager()
    password_manager.run()

# David Pinheiro
