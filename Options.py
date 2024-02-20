import os
import tkinter as tk
from tkinter import colorchooser


class Options:
    def __init__(self, app):
        self.text_size_scale = None
        self.app = app
        self.options_window = None
        self.config_file = os.path.join(os.getenv('APPDATA'), 'password_manager', 'options.conf')

    def save_config(self, text_size, text_color, bg_color):
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
                        if key == "TextSize" and len(value) != 0:
                            self.app.root.option_add("*Font", f"Arial {value}")
                        elif key == "TextColor" and len(value) != 0:
                            self.app.root.option_add("*foreground", value)
                        elif key == "BgColor" and len(value) != 0:
                            self.app.root.config(bg=value)
                            self.change_widget_bg_color(self.app.root, value)  # Change background color of all widgets
            except FileNotFoundError:
                print("No options configuration file found. Using default settings.")

    def show_options_window(self):
        self.options_window = tk.Toplevel(self.app.root)
        self.options_window.title("Options")

        tk.Label(self.options_window, text="Adjust Text Size:").pack()

        self.text_size_scale = tk.Scale(self.options_window, from_=8, to=20, orient="horizontal")
        self.text_size_scale.pack()

        text_color_button = tk.Button(self.options_window, text="Choose Text Color", pady=5,
                                      command=self.choose_text_color)
        text_color_button.pack()

        bg_color_button = tk.Button(self.options_window, text="Choose Background Color", pady=5,
                                    command=self.choose_bg_color)
        bg_color_button.pack()

        apply_button = tk.Button(self.options_window, text="Apply", pady=5,
                                 command=lambda: self.apply_changes(self.text_size_scale.get()))
        apply_button.pack()

    def choose_text_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.change_widget_text_color(self.app.root, color)
            self.save_config(self.text_size_scale.get(), color, self.app.root.cget('bg'))
            text_color = self.app.root.option_get('foreground', 'Label')
            bg_color = self.app.root.cget('bg')
            self.save_config(self.text_size_scale.get(), text_color, bg_color)
            self.options_window.destroy()

    def change_widget_text_color(self, widget, color):
        widget.option_add("*foreground", color)
        for child in widget.winfo_children():
            self.change_widget_text_color(child, color)

    def choose_bg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.app.root.config(bg=color)
            self.change_widget_bg_color(self.app.root, color)
            text_color = self.app.root.option_get('foreground', 'Label')
            bg_color = self.app.root.cget('bg')
            self.save_config(self.text_size_scale.get(), text_color, bg_color)
            self.options_window.destroy()

    def apply_changes(self, text_size):
        text_color = self.app.root.option_get('foreground', 'Label')
        bg_color = self.app.root.cget('bg')
        self.app.root.option_add("*Font", f"Arial {text_size}")
        self.save_config(text_size, text_color, bg_color)
        self.options_window.destroy()

    def change_widget_bg_color(self, widget, color):
        widget.config(bg=color)
        for child in widget.winfo_children():
            self.change_widget_bg_color(child, color)