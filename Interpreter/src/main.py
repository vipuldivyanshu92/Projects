import Canvas
import string

# Possible commands
# position
# line
# move
# circle

# --- Definition of the variables ---
cpos = (0, 0)                                   # Position of the cursor on the canvas, by default 0 0
line = 0                                        # Current line number
dInProgress = False
dName = ''

# --- Definition of the functions ---
def Cposition(args):                                                # Command called when position is called
    global cpos
    print 'changing position to : %d, %d' % (args[0], args[1])      #debug
    cpos = (int(args[0]), int(args[1]))                             # Change the cpos variable

def Cline(args):                                                    # Command called when line is called
    next_pos = [cpos[0]+args[0], cpos[1]+args[1]]                   # Evalutate next position
    print 'draw a line from : %d, %d to : %d, %d' % (cpos[0], cpos[1], next_pos[0], next_pos[1])
    Canvas.create_line(cpos[0], cpos[1], next_pos[0], next_pos[1])  # Draw the line on the canvas
    Cposition(next_pos)                                             # Change the cursor position

def Cmove(args):                                                    # Command called when move is called
    next_pos = [cpos[0]+args[0], cpos[1]+args[1]]                   # Evalutate next position
    print 'move the cursor from : %d, %d to : %d, %d' % (cpos[0], cpos[1], next_pos[0], next_pos[1])
    Cposition(next_pos)                                             # Change the cursor position    
    
def Ccircle(args):                                                  # Command called when circle is called
    print 'draw a circle with radius %d' % (args[0])                #debug
    # If the cursor is the centre then to draw it we need to find
    # the corners of the containg box, so just remove/add the radius
    # to the x and y axis
    Canvas.create_oval(cpos[0]-args[0], cpos[1]-args[0], cpos[0]+args[0], cpos[1]+args[0])

def Cdefine(args):                                           # Command called when define is called
    print 'define a new function : %s' % (args[0])
    CmdBook[args[0]] = [Execute]
    print CmdBook

def Cend(args):                                              # End of definition
    pass

def CnonExisting(args):                                      # Command called when the command called is non existent
    raise 'ECmdInvalid', 'Invalid command %s' % (args[0])    # Raise an exception if the command doesn't exist

def ChkArgs(args, types):                                    # Check the arguments
    if len(args) != len(types):                              # Check if the number of arguments is right, remove one to remove it's name
        raise 'EArgsInvalid', 'Arguments number mismatch'    # Raise an exception if false
    for i in range(len(args)):                               # for each item       
        try:
            args[i] = types[i](args[i])                      # Convert to the required format
        except:
            raise 'EArgsInvalid', 'Argument type mismatch'   # Raise an error if the value is wrong
    return args

# Definition of the book of commands
# List definition
# [0] : Function name
# [1] : Parameters type
CmdBook = {
    'position' : [Cposition, [int, int]],
    'line'     : [Cline, [int, int]],
    'move'     : [Cmove, [int, int]],
    'circle'   : [Ccircle, [int]],
    'define'   : [Cdefine, [str]],
    'end'      : [Cend, []] 
}

# Definition of the callstack
#CallStack = {
#    #func_name : [commands inside this function]
#}

f = open('test2.txt', 'r')

def Execute(l):                       # Get a list of string to execute
    chop = string.split(l, ' ')       # Return a list
    func = CmdBook.get(chop[0], False)
    if func:
        func[0](ChkArgs(chop[1:], func[1]))
    else:
        CnonExisting([chop[0]])
    
for s in f:
    print '[%d]%s' % (len(s), s)
    if s != '':          # if this is not an empty line
        Execute(s[:-1])
        
f.close()

Canvas.complete()
