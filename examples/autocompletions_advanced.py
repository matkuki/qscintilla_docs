
"""
Autocompletions - Advanced
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
Autocompletion options - Basic
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
# when the autocompletion window will always be displayed.
editor.setAutoCompletionUseSingle(QsciScintilla.AcusNever)

"""
Autocompletion options - Advanced
"""
# Create a lexer for the editor and initialize it's QsciAPIs object
my_lexer = QsciLexerCPP()
api = QsciAPIs(my_lexer)
# Set the editor's lexer
editor.setLexer(my_lexer)
# Register an image that will be displayed with an autocompletion
autocompletion_image = QPixmap("marker_image.png")
editor.registerImage(1, autocompletion_image)
# Create a list of autocompletions
autocompletions = [
    "test_autocompletion",
    "autocompletion_with_image?1",
    "another_autocompletion",
    "subtract?1(int arg_1, float arg_2) Subtract function", # This call tip has a description and an image
    "entry_that_will_be_removed_later"
]
# Add the functions to the api
for ac in autocompletions:
    api.add(ac)
# Example of removing an entry
api.remove("entry_that_will_be_removed_later")
# Prepare the QsciAPIs instance information
api.prepare()

"""
Now that the QsciAPIs instance is prepared, it is not possible to add or remove
entry using the add/remove function! You have to create a new QsciAPIs instance
and add the information again!
"""

# Create the main window
main_window = QMainWindow()
main_window.setCentralWidget(editor)
main_window.resize(800, 600)
main_window.show()

# Execute the application
application.exec_()