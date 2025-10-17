from abc import ABC, abstractmethod

class WidgetFactory(ABC):
    @abstractmethod
    def create_widget(self, widget_type: str, master, **kwargs):
        """Create and Return based on the specified type"""
        pass