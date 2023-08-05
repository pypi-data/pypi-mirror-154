from PyQt5.QtWidgets import *
from . import create_figures_gui5
import sys

    


#Call GUI
if __name__ == '__main__':
    # Create the Qt Application
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    gui = create_figures_gui5.GuiCL() # <<-- Create an instance
    gui.show()
    QApplication.setQuitOnLastWindowClosed(True)
    app.exec_()
    app.quit()

