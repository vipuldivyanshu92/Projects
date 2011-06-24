# Create a dictionnary to associate a letter to the keypad
AlphaKeyCode = {
    'a' : '2',
    'b' : '2',
    'c' : '2',
    'd' : '3',
    'e' : '3',
    'f' : '3',
    'g' : '4',
    'h' : '4',
    'i' : '4',
    'j' : '5',
    'k' : '5',
    'l' : '5',
    'm' : '6',
    'n' : '6',
    'o' : '6',
    'p' : '7',
    'q' : '7',
    'r' : '7',
    's' : '7',
    't' : '8',
    'u' : '8',
    'v' : '8',
    'w' : '9',
    'x' : '9',
    'y' : '9',
    'z' : '9',
}

KeyCodeToAlpha = {
    '2' : ['a', 'b', 'c'],
    '3' : ['d', 'e', 'f'],
    '4' : ['g', 'h', 'i'],
    '5' : ['j', 'k', 'l'],
    '6' : ['m', 'n', 'o'],
    '7' : ['p', 'q', 'r', 's'],
    '8' : ['t', 'u', 'v'],
    '9' : ['w', 'x', 'y', 'z'],
}

# Create an empty dictionnary to store the database for words, the keys are the KeyCode representation
WordDataBase = {}

def AddEntry(word, coefficient):
    Code = WordToKeyCode(word)
    if WordDataBase.has_key(Code):
        WordDataBase[Code] += [[word, coefficient]] 
    else:
        WordDataBase[Code] = [[word, coefficient]]

def PopulateDB(filename):
    f_database = open(filename, 'r')
    line = f_database.readline()
    while line:
        if line[-1] == '\n':
            line = line[:-1]
        AddEntry(line, 0)
        line = f_database.readline()
    f_database.close()

def WordToKeyCode(s):
    result = ''
    for c in s:
        result += AlphaKeyCode.get(c, '')
    return result

def KeyCodeToWord(k):
    result = ''
    for d in k:
        result += KeyCodeToAlpha[d][0]
    return result

def ListToString(l):
    result = ''
    for i in l:
        result += i + ' '
    return result

def CoeffSort(key, pos):
    for i in range(len(WordDataBase[key])):
        if (WordDataBase[key][i][1] < WordDataBase[key][pos][1]) and (pos > i):
            temp = WordDataBase[key][pos]
            del WordDataBase[key][pos]
            WordDataBase[key].insert(i, temp)
            break

PopulateDB('short.txt')     # Populate the dictionnary
#print WordDataBase         # Debug output DO NOT PRINT WITH LONG.txt (or wait for consequesies ...)

selected_word = 0

sentence = []

keycode = ''
inp = raw_input()
while inp != '#':
    if inp in ['2', '3', '4', '5', '6', '7', '8', '9']:
        keycode += inp

    elif inp == '=':
        if selected_word == len(WordDataBase.get(keycode, [[KeyCodeToWord(keycode), 0]]))-1:    # Round when end of the list
            selected_word = 0
        else:
            selected_word += 1

    elif inp == ' ':
        # Validate the current word
        if keycode:
            sentence += [WordDataBase[keycode][selected_word][0]]
            WordDataBase[keycode][selected_word][1] += 1
            # Pos of the word id selected_word
            CoeffSort(keycode, selected_word)
            selected_word = 0
            keycode = ''

    elif inp == '+':
        word = raw_input()
        if keycode == WordToKeyCode(word):
            AddEntry(word, 1)
            # Pos of the word is -1
            CoeffSort(keycode, len(WordDataBase[keycode])-1)
            sentence += [word]
            keycode = ''
        else:
            print 'Incorrect input'

    elif inp == '-':
        if len(keycode) == 0 and len(sentence) > 0:
            keycode = WordToKeyCode(sentence[-1])
            del sentence[-1]
        elif len(keycode) > 0:
            keycode = keycode[:-1]
            selected_word = 0

    print ListToString(sentence)+WordDataBase.get(keycode, [[KeyCodeToWord(keycode), 0]])[selected_word][0]
    
    inp = raw_input()
