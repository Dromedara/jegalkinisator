from PyQt5.QtWidgets import QApplication, QWidget
from window_class import MW
import sys

def main():
    app = QApplication(sys.argv)
    # create the main window
    window = MW()
    # start the event loop
    sys.exit(app.exec())

if __name__ == '__main__':
    main()