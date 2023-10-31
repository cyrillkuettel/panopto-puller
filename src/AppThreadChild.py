from AppThreadBase import AppThreadBase
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QWidget


class AppThreadChild(QWidget, AppThreadBase):
    def __int__(self, **kwargs):
        super().__init__()


if __name__ == "__main__":
    print(type(QMainWindow))
    print(type(AppThreadBase))
