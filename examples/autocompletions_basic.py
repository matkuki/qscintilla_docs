
"""
Autocompletions - Basic
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
Autocompletion options
"""
# Set the autocompletion to be case IN-sensitive
editor.setAutoCompletionCaseSensitivity(False)
# Set the threshold at which the autocompletion window appears
editor.setAutoCompletionThreshold(1)
# Set the source from which the autocompletions will be pulled from
editor.setAutoCompletionSource(QsciScintilla.AcsAll)
# Sets whether the characters to the right of the autocompletion
# will be overwritten when an autocompletion is selected.
editor.setAutoCompletionReplaceWord(True)
# Select the behaviour of autocompletions when there is only a single
# entry in the autocompletion list. The selection below sets that
# when there is a single autocompletion, it is automatically selected
# and entered into the text.
editor.setAutoCompletionUseSingle(QsciScintilla.AcusAlways)


# Create the main window
main_window = QMainWindow()
main_window.setCentralWidget(editor)
main_window.resize(800, 600)
main_window.show()

# Execute the application
application.exec_()