
"""
Created by Matic Kukovec
"""

# Import the PyQt5 module with some of the GUI widgets
import PyQt5.QtWidgets
import PyQt5.QtGui
import PyQt5.QtCore
# Import the QScintilla module
import PyQt5.Qsci
# Import Python's sys module needed to get the application arguments
import sys

"""
Custom editor with a simple commenting feature
similar to what Sublime Text does
"""
class MyCommentingEditor(PyQt5.Qsci.QsciScintilla):
    def keyPressEvent(self, event):
        # Execute the superclasses event
        super().keyPressEvent(event)
        # Check pressed key information
        key = event.key()
        key_modifiers = PyQt5.QtWidgets.QApplication.keyboardModifiers()
        if (key == PyQt5.QtCore.Qt.Key_K and 
            key_modifiers == PyQt5.QtCore.Qt.ControlModifier):
                self.comment()
    
    def comment(self):
        # Get the cursor information
        line_number, line_index = self.getCursorPosition()
        from_line, from_index, to_line, to_index = self.getSelection()
        # Check if there is selected text
        if from_line == -1 and from_index == -1:
            return
        # Set the selection from the beginning of the cursor line
        # to the end of the last selection line
        self.setSelection(
            from_line, 0, to_line, len(self.text(to_line))-1
        )
        # Get the selected text and split it into lines
        selected_text = self.selectedText()
        selected_list = selected_text.split("\n")
        # Add the commenting character to every line
        for i, line in enumerate(selected_list):
            selected_list[i] = line[:line_index] + "//" + line[line_index:]
        # Replace the whole selected text with the merged lines
        # containing the commenting characters
        self.replaceSelectedText("\n".join(selected_list))
        

# Create the main PyQt application object
application = PyQt5.QtWidgets.QApplication(sys.argv)

# Create a QScintila editor instance
editor = MyCommentingEditor()

# Show the editor
editor.show()
editor.resize(PyQt5.QtCore.QSize(800, 600))
# Put the text into the editing area of the editor
editor.setText(
"""\
#include <iostream>
using namespace std;

void Function0() {
    cout << "Function0";
}

void Function1() {
    cout << "Function1";
}

void Function2() {
    cout << "Function2";
}

void Function3() {
    cout << "Function3";
}


int main(void) {
    if (1) {
        if (1) {
            if (1) {
                if (1) {
                    int yay;
                }
            }
        }
    }

    if (1) {
        if (1) {
            if (1) {
                if (1) {
                    int yay2;
                }
            }
        }
    }

    return 0;
}\
"""
)

# Execute the application
application.exec_()
