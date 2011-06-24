# -----------------------------------------------------------
# Pacman, grid based game

# JOUET Simon

# 21/01/08
# -----------------------------------------------------------

#-- Import of required librairies
import Tkinter
import threading
import time
import random
import os
import string

# -- Variables
map_folder = './maps/'
datas_folder = './datas/'
root = Tkinter.Tk()                     # Define root variable as a Tkinter entity
Active = True
canvas = None                           #
game_player = None                      #
game_map = None                         # Define this instance of different objects as non existant
game_MovementHandler = None             #
game_Input = None                       #
game_monsters = []
max_levels = 0                          # Maximum levels playable

# -- Classes
class MainMenu:
    menus_id = []
    menus_title = ["Start", "High Scores", "Credits"]
    selected = 1
    externalitems_id = []
    
    # - Called when up arrow is pressed
    def ChangeUp(self, evt):
        if self.selected > 1:
            self.selected -= 1               # Select the previous menu
            self.UpdateMenus(self.selected+1)

    # - Called when down arrow is pressed
    def ChangeDown(self, evt):
        if self.selected < 3:
            self.selected += 1               # Select the next menu
            self.UpdateMenus(self.selected-1)

    # - Called to enter in a menu
    def EnterMenu(self, evt=None):
        if self.selected == 1:
            global game_player, game_map, game_MovementHandler, game_monsters
            game_monsters = []
            canvas.destroy()                                                                # Destroy the previous canvas
            #print "start"                                                                  #debug
            game_player = Character()                                                       # Create an instance for a character
            game_map = Map()                                                                # Create an instance for a map
            game_map.LoadMap('%s%d.map' % (map_folder, game_player.currentmap))             # Load the map
            game_map.DrawMap()                                                              # Draw the map
            game_MovementHandler = PlayerMovementHandler()                                  # Create en instance of a Movement Handler
            game_MovementHandler.Start()                                                    # Start the Movement Handler
        elif self.selected == 2:
            #print "high scores"                     #debug
            #print top(LoadScores(), 5)              #debug
            self.DelMenus()
            self.UnBindKeys()
            self.externalitems_id += [canvas.create_text(294, 180, text="High Scores", fill="Yellow", font=("Courier New", 20))]
            self.externalitems_id += [canvas.create_line(140, 200, 448, 200, fill="Yellow")]
            scores = top(LoadScores(), 5)                                                   # Get the five best scores 
            scores += ["-------|------------|0"]*(5-len(scores))                            # Add dummy input if needed
            for i in range(len(scores)):
                single = string.split(scores[i], '|')
                self.externalitems_id += [canvas.create_text(180, 220+30*i, text=single[0], fill="Yellow", font=("Courier New", 15))]
                self.externalitems_id += [canvas.create_text(300, 220+30*i, text=single[1], fill="Yellow", font=("Courier New", 15))]
                self.externalitems_id += [canvas.create_text(420, 220+30*i, text=TimeConverter(int(single[2])), fill="Yellow", font=("Courier New", 15))]
                root.bind('<Return>', self.RemoveExternalItems)
        elif self.selected == 3:
            self.DelMenus()
            self.UnBindKeys()
            # Credits texts,
            self.externalitems_id += [canvas.create_text(350, 160, text="Coded by Simon JOUET", fill="Yellow", font=("Courier New", 15))]
            self.externalitems_id += [canvas.create_text(100, 230, text="- Features implented:", fill="Yellow", font=("Courier New", 10))]
            self.externalitems_id += [canvas.create_text(120, 250, text="- Movement manager", fill="Yellow", font=("Courier New", 10))]
            self.externalitems_id += [canvas.create_text(124, 270, text="- Collision Handler", fill="Yellow", font=("Courier New", 10))]
            self.externalitems_id += [canvas.create_text(120, 290, text="- Dynamic Map load", fill="Yellow", font=("Courier New", 10))]
            self.externalitems_id += [canvas.create_text(156, 310, text="- Dynamic Ennemies creation", fill="Yellow", font=("Courier New", 10))]
            self.externalitems_id += [canvas.create_text(156, 330, text="- Ennemies movement handler", fill="Yellow", font=("Courier New", 10))]
            self.externalitems_id += [canvas.create_line(300, 200, 300, 400, fill="Yellow")]
            self.externalitems_id += [canvas.create_text(380, 230, text="- Todo list:", fill="Yellow", font=("Courier New", 10))]
            self.externalitems_id += [canvas.create_text(440, 250, text="- Improve ennemies AI", fill="Yellow", font=("Courier New", 10))]
            self.externalitems_id += [canvas.create_text(464, 270, text="- Create queue of execution", fill="Yellow", font=("Courier New", 10))]
            self.externalitems_id += [canvas.create_text(460, 290, text="  to prevent deadlocks", fill="Yellow", font=("Courier New", 10))]
            self.externalitems_id += [canvas.create_text(436, 310, text="- Fix remaining bugs", fill="Yellow", font=("Courier New", 10))]
            root.bind('<Return>', self.RemoveExternalItems)
            
    # - Called to exit high scores menu
    def RemoveExternalItems(self, evt):
        for i in self.externalitems_id:
            canvas.delete(i)
        self.selected = 1
        self.BindKeys()
        self.InitMenus()

    # - Called to create the menus the first time
    def InitMenus(self):
        for m in range(len(self.menus_title)):
            if (len(self.menus_id) > 0):         # Put red only first the first item
                color = "Yellow"
            else:
                color = "Red"
            self.menus_id += [canvas.create_text(294, 250+50*m, text=self.menus_title[m], fill=color, font=("Courier New", 30))]
            
    # - Called to delete the menu
    def DelMenus(self):
        for m in range(len(self.menus_id)-1, -1, -1):
            canvas.delete(self.menus_id[m])
            del(self.menus_id[m])

    # - Called to update the colors
    def UpdateMenus(self, previous):
        for m in range(len(self.menus_title)):    
            if (self.menus_title[m] == self.menus_title[self.selected-1]):
                canvas.delete(self.menus_id[previous-1])             # Delete the previous red menu
                self.menus_id[previous-1] = canvas.create_text(294, 250+50*(previous-1), text=self.menus_title[previous-1], fill="Yellow", font=("Courier New", 30))
                canvas.delete(self.menus_id[m])                      # Delete the current yellow menu
                self.menus_id[m] = canvas.create_text(294, 250+50*m, text=self.menus_title[m], fill="Red", font=("Courier New", 30))

    # - Called to bind the keys
    def BindKeys(self):
        root.bind("<Up>", self.ChangeUp)             # Define Action when Up arrow is pressed
        root.bind("<Down>", self.ChangeDown)         # Define Action when Down arrow is pressed
        root.bind("<Return>", self.EnterMenu)        # Define Action return is pressed
        
    # - Called to unbind the keys
    def UnBindKeys(self):
        root.unbind("<Up>")             # Define Action when Up arrow is pressed
        root.unbind("<Down>")           # Define Action when Down arrow is pressed
        root.unbind("<Return>")         # Define Action return is pressed

    # - Called to create the menu
    def Create(self):
        global canvas
        self.menus_id = []
        self.selected = 1
        if canvas != None:
            canvas.destroy()       
        background_image = Tkinter.PhotoImage(file = "%s/menu.GIF" % (datas_folder))    # Read and create variable for the image
        canvas = Tkinter.Canvas(root, height=434, width=588)                            # Create the canvas
        canvas.pack()
        background_id = canvas.create_image(294, 217, image = background_image)         # Load the background
        self.InitMenus()                                                                # Init the menus titles
        self.BindKeys()
        root.mainloop()
        

    # - Called when the object is created
    def __init__(self, evt=None):
        self.Create()
        
class InputMenu:
    player_name = ""                        # Player name variable
    name_id = 0                             # Id of the text on the canvas
    AllowedChars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"         # Allowed input chars
    
    def __init__(self, prompt):
        global canvas
        if canvas != None:
            canvas.destroy()
        canvas = Tkinter.Canvas(root, height=200, width=500, background = "black")
        canvas.create_text(250, 50, text=prompt, fill="Red", font=("Courier New", 30))
        canvas.pack()
        self.BindKeys()
        root.mainloop()
    
    # - Update the name on the canvas
    def UpdateName(self):
        if self.name_id != 0:                # Destroy the previous only if the previous exist
            canvas.delete(self.name_id)
        self.name_id = canvas.create_text(250, 100, fill="Yellow", text=self.player_name, font=("Courier New", 20))
    
    # - Action when a key is pressed
    def InputAction(self, evt):
        global game_menu
        if (len(self.player_name) <= 12):                 # Max length of the name = 12
            if evt.keysym in (self.AllowedChars):         # Only if the char is allowed
                self.player_name += evt.char
            elif (evt.keysym == "space") and (len(self.player_name) > 0) and self.player_name[-1] != ' ':
                self.player_name += ' '
        if evt.keysym == "BackSpace":                     # Handle the backspace
            self.player_name = self.player_name[:-1]      # Copy the previous without the last char
        if (evt.keysym == "Return") and (len(self.player_name) > 0):
            self.UnbindKeys()                             # Delete char bindings
            SaveScore(str(game_player.score), self.player_name, "%s" % (str(int(time.time() - game_player.start))))
            game_menu = MainMenu()                        # Go back to the main menu
        self.UpdateName()                                 # Update the name
        #print evt.keysym                                 #debug
    
    # - Bind all AllowedKeys
    def BindKeys(self):
        for c in self.AllowedChars:
            root.bind("<%s>" % (c), self.InputAction)
        root.bind("<space>", self.InputAction)
        root.bind("<BackSpace>", self.InputAction)
        root.bind("<Return>", self.InputAction)
    
    # - Unbind all allowedKey
    def UnbindKeys(self):
        for c in self.AllowedChars:
            root.unbind("<%s>" % (c))
        root.unbind("Left")
        root.unbind("<space>")
        root.unbind("<BackSpace>")
        root.unbind("<Return>")


class Character:
    canvas_id = 0                       # Referer to the integer returned by Canvas
    pos_xy = [0, 0]                     # List of the x and y current position on the canvas
    direction = 0
    score = 0                           # Score of the character
    lives = 3                           # Remaining lives of the character
    immune = False                      # The character is invincible or not
    immune_timer = 0                    # Invicibility timer
    BonusCollected = 0
    angle = 0
    angle_start = [90, 0, 270, 180]     # Angle start of pacman mouth
    angle_extent = 359                  # Angle size
    angle_inc = -5                      # Incrementation of the angle
    color = "Yellow"                    # Pacaman color
    currentmap = 0                      # Current level of the game
    start = None

    # - Called when the character is created
    def __init__(self):
        self.start = time.time()

    # - Called to go to the next level or to the main menu
    def NextLevel(self, evt=None):
        if self.currentmap+1 < max_levels:
            self.currentmap += 1
            canvas.destroy()
            game_MovementHandler.direction = 0
            game_MovementHandler.buffer = 0
            game_map.LoadMap('%s%d.map' % (map_folder, game_player.currentmap))             # Load the new map
            game_map.DrawMap()                                                              # Draw the new map
            game_MovementHandler.Start()
        else:
            NameMenu()

    def Update(self):
        if self.immune:
            self.color = "Red"
        else:
            self.color = "Yellow"
        canvas.delete(self.canvas_id)              # Delete the previous instance of the character
        if self.angle in [0, 45]:                  # Reverse when 0 or 45 are reached
            self.angle_inc = -self.angle_inc
        self.angle += self.angle_inc               # Modify the mouth angle size
        #print self.angle                          # debug
        self.angle_extent = 360-2*(self.angle)     # The size of the extent is just a full circle -2*angle
        self.canvas_id = canvas.create_arc(self.pos_xy[0]+1, self.pos_xy[1]+1, self.pos_xy[0]+23, self.pos_xy[1]+23, start=self.angle_start[self.direction-1]+self.angle, extent=self.angle_extent-1, fill=self.color, outline="Yellow")
        
class Monster:
    canvas_id = 0                       # Referer to the integer returned by Canvas
    start_xy = [0, 0]                   # Define the beginning position of the monster, needed for respawn
    pos_xy = [0, 0]                     # Position on the canvas, here x and y represent center of the bitmap
    direction = 1
    monster_image = Tkinter.PhotoImage(file = "%s/red.gif" % (datas_folder))

    # Called when a monster is eat
    def Respawn(self):
        canvas.delete(self.canvas_id)
        self.pos_xy = self.start_xy
        self.Update()
    
    def Update(self):
        # If the absolute value of the difference of position is inferior to the tile size then we have a collision         
        if (abs(self.pos_xy[0]-game_player.pos_xy[0]) < 24) and (abs(self.pos_xy[1]-game_player.pos_xy[1]) < 24):
            #print "Game Over"                   # debug
            if game_player.lives > 0:
                if not game_player.immune:
                    game_player.lives -= 1       # If the character has still live just remove one
                    game_map.RemoveLife()
                else:
                    game_player.score += 200
                    game_map.UpdateScore()
                self.Respawn()
            else:
                game_map.GameOver("YOU LOST !")              # Else print game over
                root.bind("<Return>", NameMenu)
        else:
            canvas.delete(self.canvas_id)        # Delete previous instance
            self.canvas_id = canvas.create_image(self.pos_xy[0]+12, self.pos_xy[1]+12, image = self.monster_image)
            #self.canvas_id = canvas.create_oval(self.pos_xy[0], self.pos_xy[1], self.pos_xy[0]+24, self.pos_xy[1]+24, fill="Red")
        
    def EvtChangeCell(self, cpos):
        if random.randint(1, 8) == 1:             # Chance to happen
            self.direction = random.randint(1, 4)
    
    def MovementLoop(self):
        while Active:
            NextPositionValues = game_map.NextPosition(self.pos_xy, self.direction)
            #print self.direction            # debug
            #print NextPositionValues        # debug
            if (NextPositionValues[2] not in game_map.CollisionElements):
                self.pos_xy = NextPositionValues[:-1]
            else:
                self.direction = random.randint(1, 4)
                    
            # If the modulo is 0, so if we change to another cell                
            if (self.pos_xy[0] % 24 == 0) and (self.pos_xy[1] % 24 == 0):
                #print "Change cell"                        # debug
                self.EvtChangeCell(NextPositionValues)              
                
            self.Update()
            time.sleep(0.05)

    def Start(self):
        self.Handle = threading.Thread(target = self.MovementLoop)
        self.Handle.start()
        

class Map:   
    CollisionElements = ['1']         # A modifiable list where the character can't go
    BonusElements = ['E', 'F']        # A modifiable list where the "eatable" elements
    BonusPoints = [10, 100]           # Based on the previous one
    BonusNb = 0
    lives_id = []
    score_id = 0
    gameover_id = 0

    # - Called to load a map from fmap
    def LoadMap(self, fmap_name):
        # grid_map[n] represent the row n of the the grid, so the y coordinate
        # grid_map[n][m] represent the list of one cell
        # grid_map[n][m][0] represent the type of the cell
        # grid_map[n][m][1] represent the Tkinter canvas value
        
        fmap = open(fmap_name, 'r')         # Open the map in Read-Only
        rawmap = fmap.readlines()           # Load string from the map
        fmap.close()                        # Close the previous file
        self.width = len(rawmap[0])-1       # Do not count the cariage return 
        self.height = len(rawmap)
        self.grid_map = []
        for rows in rawmap:
            line = []                           # Clear the variable each time
            for cell in rows[0:self.width]:     # Need each cell
                line += [[cell, 0]]             # Create 2 elements list for each element
            self.grid_map += [line]             # Add the line to the map
            
    # - Called to update the score
    def UpdateScore(self):
        canvas.delete(self.score_id)
        self.score_id = canvas.create_text(260, (self.height)*24+30, text=str(game_player.score), fill='Blue', font=("Courier New", 30))

    # - Called to update player lives
    def RemoveLife(self):
        canvas.delete(self.lives_id[len(self.lives_id)-1])
        del(self.lives_id[len(self.lives_id)-1])

    # - Called to draw lives
    def DrawLives(self):
        pos_x = 500
        pos_y = (self.height)*24+15
        for i in range(game_player.lives):
            self.lives_id += [canvas.create_arc(pos_x, pos_y, pos_x+24, pos_y+24, start=45, extent=270, fill="Yellow", outline="Yellow")]
            pos_x += 35
        
    # - Called when the game is over
    def GameOver(self, msg):
        global Active
        Active = False
        self.gameover_id = canvas.create_text(self.width*12, self.height*12, text=msg, fill='Green', font=("", 50))
        
    # - Called to draw the map in a Canvas
    def DrawMap(self):
        global canvas, game_monsters, Active
        Active = True
        canvas = Tkinter.Canvas(root, height=self.height*24+50, width=self.width*24, background = "black") # Create the canvas with right size, add 50 pixel for the core board
        canvas.pack()                                        # Resize the window to the canas size
        canvas.create_text(100, (self.height)*24+30, text="Score :", fill='Blue', font=("Courier New", 30))
        canvas.create_text(400, (self.height)*24+30, text="Lives :", fill='Blue', font=("Courier New", 30))
        canvas.create_text(750, (self.height)*24+30, text="Level : %s" % (game_player.currentmap+1), fill='Blue', font=("Courier New", 30))
        self.DrawLives()
        self.score_id = canvas.create_text(260, (self.height)*24+30, text=game_player.score, fill='Blue', font=("Courier New", 30))
        for row in range(self.height):                    
            for column in range(self.width):              
                cell_type = self.grid_map[row][column][0]
                if cell_type == '0':
                    pass
                elif cell_type == '1':
                    self.grid_map[row][column][1] = canvas.create_rectangle(column*24, row*24, column*24+24, row*24+24, fill="#008AFF", outline="#00FFFF")
                elif cell_type == 'S':
                    game_player.pos_xy = [column*24, row*24] 
                    game_player.canvas_id = canvas.create_oval(column*24+1, row*24+1, column*24+23, row*24+23, fill="Yellow", outline="Yellow")
                elif cell_type == 'E':
                    self.grid_map[row][column][1] = canvas.create_oval(column*24+8, row*24+8, column*24+16, row*24+16, fill="orange")
                    self.BonusNb += 1
                elif cell_type == 'F':
                    self.grid_map[row][column][1] = canvas.create_oval(column*24+6, row*24+6, column*24+18, row*24+18, fill="red")
                    self.BonusNb += 1
                elif cell_type == 'M':
                    # Dynamic creation of the ennemies one object for each ennemy
                    game_monsters.append(Monster())
                    game_monsters[-1].start_xy = [column*24, row*24]
                    game_monsters[-1].pos_xy = game_monsters[-1].start_xy
                    game_monsters[-1].Update()
                    game_monsters[-1].Start()
                else:
                    pass
    
    # - Called to know the nest position with the current direction and the map type            
    def NextPosition(self, pos_xy, direction):
        #print pos_xy                            #debug
        #print game_map.width*24                 #debug
        #print game_map.height*24                #debug
                
        if ((pos_xy[0] <= 0) and (direction == 4)) or ((pos_xy[0] >= (game_map.width-1)*24) and (direction == 2)):        # Check if we are still in the map wrt to X axis
            if direction == 2:
                return [0, pos_xy[1], 0]                                    # Go to the left side of the map
            elif direction == 4:
                return [(game_map.width-1)*24, pos_xy[1], 0]                # Go to the right side
        elif ((pos_xy[1] <= 0) and (direction == 1)) or ((pos_xy[1] >= (game_map.height-1)*24) and (direction == 3)):     # Check if we are still in the map wrt to Y axis
            if direction == 1:
                return [pos_xy[0], (game_map.height-1)*24, 0]
            elif direction == 3:
                return [pos_xy[0], 0, 0]
        else:                                                               # If we are still in the map
            if direction == 1:
                return [pos_xy[0], pos_xy[1]-2, self.grid_map[(pos_xy[1]-2) / 24][pos_xy[0] / 24][0]]
            elif direction == 2:
                return [pos_xy[0]+2, pos_xy[1], self.grid_map[pos_xy[1] / 24][(pos_xy[0]+24) / 24][0]] 
            elif direction == 3:
                return [pos_xy[0], pos_xy[1]+2, self.grid_map[(pos_xy[1]+24) / 24][pos_xy[0] / 24][0]]            
            elif direction == 4:
                return [pos_xy[0]-2, pos_xy[1], self.grid_map[pos_xy[1] / 24][(pos_xy[0]-2) / 24][0]]
            else:
                return [pos_xy[0], pos_xy[1], 0]

    # - Called to remove one element from the Canvas    
    def DestroyElement(self, x, y):
        cell_x = x / 24
        cell_y = y / 24
        canvas.delete(self.grid_map[cell_y][cell_x][1])
        self.grid_map[cell_y][cell_x] = ['0', 0]
        
class PlayerMovementHandler:  
    buffer = 0            # Buffer is the next direction to take
    Keys = ['<Up>', '<Right>', '<Down>', '<Left>']
    
    # - Called when a key is pressed to change the direction variable  
    def ChangeUp(self, evt):
        self.buffer = 1
            
    def ChangeRight(self, evt):
        self.buffer = 2
            
    def ChangeDown(self, evt):
        self.buffer = 3
            
    def ChangeLeft(self, evt):
        self.buffer = 4
        
    # - Called if the Movement keys want to be reallocated by default it is the arrows
    def AssociateKeys(self, Keys):
        root.bind(Keys[0], self.ChangeUp)
        root.bind(Keys[1], self.ChangeRight)
        root.bind(Keys[2], self.ChangeDown)
        root.bind(Keys[3], self.ChangeLeft)
        root.unbind("<Return>")
        
    def EvtChangeCell(self, cpos):
        game_player.direction = self.buffer 
        #print "Change Cell"                 #debug
        if cpos[2] in game_map.BonusElements:
            #print "BONUS !"                 #debug
            if cpos[2] == 'F':               # If the character have eat a big thing
                game_player.immune_timer = 5
                game_player.immune = True
            game_player.score += game_map.BonusPoints[game_map.BonusElements.index(cpos[2])]
            #print game_player.score         #debug
            game_map.DestroyElement(cpos[0], cpos[1])
            game_map.UpdateScore()           # Update the score of the character 
            game_player.BonusCollected += 1
            if game_player.BonusCollected == game_map.BonusNb:
                game_map.GameOver("YOU WIN !")
                root.bind("<Return>", game_player.NextLevel)
            
    # - Main loop to edit if you want to create another grid-based game        
    def MovementLoop(self):
        while Active:
            #print game_player.direction     #debug
            #print game_player.pos_xy        #debug
                
            NextPositionValues = game_map.NextPosition(game_player.pos_xy, game_player.direction)
            #print NextPositionValues        #debug
            # Just start to update if the player have moved
            if (NextPositionValues[2] not in game_map.CollisionElements) and (game_player.direction != 0):
                game_player.pos_xy = NextPositionValues[:-1]            # Just get the X and y
                game_player.Update()                                    # Update the position of the current character 
                
            if (game_player.pos_xy[0] % 24 == 0) and (game_player.pos_xy[1] % 24 == 0):
                self.EvtChangeCell(NextPositionValues)

            if game_player.immune:
                game_player.immune_timer -= 0.015
                #print game_player.immune_timer         #debug
                if game_player.immune_timer <= 0:
                    game_player.immune = False
            time.sleep(0.015)
            
    
    # - Called to start the movement handler in a new thread
    def Start(self):
        self.AssociateKeys(self.Keys)
        self.Handle = threading.Thread(target = self.MovementLoop)     # Allocate the value of the thread id
        self.Handle.start()                                            # Start the thread   
        
               
# -- Functions
# - Called when program is closing
def callback():
    global Active
    Active = False
    root.destroy()

# - Called to evaluate the number of possible maps
def NumberOfMaps():
    global max_levels
    files = os.listdir(map_folder)
    for i in files:
        if os.path.isfile("""%s\%s""" % (map_folder, i)):
            if ".map" in i:
                max_levels += 1
                
# - Called to load the scores
def LoadScores():
    fscores = open("%s/scores" % (datas_folder), 'r')
    scores = fscores.readlines()
    fscores.close()
    return scores

# - Return the top n from a list
def top(l, n):
    l.sort()
    l.reverse()
    return l[0:n]

# - Save a score    
def SaveScore(score, name, t):
    if len(score) < 7:
        score = "%s%s" % ("0"*(7-len(score)), score)
    seq = LoadScores()
    fscores = open("%s/scores" % (datas_folder), 'w')
    leadingchar = ""
    if len(seq) > 0:
        leadingchar = "\n"
    seq.append("%s%s|%s|%s" % (leadingchar, score, name, t))
    fscores.writelines(seq)
    fscores.close()
    
# - Convert a time a second to xx"yy'
def TimeConverter(s):
    if s > 0:
        min = s / 60
        sec = s - min*60
        strmin = "%s" % ((2-len(str(min)))*"0"+str(min))
        strsec = "%s" % ((2-len(str(sec)))*"0"+str(sec))
        return "%s\"%s'" % (strmin, strsec)
    else:
        return "--\"--'"
    
def NameMenu(evt=None):
    global game_Input
    game_Input = InputMenu("Enter your name :")    

# -- Main loop
root.title("Pacman")
root.protocol("WM_DELETE_WINDOW", callback)         # Event called when the windows is closed to stop the thread
NumberOfMaps()
game_menu = MainMenu()
root.mainloop()
