    
# Import the PyQt5 module with some of the GUI widgets
import PyQt5.QtWidgets
# Import the QScintilla module
import PyQt5.Qsci
# Import Python's sys module needed to get the application arguments
import sys
import re

# Create a custom Nim lexer
class LexerC(PyQt5.Qsci.QsciLexerCustom):
    styles = {
        "Default" : 0,
        "Keyword" : 1,
        "String" : 2,
        "Comment" : 3,
        "MutilineComment" : 4,
    }
    keyword_list = [
        "auto", "break", "case", "char", "const",
        "continue", "default", "do", "double", "else",
        "enum", "extern", "float", "for", "goto",
        "if", "int", "long", "register", "return",
        "short", "signed", "sizeof", "static", "struct",
        "switch", "typedef", "union", "unsigned", "void",
        "volatile", "while",
    ]
    flags = {
        "String": False,
        "Comment": False,
        "MutilineComment": False,
    }
    
    def __init__(self, parent=None):
        # Initialize superclass
        super().__init__(parent)
        # Set the default style values
        self.setDefaultColor(PyQt5.QtGui.QColor(0x00, 0x00, 0x00))
        self.setDefaultPaper(PyQt5.QtGui.QColor(0xff, 0xff, 0xff))
        self.setDefaultFont(PyQt5.QtGui.QFont("Courier", 8))
        # Initialize all style colors
        self.init_colors()
        # Init the fonts
        for i in range(len(self.styles)):
            if i == self.styles["Keyword"]:
                self.setFont(PyQt5.QtGui.QFont("Courier", 8, weight=PyQt5.QtGui.QFont.Black), i)
            else:
                self.setFont(PyQt5.QtGui.QFont("Courier", 8), i)
    
    def init_colors(self):
        # Font color
        self.setColor(PyQt5.QtGui.QColor(0x00, 0x00, 0x00), self.styles["Default"])
        self.setColor(PyQt5.QtGui.QColor(0x00, 0x00, 0x7f), self.styles["Keyword"])
        self.setColor(PyQt5.QtGui.QColor(0x7f, 0x00, 0x7f), self.styles["String"])
        self.setColor(PyQt5.QtGui.QColor(0x00, 0x7f, 0x00), self.styles["Comment"])
        self.setColor(PyQt5.QtGui.QColor(0x00, 0xff, 0x00), self.styles["MutilineComment"])
        # Paper color
        for i in range(len(self.styles)):
            self.setPaper(PyQt5.QtGui.QColor(0xff, 0xff, 0xff), i)
    
    def language(self):
        return "C"
    
    def description(self, style):
        if style < len(self.styles):
            description = "Custom lexer for the C programming language"
        else:
            description = ""
        return description
    
    def styleText(self, start, end):
        for k in self.flags.keys():
            self.flags[k] = False
        # Initialize the styling
        self.startStyling(start)
        # Tokenize the text that needs to be styled using regular expressions.
        # To style a sequence of characters you need to know the length of the sequence
        # and which style you wish to apply to the sequence. It is up to the implementer
        # to figure out which style the sequence belongs to. 
        # THE PROCEDURE SHOWN BELOW IS JUST ONE OF MANY!
        splitter = re.compile(r"(\{\.|\.\}|\#|\'|\"\"\"|\n|\s+|\w+|\W)")
        # Scintilla works with bytes, so we have to adjust the start and end boundaries.
        # Like all Qt objects the lexers parent is the QScintilla editor.
        text = self.parent().text()[start:end]
        tokens = [(token, len(bytearray(token, "utf-8"))) for token in splitter.findall(text)]
        # Check if there is a style(comment, string, ...) stretching on from the previous line
        editor = self.parent()
        if start != 0:
            previous_style = editor.SendScintilla(editor.SCI_GETSTYLEAT, start - 1)
            if previous_style == self.styles["MutilineComment"]:
                self.flags["MutilineComment"] = True
        # Initialize token variables
        previous_token_text = ""
        token_text = ""
        next_token_text = ""
        # Style the text in a loop
        for i, token in enumerate(tokens):
            # Save previous token
            if token_text != "":
                previous_token_text = token_text
            # Set the current and next token information
            token_text = token[0]
            next_token_text = ""
            if len(tokens) > i+1:
                next_token_text = tokens[i+1][0]
            token_length = token[1]
            
            ## Token sequence styling
            # String
            if self.flags["String"] == True:
                self.setStyling(token_length, self.styles["String"])
                if "\"" in token_text or "\n" in token_text:
                    self.flags["String"] = False
                continue
            else:
                if "\"" in token_text:
                    self.setStyling(token_length, self.styles["String"])
                    self.flags["String"] = True
                    continue
            # Comment
            if self.flags["Comment"] == True:
                self.setStyling(token_length, self.styles["Comment"])
                if "\n" in token_text:
                    self.flags["Comment"] = False
                continue
            else:
                if token_text == "/" and next_token_text == "/":
                    self.setStyling(token_length, self.styles["Comment"])
                    self.flags["Comment"] = True
                    continue
            # Multiline comment
            if self.flags["MutilineComment"] == True:
                self.setStyling(token_length, self.styles["MutilineComment"])
                if previous_token_text.strip() == "*" and token_text.strip() == "/":
                    self.flags["MutilineComment"] = False
                continue
            else:
                if token_text == "/" and next_token_text == "*":
                    self.setStyling(token_length, self.styles["MutilineComment"])
                    self.flags["MutilineComment"] = True
                    continue
            
            ## Sprecial token styling
            if token_text in self.keyword_list:
                # Keyword
                self.setStyling(token_length, self.styles["Keyword"])
            else:
                # Style with the default style
                self.setStyling(token_length, self.styles["Default"])
        
        
        # Folding
        lines = self.parent().text().splitlines()
        # Initialize the folding variables
        fold_level = 0
        folding = False
        # Folding loop
        for line_number, line in enumerate(lines):
            # Add folding points as needed
            open_count = line.count('{')
            close_count = line.count('}')
            if close_count > 0:
                # Set the line's folding level first, so that the closing curly brace is added to the fold
                editor.SendScintilla(PyQt5.Qsci.QsciScintilla.SCI_SETFOLDLEVEL, line_number, fold_level | PyQt5.Qsci.QsciScintilla.SC_FOLDLEVELHEADERFLAG)
                # Adjust the folding level
                fold_level += open_count
                fold_level -= close_count
            else:
                # Adjust the folding level first
                fold_level += open_count
                fold_level -= close_count
                if fold_level <= 0:
                    fold_level = 0
                # Set the line's adjusted folding level
                editor.SendScintilla(PyQt5.Qsci.QsciScintilla.SCI_SETFOLDLEVEL, line_number, fold_level | PyQt5.Qsci.QsciScintilla.SC_FOLDLEVELHEADERFLAG)
            print(fold_level)
        # Reset the fold level of the last line
        editor.SendScintilla(PyQt5.Qsci.QsciScintilla.SCI_SETFOLDLEVEL, len(lines), 0)
        

# Create the main PyQt application object
application = PyQt5.QtWidgets.QApplication(sys.argv)

# Create a QScintila editor instance
editor = PyQt5.Qsci.QsciScintilla()
# Set the End-Of-Line character to Unix style ('\n')
editor.setEolMode(PyQt5.Qsci.QsciScintilla.EolUnix)
# Set the folding style, margin 2 is the default margin for displayingfolding
editor.setFolding(PyQt5.Qsci.QsciScintilla.PlainFoldStyle, 2)
# Set the lexer to the custom Nim lexer
nim_lexer = LexerC(editor)
editor.setLexer(nim_lexer)
# Set the initial text
editor.setText(
"""
int global = 0;

// Main function
int main()
{
    if (global == 0)
    {
        // Branch 0
        printf("Executed branch 0");
    }
    else
    {
        // Branch 1
        printf("Executed branch 1");
    }

    /*
        End
    */
    end_function();
}

void end_function(void)
{
    printf("End of program.");
}
"""
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
