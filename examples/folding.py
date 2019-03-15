
# Import the PyQt5 module with some of the GUI widgets
import PyQt5.QtWidgets
import PyQt5.QtGui
# Import the QScintilla module
import PyQt5.Qsci
# Import Python's sys module needed to get the application arguments
import sys

# Create the main PyQt application object
application = PyQt5.QtWidgets.QApplication(sys.argv)

# Create a QScintila editor instance
editor = PyQt5.Qsci.QsciScintilla()
# Set the folding style, margin 2 is the default margin for displayingfolding
editor.setFolding(PyQt5.Qsci.QsciScintilla.PlainFoldStyle, 2)
# Show the editor
editor.show()
# Put the some Python code into the editing area of the editor
editor.setText("""
def my_function():
    print("inside my_function")

def function_0():
    print("inside function_0")
    def nested_function():
        print("inside nested_function")
        a = 12
        b = 13
    nested_function()

if  __name__ == "__main__":
    my_function()
""")

# Example of manually folding the above Python code:
#0
#1  def my_function():
#2     print("inside my_function")
#3 
#4  def function_0():
#5      print("inside function_0")
#6      def nested_function():
#7          print("inside nested_function")
#8          a = 12
#9          b = 13
#10      nested_function()
#11 
#12 if  __name__ == "__main__":
#13     my_function()
#14
# Set 'def' line to level 0 and subsequent function lines to level 1
editor.SendScintilla(PyQt5.Qsci.QsciScintilla.SCI_SETFOLDLEVEL, 1, 0 | PyQt5.Qsci.QsciScintilla.SC_FOLDLEVELHEADERFLAG)
editor.SendScintilla(PyQt5.Qsci.QsciScintilla.SCI_SETFOLDLEVEL, 2, 1 | PyQt5.Qsci.QsciScintilla.SC_FOLDLEVELHEADERFLAG)
# End the current fold
editor.SendScintilla(PyQt5.Qsci.QsciScintilla.SCI_SETFOLDLEVEL, 3, 0)
# Again set 'def' line to level 0 and subsequent function lines to level 1
editor.SendScintilla(PyQt5.Qsci.QsciScintilla.SCI_SETFOLDLEVEL, 4, 0 | PyQt5.Qsci.QsciScintilla.SC_FOLDLEVELHEADERFLAG)
editor.SendScintilla(PyQt5.Qsci.QsciScintilla.SCI_SETFOLDLEVEL, 5, 1 | PyQt5.Qsci.QsciScintilla.SC_FOLDLEVELHEADERFLAG)
# Add another sub-level fold to the current fold, by setting it to a higher level
editor.SendScintilla(PyQt5.Qsci.QsciScintilla.SCI_SETFOLDLEVEL, 6, 1 | PyQt5.Qsci.QsciScintilla.SC_FOLDLEVELHEADERFLAG)
for i in range(7, 10):
    editor.SendScintilla(PyQt5.Qsci.QsciScintilla.SCI_SETFOLDLEVEL, i, 2 | PyQt5.Qsci.QsciScintilla.SC_FOLDLEVELHEADERFLAG)
# Set the level back to 1
editor.SendScintilla(PyQt5.Qsci.QsciScintilla.SCI_SETFOLDLEVEL, 10, 1 | PyQt5.Qsci.QsciScintilla.SC_FOLDLEVELHEADERFLAG)
# End the current fold
editor.SendScintilla(PyQt5.Qsci.QsciScintilla.SCI_SETFOLDLEVEL, 11, 0)
# Again set folding for the if statement
editor.SendScintilla(PyQt5.Qsci.QsciScintilla.SCI_SETFOLDLEVEL, 12, 0 | PyQt5.Qsci.QsciScintilla.SC_FOLDLEVELHEADERFLAG)
editor.SendScintilla(PyQt5.Qsci.QsciScintilla.SCI_SETFOLDLEVEL, 13, 1 | PyQt5.Qsci.QsciScintilla.SC_FOLDLEVELHEADERFLAG)
# End the current fold
editor.SendScintilla(PyQt5.Qsci.QsciScintilla.SCI_SETFOLDLEVEL, 14, 0)

# An example of folding the 'nested_function' in the above code.
editor.SendScintilla(PyQt5.Qsci.QsciScintilla.SCI_FOLDLINE, 6, 0)
# Folding options for SCI_FOLDLINE are:
#     0     Contract.
#     1     Expand.
#     2     Toggle between contracted and expanded.

# Execute the application
application.exec_()
