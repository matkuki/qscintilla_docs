
"""
Created by Matic Kukovec
"""

# Import the PyQt5 module with some of the GUI widgets
import PyQt5.QtWidgets
import PyQt5
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
editor.setText("Hello World\n")
# Append more text
for i in range(100):
    editor.append("This is line {}\n".format(i))
# Find a specific line
editor.findFirst("This is line 55", False, False, False, False, True)
# Find a specific line backwards
editor.findFirst("This is line 33", False, False, False, False, False)

# Execute the application
application.exec_()
