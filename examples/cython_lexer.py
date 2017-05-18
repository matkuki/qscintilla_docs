    
# Import the PyQt5 module with some of the GUI widgets
import PyQt5.QtWidgets
# Import the QScintilla module
import PyQt5.Qsci
# Import Python's sys module needed to get the application arguments
import sys
import re

# Create a custom Nim lexer
class LexerNim(PyQt5.Qsci.QsciLexerCustom):
    styles = {
        "Default" : 0,
        "Keyword" : 1,
        "Unsafe" : 2,
        "MultilineComment" : 3,
    }
    keyword_list = [
        "block", "const", "export", "import", "include", "let", 
        "static", "type", "using", "var", "when", 
        "as", "atomic", "bind", "sizeof", 
        "break", "case", "continue", "converter",
        "discard", "distinct", "do", "echo", "elif", "else", "end",
        "except", "finally", "for", "from", "defined", 
        "if", "interface", "iterator", "macro", "method", "mixin", 
        "of", "out", "proc", "func", "raise", "ref", "result", 
        "return", "template", "try", "inc", "dec", "new", "quit", 
        "while", "with", "without", "yield", "true", "false", 
        "assert", "min", "max", "newseq", "len", "pred", "succ", 
        "contains", "cmp", "add", "del","deepcopy", "shallowcopy", 
        "abs", "clamp", "isnil", "open", "reopen", "close","readall", 
        "readfile", "writefile", "endoffile", "readline", "writeline",
    ]
    unsafe_keyword_list = [
        "asm", "addr", "cast", "ptr", "pointer", "alloc", "alloc0",
        "allocshared0", "dealloc", "realloc", "nil", "gc_ref", 
        "gc_unref", "copymem", "zeromem", "equalmem", "movemem", 
        "gc_disable", "gc_enable", 
    ]
    
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
                # Make keywords bold
                self.setFont(PyQt5.QtGui.QFont("Courier", 8, weight=PyQt5.QtGui.QFont.Black), i)
            else:
                self.setFont(PyQt5.QtGui.QFont("Courier", 8), i)
        # Set the Keywords style to be clickable with hotspots
        # using the scintilla low level messaging system
        parent.SendScintilla(
            PyQt5.Qsci.QsciScintillaBase.SCI_STYLESETHOTSPOT, 
            self.styles["Keyword"], 
            True
        )
        parent.SendScintilla(
            PyQt5.Qsci.QsciScintillaBase.SCI_SETHOTSPOTACTIVEFORE, 
            True, 
            PyQt5.QtGui.QColor(0x00, 0x7f, 0xff)
        )
        parent.SendScintilla(
            PyQt5.Qsci.QsciScintillaBase.SCI_SETHOTSPOTACTIVEUNDERLINE, True
        )
        # Define a hotspot click function
        def hotspot_click(position, modifiers):
            """
            Simple example for getting the clicked token
            """
            text = parent.text()
            delimiters = [
                '(', ')', '[', ']', '{', '}', ' ', '.', ',', ';', '-',
                '+', '=', '/', '*', '#'
            ]
            start = 0
            end = 0
            for i in range(position+1, len(text)):
                if text[i] in delimiters:
                    end = i
                    break
            for i in range(position,-1,-1):
                if text[i] in delimiters:
                    start = i
                    break
            clicked_token = text[start:end].strip()
            # Print the token and replace it with the string "CLICK"
            print("'" + clicked_token + "'")
            parent.setSelection(0, start+1, 0, end)
            parent.replaceSelectedText("CLICK")
        # Attach the hotspot click signal to a predefined function
        parent.SCN_HOTSPOTCLICK.connect(hotspot_click)
        
        # Check if the cython lexer is available
        try:
            import cython_module
            self.cython_module = cython_module
            self.cython_imported = True
            print("Cython module successfully imported.")
        except:
            self.cython_imported = False
            print("Failed importing the Cython module!")
    
    def init_colors(self):
        # Font color
        self.setColor(PyQt5.QtGui.QColor(0x00, 0x00, 0x00), self.styles["Default"])
        self.setColor(PyQt5.QtGui.QColor(0x00, 0x00, 0x7f), self.styles["Keyword"])
        self.setColor(PyQt5.QtGui.QColor(0x7f, 0x00, 0x00), self.styles["Unsafe"])
        self.setColor(PyQt5.QtGui.QColor(0x7f, 0x7f, 0x00), self.styles["MultilineComment"])
        # Paper color
        for i in range(len(self.styles)):
            self.setPaper(PyQt5.QtGui.QColor(0xff, 0xff, 0xff), i)
    
    def language(self):
        return "Nim"
    
    def description(self, style):
        if style < len(self.styles):
            description = "Custom lexer for the Nim programming languages"
        else:
            description = ""
        return description
    
    def styleText(self, start, end):
        if self.cython_imported == True:
            self.cython_module.cython_style_text(start, end, self, self.parent())
        else:
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
            text = bytearray(self.parent().text(), "utf-8")[start:end].decode("utf-8")
            tokens = [
                (token, len(bytearray(token, "utf-8"))) 
                    for token in splitter.findall(text)
            ]
            # Multiline styles
            multiline_comment_flag = False
            # Check previous style for a multiline style
            if start != 0:
                previous_style = editor.SendScintilla(editor.SCI_GETSTYLEAT, start - 1)
                if previous_style == self.styles["MultilineComment"]:
                    multiline_comment_flag = True
            # Style the text in a loop
            for i, token in enumerate(tokens):
                if multiline_comment_flag == False and token[0] == "#" and tokens[i+1][0] == "[":
                    # Start of a multiline comment
                    self.setStyling(token[1], self.styles["MultilineComment"])
                    # Set the multiline comment flag
                    multiline_comment_flag = True
                elif multiline_comment_flag == True:
                    # Multiline comment flag is set
                    self.setStyling(token[1], self.styles["MultilineComment"])
                    # Check if a multiline comment ends
                    if token[0] == "#" and tokens[i-1][0] == "]":
                        multiline_comment_flag = False
                elif token[0] in self.keyword_list:
                    # Keyword
                    self.setStyling(token[1], self.styles["Keyword"])
                elif token[0] in self.unsafe_keyword_list:
                    # Keyword
                    self.setStyling(token[1], self.styles["Unsafe"])
                else:
                    # Style with the default style
                    self.setStyling(token[1], self.styles["Default"])
    

# Create the main PyQt application object
application = PyQt5.QtWidgets.QApplication(sys.argv)

# Create a QScintila editor instance
editor = PyQt5.Qsci.QsciScintilla()
# Set the lexer to the custom Nim lexer
nim_lexer = LexerNim(editor)
editor.setLexer(nim_lexer)
# Set the initial text
initial_text = """
proc python_style_text*(self, args: PyObjectPtr): PyObjectPtr {.exportc, cdecl.} =
    var
        result_object: PyObjectPtr
        value_start, value_end: cint
        lexer, editor: PyObjectPtr
        parse_result: cint
    
    parse_result = argParseTuple(
        args, 
        "iiOO", 
        addr(value_start),
        addr(value_end),
        addr(lexer),
        addr(editor),
    )
    
    #[
	    if parse_result == 0:
		echo "Napaka v pretvarjanju argumentov v funkcijo!"        
		returnNone()
    ]#
    
    var
        text_method = objectGetAttr(editor, buildValue("s", cstring("text")))
        text_object = objectCallObject(text_method, tupleNew(0))
        string_object = unicodeAsEncodedString(text_object, "utf-8", nil)
        cstring_whole_text = bytesAsString(string_object)
        whole_text = $cstring_whole_text
        text = whole_text[int(value_start)..int(value_end-1)]
        text_length = len(text)
        current_token: string = ""
    # Prepare the objects that will be called as functions
    var
        start_styling_obj: PyObjectPtr
        start_args: PyObjectPtr
        set_styling_obj: PyObjectPtr
        set_args: PyObjectPtr
        send_scintilla_obj: PyObjectPtr
        send_args: PyObjectPtr
    start_styling_obj = objectGetAttr(lexer, buildValue("s", cstring("startStyling")))
    start_args = tupleNew(1)
    set_styling_obj = objectGetAttr(lexer, buildValue("s", cstring("setStyling")))
    set_args = tupleNew(2)
    send_scintilla_obj = objectGetAttr(editor, buildValue("s", cstring("SendScintilla")))
    send_args = tupleNew(2)
    
    # Template for final cleanup
    template clean_up() =
        xDecref(text_method)
        xDecref(text_object)
        xDecref(string_object)
        xDecref(args)
        xDecref(result_object)
        
        xDecref(start_styling_obj)
        xDecref(start_args)
        xDecref(set_styling_obj)
        xDecref(set_args)
        xDecref(send_scintilla_obj)
        xDecref(send_args)
    # Template for the lexers setStyling function
    template set_styling(length: int, style: int) =
        discard tupleSetItem(set_args, 0, buildValue("i", length))
        discard tupleSetItem(set_args, 1, buildValue("i", style))
        discard objectCallObject(set_styling_obj, set_args)
    # Procedure for getting previous style
    proc get_previous_style(): int =
        discard tupleSetItem(send_args, 0, buildValue("i", SCI_GETSTYLEAT))
        discard tupleSetItem(send_args, 1, buildValue("i", value_start - 1))
        result = longAsLong(objectCallObject(send_scintilla_obj, send_args))
        xDecref(send_args)
    # Template for starting styling
    template start_styling() =
        discard tupleSetItem(start_args, 0, buildValue("i", value_start))
        discard objectCallObject(start_styling_obj, start_args)
    # Safety
    if set_styling_obj == nil:
        raise newException(FieldError, "Lexer doesn't contain the 'setStyling' method!")
    elif start_styling_obj == nil:
        raise newException(FieldError, "Lexer doesn't contain the 'startStyling' method!")
    elif send_scintilla_obj == nil:
        raise newException(FieldError, "Editor doesn't contain the 'SendScintilla' method!")
    # Styling initialization
    start_styling()
    #------------------------------------------------------------------------------
    var 
        actseq = SeqActive(active: false)
        token_name: string = ""
        previous_token: string = ""
        token_start: int = 0
        token_length: int = 0
    # Check previous style
    if value_start != 0:
        var previous_style = get_previous_style()
        for i in multiline_sequence_list:
            if previous_style == i.style:
                actseq.sequence = i
                actseq.active = true
                break
    # Style the tokens accordingly
    proc check_start_sequence(pos: int, sequence: var SeqActive): bool =
        for s in sequence_lists:
            var found = true
            for i, ch in s.start.pairs:
                if text[pos+i] != ch:
                    found = false
                    break
            if found == false:
                continue
            sequence.sequence = s
            return true
        return false
    
    proc check_stop_sequence(pos: int, actseq: SeqActive): bool =
        if text[pos] in actseq.sequence.stop_extra:
            return true
        if pos > 0 and (text[pos-1] in actseq.sequence.negative_lookbehind):
            return false
        for i, s in actseq.sequence.stop.pairs:
            if text[pos+i] != s:
                return false
        return true
    
    template style_token(token_name: string, token_length: int) =
        if token_length > 0:
            if token_name in keywords:
                set_styling(token_length, styles["Keyword"])
                previous_token = token_name
            elif token_name in custom_keywords:
                set_styling(token_length, styles["CustomKeyword"])
            elif token_name[0].isdigit() or (token_name[0] == '.' and token_name[1].isdigit()):
                set_styling(token_length, styles["Number"])
            elif previous_token == "class":
                set_styling(token_length, styles["ClassName"])
                previous_token = ""
            elif previous_token == "def":
                set_styling(token_length, styles["FunctionMethodName"])
                previous_token = ""
            else:
                set_styling(token_length, styles["Default"])
    
    var i = 0
    token_start = i
    while i < text_length:
        if actseq.active == true or check_start_sequence(i, actseq) == true:
            #[
                Multiline sequence already started in the previous line or
                a start sequence was found
            ]#
            if actseq.active == false:
                # Style the currently accumulated token
                token_name = text[token_start..i]
                token_length = i - token_start
                style_token(token_name, token_length)
            # Set the states and reset the flags
            token_start = i
            token_length = 0
            if actseq.active == false:
                i += len(actseq.sequence.start)
            while i < text_length:
                # Check for end of comment
                if check_stop_sequence(i, actseq) == true:
                    i += len(actseq.sequence.stop)
                    break
                i += 1
            # Style text
            token_length = i - token_start
            set_styling(token_length, actseq.sequence.style)
            # Style the separator tokens after the sequence, if any
            token_start = i
            while text[i] in extended_separators and i < text_length:
                i += 1
            token_length = i - token_start
            if token_length > 0:
                set_styling(token_length, styles["Default"])
            # Set the states and reset the flags
            token_start = i
            token_length = 0
            # Skip to the next iteration, because the index is already
            # at the position at the end of the string
            actseq.active = false
            continue
        elif text[i] in extended_separators:
            #[
                Separator found
            ]#
            token_name = text[token_start..i-1]
            token_length = len(token_name)
            if token_length > 0:
                style_token(token_name, token_length)
                token_start = i
                while text[i] in extended_separators and i < text_length:
                    i += 1
                token_length = i - token_start
                if token_length > 0:
                    set_styling(token_length, styles["Default"])
                # State reset
                token_start = i
                token_length = 0
                continue
            else:
                while text[i] in extended_separators and i < text_length:
                    i += 1
                token_length = i - token_start
                if token_length > 0:
                    set_styling(token_length, styles["Default"])
                # State reset
                token_start = i
                token_length = 0
                continue
        # Update loop variables
        inc(i)
        # Check for end of text
        if i == text_length:
            token_name = text[token_start..i-1]
            token_length = len(token_name)
            style_token(token_name, token_length)
        elif i > text_length:
            raise newException(IndexError, "Styling went over the text length limit!")
    #------------------------------------------------------------------------------
    clean_up()
    returnNone()
"""
# Set the editor's text to something huge
editor.setText(100 * initial_text)


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
