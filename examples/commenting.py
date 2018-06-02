
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
similar to what SublimeText3 does
"""
class MyCommentingEditor(PyQt5.Qsci.QsciScintilla):
    comment_string = "// "
    line_ending = "\n"
    
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
        # Check if the selections are valid
        selections = self.get_selections()
        if selections == None:
            return
        # Start the undo action that can undo all commenting at once
        self.beginUndoAction()
        # Loop over selections and comment them
        for i, sel in enumerate(selections):
            self._comment_selection(sel[0], sel[1])
        # Select back the previously selected regions
        self.SendScintilla(self.SCI_CLEARSELECTIONS)
        for i, sel in enumerate(selections):
            start_index = self.positionFromLineIndex(sel[0], 0)
            end_index = self.positionFromLineIndex(sel[1], len(self.text(sel[1]))-1)
            if i == 0:
                self.SendScintilla(self.SCI_SETSELECTION, start_index, end_index)
            else:
                self.SendScintilla(self.SCI_ADDSELECTION, start_index, end_index)
        self.endUndoAction()
    
    def get_selections(self):
        # Get the selection and store them in a list
        selections = []
        for i in range(self.SendScintilla(self.SCI_GETSELECTIONS)):
            selection = (
                self.SendScintilla(self.SCI_GETSELECTIONNSTART, i),
                self.SendScintilla(self.SCI_GETSELECTIONNEND, i)
            )
            # Add selection to list
            from_line, from_index = self.lineIndexFromPosition(selection[0])
            to_line, to_index = self.lineIndexFromPosition(selection[1])
            selections.append((from_line, to_line))
        selections.sort()
        # Check if there are selections or not
        if len(selections) == 1 and selections[0][0] == selections[0][1]:
            return None
        # Return selection list
        return selections
    
    def _comment_selection(self, arg_from_line, arg_to_line):
        # Get the cursor information
        from_line = arg_from_line
        to_line = arg_to_line
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
#            selected_list[i] = line[:indent_index] + self.comment_string + line[indent_index:]
            selected_list[i] = self.comment_string + line
        # Replace the whole selected text with the merged lines
        # containing the commenting characters
        replace_text = self.line_ending.join(selected_list)
        self.replaceSelectedText(replace_text)

        

# Create the main PyQt application object
application = PyQt5.QtWidgets.QApplication(sys.argv)

# Create a QScintila editor instance
editor = MyCommentingEditor()
editor.SendScintilla(editor.SCI_SETMULTIPLESELECTION, 1)
editor.SendScintilla(editor.SCI_SETADDITIONALSELECTIONTYPING, True)

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
