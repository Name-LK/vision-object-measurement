from factory.gui_factory import CTkWidgetFactory
from view.main_window import App
from logic.live_capture import run_live_capture

factory = CTkWidgetFactory()
app = App(widget_factory=factory, button_action=run_live_capture)
app.mainloop()