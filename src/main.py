from echo_vision.factory.gui_factory import CTkWidgetFactory
from echo_vision.views.main_window import App
from echo_vision.logic.cloud_capture import run_live_capture_pipeline, run_measurement_pipeline
from echo_vision.logic.rgb_capture import rgb_live_pipeline
def main():
    factory = CTkWidgetFactory()
    app = App(widget_factory=factory, button_action=run_live_capture_pipeline, button_action_2=run_measurement_pipeline, button_action_3=rgb_live_pipeline)
    app.mainloop()
         
if __name__ == "__main__":
	main()
