import os
import tkinter as tk
from tkinter import colorchooser


class Options:
    def __init__(self, app, update_ui_callback):
        self.selected_cryptography = None
        self.text_size_scale = None

        self.text_color = None
        self.background_color = None
        self.text_size = None

        self.app = app
        self.options_window = None
        self.update_ui_callback = update_ui_callback
        self.config_file = os.path.join(os.getenv('APPDATA'), 'password_manager', 'options.conf')

    def save_config(self, text_size, text_color, bg_color):
        self.text_size = text_size
        self.text_color = text_color
        self.background_color = bg_color
        with open(self.config_file, "w") as f:
            f.write(f"TextSize={text_size}\n")
            f.write(f"TextColor={text_color}\n")
            f.write(f"BgColor={bg_color}\n")

    def load_file(self):
        if not os.path.exists(os.path.dirname(self.config_file)):
            os.makedirs(os.path.dirname(self.config_file))
        else:
            try:
                with open(self.config_file, "r") as f:
                    for line in f:
                        key, value = line.strip().split("=")
                        if key == "TextSize" and len(value) != 0 and value[0] != ".":
                            self.text_size = value
                            self.app.root.option_add("*Font", f"Arial {value}")
                        elif key == "TextColor" and len(value) != 0:
                            self.text_color = value
                            self.app.root.option_add("*foreground", value)
                        elif key == "BgColor" and len(value) != 0:
                            self.background_color = value
                            self.app.root.config(bg=value)
                            self.change_widget_bg_color(self.app.root, value)

                if self.options_window:
                    self.options_window.config(bg=self.background_color)
                    self.change_widget_bg_color(self.options_window, self.background_color)
                    self.change_widget_text_color(self.options_window, self.text_color)
                    self.text_size_scale.set(self.text_size)

            except FileNotFoundError:
                print("No options configuration file found. Using default settings.")

    def show_options_window(self):
        self.options_window = tk.Toplevel(self.app.root, bg=self.background_color)
        self.options_window.title("Options")

        tk.Label(self.options_window, text="Adjust Text Size:", fg=self.text_color,
                 bg=self.background_color).pack()

        self.text_size_scale = tk.Scale(self.options_window, from_=8, to=20, orient="horizontal", fg=self.text_color,
                                        bg=self.background_color)
        self.text_size_scale.pack()
        self.text_size_scale.set(self.text_size)

        text_color_button = tk.Button(self.options_window, text="Choose Text Color", pady=5,
                                      command=self.choose_text_color, fg=self.text_color,
                                      bg=self.background_color)
        text_color_button.pack()

        bg_color_button = tk.Button(self.options_window, text="Choose Background Color", pady=5,
                                    command=self.choose_bg_color, fg=self.text_color,
                                    bg=self.background_color)
        bg_color_button.pack()

        apply_button = tk.Button(self.options_window, text="Apply", pady=5,
                                 command=lambda: self.apply_changes(),
                                 bg=self.background_color)
        apply_button.pack()

        cryptography_label = tk.Label(self.options_window, text="Select Cryptography Type:", fg=self.text_color,
                                      bg=self.background_color)
        cryptography_label.pack()
        cryptography_options = ["AES", "RSA", "DES", "Blowfish", "Twofish"]
        self.selected_cryptography = tk.StringVar(self.options_window)
        self.selected_cryptography.set(cryptography_options[0])
        cryptography_dropdown = tk.OptionMenu(self.options_window, self.selected_cryptography, *cryptography_options)
        cryptography_dropdown.config(fg=self.text_color, bg=self.background_color)
        cryptography_dropdown.pack()

    def choose_text_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.text_color = color

    def choose_bg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.background_color = color

    def apply_changes(self):
        self.app.root.option_get('foreground', 'Label')
        self.app.root.cget('bg')

        self.text_size = self.text_size_scale.get()
        self.text_size_scale.set(self.text_size)
        self.change_widget_text_size(self.app.root, self.text_size)
        self.change_widget_text_size(self.options_window, self.text_size)

        self.options_window.config(bg=self.background_color)
        self.app.root.config(bg=self.background_color)
        self.change_widget_bg_color(self.app.root, self.background_color)

        self.change_widget_text_color(self.options_window, self.text_color)
        self.change_widget_text_color(self.app.root, self.text_color)

        self.save_config(self.text_size, self.text_color, self.background_color)
        self.update_ui_callback(self.text_size, self.text_color, self.background_color)

        self.options_window.destroy()

    def change_widget_text_size(self, widget, size):
        widget.option_add("*Font", f"Arial {size}")
        for child in widget.winfo_children():
            self.change_widget_text_size(child, size)

    def change_widget_bg_color(self, widget, color):
        if widget.winfo_name() == "strength" or widget.winfo_name == "icon":
            return
        widget.config(bg=color)
        for child in widget.winfo_children():
            self.change_widget_bg_color(child, color)

    def change_widget_text_color(self, widget, color):
        widget.option_add("*foreground", color)
        for child in widget.winfo_children():
            self.change_widget_text_color(child, color)

# David Pinheiro
