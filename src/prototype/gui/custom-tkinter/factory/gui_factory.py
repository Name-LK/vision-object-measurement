from interfaces.gui_interface import WidgetFactory
import customtkinter

class CTkWidgetFactory(WidgetFactory):
    def create_widget(self, widget_type, master, **kwargs):
        widget_type = widget_type.lower()

        if widget_type == "button":
            return customtkinter.CTkButton(master=master, **kwargs)
        elif widget_type == "label":
            return customtkinter.CTkLabel(master=master, **kwargs)
        elif widget_type == "frame":
            return customtkinter.CTkFrame(master=master, **kwargs)
        elif widget_type == "entry":
            return customtkinter.CTkEntry(master=master, **kwargs)
        else:
            raise ValueError(f"Not supported widget type '{widget_type}'")