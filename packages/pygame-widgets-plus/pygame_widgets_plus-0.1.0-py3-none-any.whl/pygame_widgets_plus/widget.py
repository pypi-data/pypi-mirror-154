# import pygame
from abc import ABC, abstractmethod


class WidgetBase(ABC):
    def __init__():
        super().__init__()
        self._x = 0
        self._y = 0
        self._value = None
        
        self._onMousePressed = None
        self._onMousePressedArgs = None
        
        self._onMouseReleased = None
        self._onMouseReleasedArgs = None
        
        self._onMouseMoved = None
        self._onMouseMovedArgs = None
        
        self._show = True
        pass

    def show(self):
        self._show = True

    def hide(self):
        self._show = False

    def value(self):
        return self._value

    def value(self, value):
        self._value = value

    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def draw(self):
        pass