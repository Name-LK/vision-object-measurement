import customtkinter

class ButtonCreator:
    def __init__(self):
        customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        self.app = customtkinter.CTk()  # create CTk window like you do with the Tk window
        self.app.geometry("400x240")

    def create_button(self, name, command):
        button = customtkinter.CTkButton(master=self.app, text=name, command=command)
        button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
        self.app.mainloop()

def button_pressed():
    print("PRESSED")

if __name__ == "__main__":
    creator = ButtonCreator()
    creator.create_button(name='button', command=button_pressed)