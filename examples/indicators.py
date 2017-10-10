
"""
Various examples of indicators
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
editor.setText(
"""This is line 1.
This is line 2.
This is line 3.
This is line 4.
This is line 5.
This is line 6.
This is line 7."""
)


"""
Indicator initialization
"""
indicator_number = 0
indicator_value = 222
indicator_color = PyQt5.QtGui.QColor(0xff, 0x00, 0xff, 0xff)
indicator_hover_color = PyQt5.QtGui.QColor(0x8a, 0x8a, 0x00)
draw_under_text = True
# Define the indicator type.
# 32 IS THE MAXIMUM NUMBER OF DIFFERENT TYPES OF INDICATORS!
"""
The indicator styles are:
    PyQt5.Qsci.QsciScintilla.PlainIndicator
    PyQt5.Qsci.QsciScintilla.SquiggleIndicator
    PyQt5.Qsci.QsciScintilla.TTIndicator
    PyQt5.Qsci.QsciScintilla.DiagonalIndicator
    PyQt5.Qsci.QsciScintilla.StrikeIndicator
    PyQt5.Qsci.QsciScintilla.HiddenIndicator
    PyQt5.Qsci.QsciScintilla.BoxIndicator
    PyQt5.Qsci.QsciScintilla.RoundBoxIndicator
    PyQt5.Qsci.QsciScintilla.StraightBoxIndicator
    PyQt5.Qsci.QsciScintilla.FullBoxIndicator
    PyQt5.Qsci.QsciScintilla.DashesIndicator
    PyQt5.Qsci.QsciScintilla.DotsIndicator
    PyQt5.Qsci.QsciScintilla.SquiggleLowIndicator
    PyQt5.Qsci.QsciScintilla.DotBoxIndicator
    PyQt5.Qsci.QsciScintilla.SquigglePixmapIndicator
    PyQt5.Qsci.QsciScintilla.ThickCompositionIndicator
    PyQt5.Qsci.QsciScintilla.ThinCompositionIndicator
    PyQt5.Qsci.QsciScintilla.TextColorIndicator
    PyQt5.Qsci.QsciScintilla.TriangleIndicator
    PyQt5.Qsci.QsciScintilla.TriangleCharacterIndicator
"""
editor.indicatorDefine(
    PyQt5.Qsci.QsciScintilla.RoundBoxIndicator,
    indicator_number,
)
# Set the indicator's color
editor.setIndicatorForegroundColor(
    indicator_color, 
    indicator_number
)
# Set the indicator's color when the mouse hovers over it.
# THIS APPLIES TO INDICATORS THAT HAVE A BACKGROUND COLOR LIKE 'RoundBoxIndicator'!
editor.setIndicatorHoverForegroundColor(
    indicator_hover_color, 
    indicator_number
)
# Set the indicator's hover style (the styles are the same as with 'indicatorDefine')
editor.setIndicatorHoverStyle(
    PyQt5.Qsci.QsciScintilla.RoundBoxIndicator,
    indicator_number
)
# 
editor.setIndicatorDrawUnder(
    draw_under_text, 
    indicator_number
)

editor.SendScintilla(
    PyQt5.Qsci.QsciScintilla.SCI_SETINDICATORCURRENT,
    indicator_number
)
editor.SendScintilla(
    PyQt5.Qsci.QsciScintilla.SCI_SETINDICATORVALUE,
    indicator_number,
    0xffff
)

"""
Connect to the indicator signals for feedback when an indicator is clicked or
a mouse button is released over an indicator
"""
def indicator_click(line, index, keys):
    # Use the low level SendScintilla function to get the indicator's value
    position = editor.positionFromLineIndex(line, index)
    # The value can only be set using the low level API described at line 165
    # of this file. Otherwise the value will always be '1'.
    value = editor.SendScintilla(
        PyQt5.Qsci.QsciScintilla.SCI_INDICATORVALUEAT,
        indicator_number,
        position
    )
    # Display the information
    print("indicator clicked in line '{}', index '{}', value '{}'".format(line, index, value))

def indicator_released(line, index, keys):
    # Use the low level SendScintilla function to get the indicator's value
    position = editor.positionFromLineIndex(line, index)
    # The value can only be set using the low level API described at line 165
    # of this file. Otherwise the value will always be '1'.
    value = editor.SendScintilla(
        PyQt5.Qsci.QsciScintilla.SCI_INDICATORVALUEAT,
        indicator_number,
        position
    )
    # Display the information
    print("indicator released in line '{}', index '{}', value '{}'".format(line, index, value))

editor.indicatorClicked.connect(indicator_click)
editor.indicatorReleased.connect(indicator_released)


"""
Indicator usage
"""
# Fill an indicator over a couple of lines
editor.fillIndicatorRange(     
    0, # line from
    0, # column from
    0, # line to
    len(editor.text(0)), # column to
    indicator_number 
)
editor.fillIndicatorRange(     
    3, # line from
    0, # column from
    3, # line to
    len(editor.text(3)), # column to
    indicator_number 
)

# An example of how to remove an already filled indicator
editor.fillIndicatorRange(     
    4, # line from
    0, # column from
    4, # line to
    len(editor.text(4)), # column to
    indicator_number 
)
editor.clearIndicatorRange(     
    4, # line from
    0, # column from
    4, # line to
    len(editor.text(4)), # column to
    indicator_number 
)

"""
To add a value to an indicator that can later be retrieved by the click or release signals,
it is necessery to use the low level API to fill the indicator using SendScintilla!
"""
# Select the indicator
editor.SendScintilla(
    PyQt5.Qsci.QsciScintilla.SCI_SETINDICATORCURRENT,
    indicator_number
)
# Give it a value.
# This can be used for determinig how to handle the clicked/released indicator signals.
value = 123
editor.SendScintilla(
    PyQt5.Qsci.QsciScintilla.SCI_SETINDICATORVALUE,
    value
)
# Fill the indicator
fill_line = 4 # This is the 5th line in the document, as the indexes in Python start at 0!
start_position = editor.positionFromLineIndex(fill_line, 0)
length = len(editor.text(fill_line))
editor.SendScintilla(
    PyQt5.Qsci.QsciScintilla.SCI_INDICATORFILLRANGE,
    start_position,
    length
)

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