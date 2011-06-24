# Declarations
import Canvas
import string

# Variables
InCall = 'Main'
cursor_pos = (0, 0)

# Remove the char return if necessary
def trim(s):
    if s[-1] == '\n':
        return s[:-1]
    else:
        return s
    
# Built-in Commands :
# line
# circle
# position
# move
# define
# end

def C_line(args):
    global cursor_pos 
    nextposition = (cursor_pos[0]+int(args[0]), cursor_pos[1]+int(args[1]))
    Canvas.create_line(cursor_pos[0], cursor_pos[1], nextposition[0], nextposition[1])
    cursor_pos = nextposition

def C_circle(args):
    Canvas.create_oval(cursor_pos[0]-int(args[0]), cursor_pos[1]-int(args[0]), cursor_pos[0]+int(args[0]), cursor_pos[1]+int(args[0]))

def C_position(args):
    global cursor_pos
    cursor_pos = (int(args[0]), int(args[1]))

def C_move(args):
    global cursor_pos
    nextposition = (cursor_pos[0]+int(args[0]), cursor_pos[1]+int(args[1]))
    cursor_pos = nextposition

def C_define(args):
    global InCall
    Functions[args[0]] = []
    InCall = args[0]

def C_end(args):
    pass

def Execute(l):
    for cmd in l:
        chop = string.split(cmd, ' ')
        print chop[0]
        if Commands.has_key(chop[0]):
            print 'This is a built-in command'
            Commands[chop[0]](chop[1:])
        elif Functions.has_key(chop[0]):
            print 'This is a user-defined function'
            Execute(Functions[chop[0]])
        else:
            print 'Unknown command : %s' % (chop[0])
        print

Commands = {
    'line'      : C_line,
    'circle'    : C_circle,
    'position'  : C_position,
    'move'      : C_move,
    'define'    : C_define,
    'end'       : C_end
}

Functions = {
}

file = open('test2.txt', 'r')

for line in file:
    line = string.lower(trim(line))
    if line == 'end':
        InCall = 'Main' 
    if InCall == 'Main':
        Execute([line])
    else:
        Functions[InCall] += [line]

file.close()

Canvas.complete()
