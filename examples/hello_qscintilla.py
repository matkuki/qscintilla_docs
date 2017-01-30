
"""
Created by Matic Kukovec
"""

# Import the PyQt5 module with some of the GUI widgets
import PyQt5.QtWidgets
# Import the QScintilla module
import PyQt5.Qsci
# Import Python's sys module needed to get the application arguments
import sys

# Create the main PyQt application object
application = PyQt5.QtWidgets.QApplication(sys.argv)

# Create a QScintila editor instance
editor = PyQt5.Qsci.QsciScintilla()
print(sys.getrefcount(editor))

# Show the editor
editor.show()
# Put the “Hello World” text into the editing area of the editor
editor.setText("Hello World")

# Execute the application
application.exec_()
