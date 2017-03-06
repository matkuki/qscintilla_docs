    
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
# Set the initial text
editor.setText("Inicialization example.")
# Append some text
editor.append("\nAdded text.\n")

"""
General cutomizations
"""
# Set the background color of all margins EXCEPT 
# SymbolMarginDefaultForegroundColor and SymbolMarginDefaultBackgroundColor.
# If this is not set it defaults to gray.
editor.setMarginsBackgroundColor(PyQt5.QtGui.QColor(0x8a, 0x00, 0x34, 80))
# Set the foreground color (the text on margins) of all margins.
# If this is not set it defaults to Black.
editor.setMarginsForegroundColor(PyQt5.QtGui.QColor(0x00, 0x00, 0xff, 0xff))

"""
Line number margin
"""
# Set margin 0 as the line margin (this is the default, so you can skip this step)
# One way is to set the margins type with 'setMarginType', 
# the other way is to use the 'setMarginLineNumbers' function.
if True:
    editor.setMarginType(0, PyQt5.Qsci.QsciScintilla.NumberMargin)
else:
    # This function can also be used on a margin of a type other then
    # NumberMargin, but then the line numbers overlap or overwrite 
    # the other content of the margin
    editor.setMarginLineNumbers(0, True)
# Set the width of the line number margin with a string, which sets the width
# to the width of the entered string text. There is also an alternative function
# with the same name which you can use to set the width directly in number of pixels.
editor.setMarginWidth(0, "00")

"""
Symbol margin - Used to display custom symbols
"""
# Set margin 1 as a symbol margin (this is the default, so you can skip this step)
editor.setMarginType(1, PyQt5.Qsci.QsciScintilla.SymbolMargin)
# Set the margin's width
editor.setMarginWidth(1, 20)
# Prepare an image for the marker
image_scale_size = PyQt5.QtCore.QSize(16, 16)
marker_image = PyQt5.QtGui.QPixmap("marker_image.png")
scaled_image = marker_image.scaled(image_scale_size)
# Set the margin mask (mask constant ~SC_MASK_FOLDERS enables all markers!)
# This sets which of the 32 markers will be visible on margin 1
editor.setMarginMarkerMask(
    1, 0b1111111111111111111111111 #~PyQt5.Qsci.QsciScintillaBase.SC_MASK_FOLDERS 
)
# Just for info we display the margin mask, which should be: 0b1111111111111111111111111
# which means all 32 markers are enabled.
editor.append("Margin 1 marker mask: {}".format(bin(editor.marginMarkerMask(1))))
# Create and add marker on margin 1 and add it to line 0
marker = editor.markerDefine(scaled_image, 1)
editor.markerAdd(1, 1)
editor.setMarkerBackgroundColor(PyQt5.QtGui.QColor(0x8a, 0xe2, 0x34, 80), -1)

"""
Symbol margin with the background color set to the editor's default paper (background) color
"""
# Set margin 2 as a symbol margin with customizable background color
editor.setMarginType(2, PyQt5.Qsci.QsciScintilla.SymbolMarginDefaultBackgroundColor)
# Set the margin's width
editor.setMarginWidth(2, "000000")

"""
Symbol margin with the background color set to the editor's default font color
"""
# Set margin 3 as a symbol margin with customizable background color
editor.setMarginType(3, PyQt5.Qsci.QsciScintilla.SymbolMarginDefaultForegroundColor)
# Set the margin's width
editor.setMarginWidth(3, "0000")
# Set the margin mask to display all markers
editor.setMarginMarkerMask(
    3, 0b1111111111111111111111111
)
# Add a marker that is built into QScintilla.
# Note that the marker will be displayed on all symbol margins with the 
# third marker bit set to '1'!
marker = editor.markerDefine(PyQt5.Qsci.QsciScintilla.Rectangle, 2)
editor.markerAdd(0, 2)

"""
Text margin
"""
# Set margin 4 as a symbol margin with customizable background color
editor.setMarginType(4, PyQt5.Qsci.QsciScintilla.TextMargin)
# Set the margin's width
editor.setMarginWidth(4, "00000")
# Set the margin's text on line 1 font style 0 (Style 0 is taken from the current lexer, I think!)
# 'setMarginText' function sets the text to every Text margin, if you have more than one.
editor.setMarginText(0, "line1", 0)
# Create a new style and set it on line 2 with some text
style = PyQt5.Qsci.QsciStyle(
    2, # style (This has to be set to something other than 0, as that is the default)
    "new style", # description
    PyQt5.QtGui.QColor(0x8a, 0xe2, 0x34, 80), # color (font)
    PyQt5.QtGui.QColor(0xff, 0xff, 0x00, 0xff), # paper (background)
    PyQt5.QtGui.QFont('Helvetica', 10), # font
    eolFill=False, # End-Of-Line Fill
)
editor.setMarginText(1, "line2", style)

"""
More marker examples
"""
# Define a marker using an ASCII character
marker = editor.markerDefine("T", 2)
editor.markerAdd(0, 2)

# For the QScintilla editor to properly process events we need to add it to
# a QMainWindow object.
main_window = PyQt5.QtWidgets.QMainWindow()
# Set the central widget of the main window to be the editor
main_window.setCentralWidget(editor)
# Resize the main window and show it on the screen
main_window.resize(800, 600)
main_window.show()

# Execute the application
application.exec_()
