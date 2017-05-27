
# Cython libraries
from libc.stdlib cimport malloc, free
from libc.string cimport strcmp, strstr, strlen, strcpy, strchr, strtok
from cpython.unicode cimport PyUnicode_AsEncodedString

cdef int my_ints[5]
print(my_ints)

"""
Common functions and variables
"""
# Separator list
cdef char* extended_separators = [
    ' ', '\t', '(', ')', '.', ';', 
    '+', '-', '/', '*', ':', ',', 
    '\n', '[', ']', '{', '}', '<', 
    '>', '|', '=', '@', '&', '%',
    '!', '?', '^', '~', '\"'
]

# Separator list length
cdef int separator_list_length = strlen(extended_separators)

cdef inline char** to_cstring_array(string_list):
    """C function that transforms a Python list into a C array of strings(char arrays)"""
    # Allocate the array of C strings on the heap
    cdef char **return_array = <char **>malloc(len(string_list) * sizeof(char *))
    # Loop through the python list of strings
    for i in range(len(string_list)):
        # Decode the python string to a byte array
        temp_value = PyUnicode_AsEncodedString(string_list[i], 'utf-8', "strict")
        # Allocate the current C string on the heap (+1 is for the termination character '\0')
        temp_str = <char*>malloc((len(temp_value) * sizeof(char)) + 1)
        # Copy the decoded string into the allocated C string
        strcpy(temp_str, temp_value)
        # Set the reference of the C string in the allocated array at the current index
        return_array[i] = temp_str
    return return_array

cdef inline free_cstring_array(char** cstring_array, int list_length):
    """
        C function for cleaning up a C array of characters:
            This function is not needed, but is included as an example of
            how to manually free memory after it is not needed anymore.
    """
    for i in range(list_length):
        free(cstring_array[i])
    free(cstring_array)

cdef inline char check_extended_separators(char character) nogil:
    cdef int cnt
    for cnt in range(0, separator_list_length):
        if character == extended_separators[cnt]:
            return character
    return 0


# Style C enumeration
cdef enum NimStyles:
    Default,
    Keyword,
    Unsafe,
    MultilineComment

# Keyword lists, these could have been imported from the cython_lexer.py module,
# but for completness they will be declared here also
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
# Keyword list length
cdef int keyword_list_length = len(keyword_list)
cdef int unsafe_keyword_list_length = len(unsafe_keyword_list)

"""
    Change python keyword lists into a C arrays:
        This is the first mayor optimization. Looping over and accessing 
        C arrays is much faster than with Python lists.
"""
cdef char** c_keyword_list = to_cstring_array(keyword_list)
cdef char** c_unsafe_keyword_list = to_cstring_array(unsafe_keyword_list)

def cython_style_text(int start, int end, lexer, editor):
    # Local variable definitions, notice the cdef keyword infront of them,
    # that declares them as C variables.
    cdef int    i = 0
    cdef char   commenting = 0
    cdef char*  c_text
    cdef int    text_length = 0
    cdef char   first_comment_pass = 0
    """
        Token arrays have to have the lenght of the maximum word
        of any in the document. Otherwise there will be an out of bounds assignment.
        The other way would be to dynamically allocate the array using malloc,
        if the size gets larger than the predefined one.
    """
    cdef char[255]  current_token
    cdef char[255]  previous_token
    cdef int        token_length = 0
    cdef int        temp_state = 0
    # Get the Python text as a string
    py_text     = editor.text()
    # Convert the python string into a C string
    c_text      = NULL
    py_text     = editor.text()
    text        = bytearray(py_text, "utf-8")[start:end]
    c_text      = text
    text_length = len(text)
    # Loop optimization, but it's still a pure python function, meaning quite slow
    setStyling  = lexer.setStyling
    # Initialize comment state and split the text into tokens
    commenting  = 0
    stringing   = 0
    # Initialize the styling
    lexer.startStyling(start)
    # Check if there is a style(comment, string, ...) stretching on from the previous line
    if start != 0:
        previous_style = editor.SendScintilla(editor.SCI_GETSTYLEAT, start - 1)
        if previous_style == MultilineComment:
            commenting = 1
    # When looping in Cython, it is advisable to use a C integer, as Cython
    # optimizes this into a C loop, which is much faster than a Python loop
    while i < text_length:
        # Check for a comment
        if ( ((c_text[i] == '#' and c_text[i+1] == '[') and commenting == 0) or
             commenting == 1 ):
            temp_state = i - temp_state
            #Style the currently accumulated token
            if temp_state > 0:
                current_token[token_length] = 0
                check_token(
                    current_token,
                    previous_token,
                    c_text[i],
                    temp_state,
                    setStyling
                )
            temp_state = i
            # Skip the already counted '[*' characters
            if commenting == 0:
                i += 2
            # Initialize the comment counting
            if first_comment_pass == 0:
                comment_count = 1
            first_comment_pass = 0
            # Loop until the comment ends
            while not(i >= text_length):
                # Count the comment beginnings/ends
                if c_text[i] == ']' and c_text[i+1] == '#':
                    i += 1
                    break
                else:
                    i += 1
            # Only style the '*]' characters if it's not the end of the text
            if i < text_length:
                i += 2
            # Style the comment
            temp_state = i - temp_state
            setStyling(temp_state, MultilineComment)
            temp_state = i
            # Reset the comment flag
            commenting = 0
            token_length = 0
            # Skip to the next iteration, because the index is already
            # at the position at the end of the '*]' characters
            continue
        elif check_extended_separators(c_text[i]) != 0:
            temp_state = i - temp_state
            # Style the currently accumulated token
            current_token[token_length] = 0
            if temp_state > 0:
                check_token(
                    current_token,
                    previous_token,
                    c_text[i],
                    temp_state,
                    setStyling
                )
            # Save the token
            strcpy(previous_token, current_token)
            # Update the temporary variables
            temp_state = i
            i += 1
            # Skip until the next non-whitespace character and style the 
            # accumulated token with the default style
            while c_text[i] == ' ' or c_text[i] == '\t':
                i += 1
            temp_state = i - temp_state
            setStyling(temp_state, Default)
            #Set the new index and reset the token lenght
            temp_state = i
            token_length = 0
            #Skip to the next iteration, because the index is already
            #at the position of the next separator
            continue
        elif i < text_length:
            current_token[token_length] = c_text[i]
            token_length += 1
            i += 1
            while (check_extended_separators(c_text[i]) == 0 and 
                   i < text_length):
                current_token[token_length] = c_text[i]
                token_length += 1
                i += 1
            #Correct the index one character back
            i -= 1
        
        #Increment the array index
        i += 1
        #Style the text at the end of the document if
        #the end has been reached
        if i >= text_length:
            temp_state = i - temp_state
            #Style the currently accumulated token
            current_token[token_length] = 0
            if temp_state > 0:
                check_token(
                    current_token,
                    previous_token,
                    c_text[i],
                    temp_state,
                    setStyling
                )

cdef inline void check_token(char*  current_token,
                             char*  previous_token,
                             char   current_character,
                             int    temp_state,
                             setStyling):
    """Check and style a token"""
    if check_keyword(current_token) == 1:
        # Keyword
        setStyling(temp_state, Keyword)
    elif check_unsafe_keyword(current_token) == 1:
        # Unsafe keyword
        setStyling(temp_state, Unsafe)
    else:
        setStyling(temp_state, Default)

cdef inline char check_keyword(char* token_string) nogil:
    """
        C function for checking if the token is a keyword.
        Notice that the function declaration has the 'inline' and 'nogil'
        optimizations added. 'inline' inlines the function directly at every
        address where it is called in the resulting compiled module. 'nogil'
        disables the Python GIL (Global-Interpreter-Lock) as it is not needed
        in this function as it uses only C code.
        Check the documentation for more details.
    """
    global keyword_list_length
    global c_keyword_list
    cdef int i
    for i in range(keyword_list_length):
        if strcmp(token_string, c_keyword_list[i]) == 0:
            #String token is a keyword
            return 1
    #Not a keyword
    return 0

cdef inline char check_unsafe_keyword(char* token_string) nogil:
    """
        C function for checking if the token is an unsafe keyword.
        Same as the above function 'check_keyword', check in it's comment
        for more details.
    """
    global unsafe_keyword_list_length
    global c_unsafe_keyword_list
    cdef int i
    for i in range(unsafe_keyword_list_length):
        if strcmp(token_string, c_unsafe_keyword_list[i]) == 0:
            #String token is a keyword
            return 1
    #Not a keyword
    return 0
    


