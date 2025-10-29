import customtkinter
from echo_vision.factory.gui_factory import CTkWidgetFactory

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self, widget_factory, button_action, button_action_2):
        super().__init__()

        self.widget_factory = widget_factory
        self.button_action = button_action
        self.button_action_2 = button_action_2

        self.title("Title example")
        self.geometry("400x300")

        self._create_widgets()

    def _create_widgets(self):
        info_label = self.widget_factory.create_widget(
            "label",
            master=self,
            text="Widgets created succesfully!"
        )
        info_label.pack(pady=20, padx=20)

        main_button = self.widget_factory.create_widget(
            "button",
            master=self,
            text="Live Capture",
            command=self.button_action
        )
        main_button.pack(pady=10, padx=20)

        my_entry = self.widget_factory.create_widget(
            "button",
            master=self,
            text="Live Mesurement",
            command=self.button_action_2
        )
        my_entry.pack(pady=10, padx=20)
    
    def button_function(self):
        """Function to run when button is pressed"""
        print("Button Pressed")