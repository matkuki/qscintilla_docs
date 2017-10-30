
"""
Call tips example
"""

# Import everything we need
import sys
import time
import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qsci import *

# Create the main PyQt application object
application = QApplication(sys.argv)

# Create a QScintila editor instance
editor = QsciScintilla()

"""
Setup the call tip options
"""
# Select the context at which the call tips are displayed.
# This selects when call tips are active, depending of the 
# scope like a C++ namespace or Python module.
editor.setCallTipsStyle(QsciScintilla.CallTipsNoContext)
# Set the number of calltips that will be displayed at one time.
# 0 shows all applicable call tips.
editor.setCallTipsVisible(0)
# This selects the position at which the call tip rectangle will appear.
# If it is not possible to show the call tip rectangle at the selected position
# because it would be displayed outside the bounds of the document, it will be
# displayed where it is possible.
editor.setCallTipsPosition(QsciScintilla.CallTipsAboveText)
# Select the various highlight colors
# Background
editor.setCallTipsBackgroundColor(QColor(0xff, 0xff, 0xff, 0xff))
# Text
editor.setCallTipsForegroundColor(QColor(0x50, 0x50, 0x50, 0xff))
# Current argument text
editor.setCallTipsHighlightColor(QColor(0xff, 0x00, 0x00, 0xff))

# Create a lexer for the editor and initialize it's QsciAPIs object
my_lexer = QsciLexerCPP()
api = QsciAPIs(my_lexer)

# Create a function list that will be used by the autocompletions and call tips.
# The difference between a call tip and an autocompletion is that the call tip
# has also the arguments defined!
# In the example 'funcs' list below the first item is a call tip and
# the second item is an autocompletion.
funcs = [
    "test_autocompletion",
    "add(int arg_1, float arg_2)", 
    "subtract(int arg_1, test arg_2)", 
    "subtract(float arg_1, float arg_2)", 
    "subtract(test arg_1, test arg_2)", 
    "divide(float div_1, float div_2)",
    "some_func(arg_3)"
]
# Add the functions to the api
for s in funcs:
    api.add(s)

# Prepare the QsciAPIs instance
api.prepare()

# Set the editor's lexer
editor.setLexer(my_lexer)
# Autocompletion options (this is not necessary)
editor.setAutoCompletionThreshold(1)
editor.setAutoCompletionSource(QsciScintilla.AcsAll)
editor.setAutoCompletionCaseSensitivity(False)

# Create the main window
main_window = QMainWindow()
main_window.setCentralWidget(editor)
main_window.resize(800, 600)
main_window.show()

# Execute the application
application.exec_()
