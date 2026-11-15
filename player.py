import pygame #Imports pygame library

#Physics
Gravity = 1
jumpPower = -18

class Player:
    def __init__(self, x, y, animations): #Constructor

        #Sprites
        self.animations = {} #Sprite sheet for state
        for stateName, sprites in animations.items(): #Takes the name of the state as well as the sprite sheet for all sprite sheets and frame count
            sheet = sprites["sheet"] #Sprite Sheet
            frames = sprites["frames"] #Number of frames
            self.animations[stateName] = self.cut_sprite(sheet, frames) #Splits sprite sheet correspondingly
        self.state = "Idle" #State of player
        self.current_sprite = 0 #Tracks the current frame of sprite animation
        self.image = self.animations[self.state][0] #Sets the initial frame to first sprite image
        self.direction = 1 #Facing direction (1 = right, -1 = left)

        self.vely = 0 #Initalise y velocity 
        self.velx = 0 #Initliase x velocity
        self.acceleration = 0.7 #Player velx acceleration speed
        self.sliding = False #Initliase boolean to toggle player sliding
        self.SlideSide = "" #Determines player slide side
        self.friction = 0.4 #Player velx stopping speed
        self.max_velx = 5
        self.onground = False #Initliase boolean to check if player is on ground
        self.rect = self.image.get_rect() #Gets the hitbox from the player image
        self.rect.x = x # X position
        self.rect.y = y # Y position

        #Jump logic
        self.wallJumpBoost = False #Boolean to toggle wall jump velx speed lock
        self.maxJumps = 2 #Maximum amount of times allowed to jump in air
        self.JumpCounter = 0 #Keeps track of current jumps made before touching ground

    #Split sprite sheet into individual frames
    def cut_sprite(self, sheet, frame_count):
        sprite_frames = [] #List to hold sprite images separated
        sheet_split = sheet.get_width() // frame_count #The horizontal dimensions are divided by the amount of images in a sheet
        sheet_height = sheet.get_height() #The vertical dimension of the sprite sheet

        for i in range(frame_count): #Iterate through number of images in sprite sheet
            frame = sheet.subsurface(pygame.Rect(i * sheet_split, 0, sheet_split, sheet_height)).copy() #Creates rect of copied frame to save as separate image
            frame = pygame.transform.scale(frame, (65, 74)) #Scales the image to appropriate size
            sprite_frames.append(frame) #Add current i frame to list

        return sprite_frames #Returns list of frames
    
    def update_animation(self):
        frames = self.animations[self.state] #Play corresponding sprite sheet

        self.image = frames[int(self.current_sprite)] #Set current image to current frame animation
        self.current_sprite += 0.3 #Increment sprite frame ever 3 loops

        if self.current_sprite >= len(frames): #Reset animation
            self.current_sprite = 0

        if self.direction == -1:  #Flip image if going left
            self.image = pygame.transform.flip(self.image, True, False)

    def updateState(self):
        
        if self.onground == False: #State when in air
            if self.state != "jump":
                self.state = "jump"
                self.current_sprite = 0 #Reset sprite count

        else:
            if abs(self.velx) > 0.5: #State if moving
                if self.state != "run":
                    self.state = "run"
                    self.current_sprite = 0 #Reset sprite count
            else:
                if self.state != "Idle": #State if not moving and on ground
                    self.state = "Idle"
                    self.current_sprite = 0 #Reset sprite count

    #Jump procedure
    def jump(self):
        if self.onground:  #Checks if player is on the ground to allow jumping
            self.vely = jumpPower
            self.onground = False
            self.JumpCounter += 1 #Increments jump counter
        
        #If player is in air
        elif self.JumpCounter < self.maxJumps: #Checks if current jumps made are less than the max
            self.vely = jumpPower #Set jump velocity
            self.JumpCounter += 1 #Increment jump counter

    #Platform collision
    def CheckVerticalCollision(self, platforms): 

        self.onground = False

        for platform in platforms: #Iterates through all platforms
            if self.rect.colliderect(platform.rect): #Checks for player rect overriding platform rect
                if self.vely > 0: #When player is falling
                    if self.rect.bottom <= platform.rect.top + self.vely: #Checks top platform collision
                        self.rect.bottom = platform.rect.top #Sets players pos above platform
                        self.onground = True 
                        self.vely = 0
                        self.JumpCounter = 0 #Resets jumps
                    
                elif self.vely < 0: #When player is going up
                    if self.rect.top >= platform.rect.bottom + self.vely: #Checks bottom platform collision
                        self.rect.top = platform.rect.bottom #Sets players pos below platform 
                        self.vely = 0 #Stops player from moving

    def CheckHorizontalCollision(self, platforms):
        self.sliding = False
        for platform in platforms: #Iterates through all platforms
            if self.rect.colliderect(platform.rect): #Check for collision between player and platform

                if self.velx > 0: #Left wall collision
                    self.rect.right = platform.rect.left 
                    self.velx = 0 #Stop player movement
                    self.sliding = True #Enable sliding state
                    self.SlideSide = "Left"
                    break #Stop check if collision found
 
                elif self.velx < 0: #Right wall collision
                    self.rect.left = platform.rect.right 
                    self.velx = 0 #Stop player movement
                    self.sliding = True #Enable sliding state
                    self.SlideSide = "Right"
                    break #Stop check if collision found

            else:
                self.sliding = False

    def update(self, floor_y, platforms):
        self.onground = False #Assumed not on ground unless proven wrong

        keys = pygame.key.get_pressed() #Make key library

        #Horizontal movement
        if not self.sliding: #Unlocks movement if not sliding
            if keys[pygame.K_a]: #Left
                self.velx -= self.acceleration
                self.direction = -1 #Change direction left
            elif keys[pygame.K_d]: #Right
                self.velx += self.acceleration
                self.direction = 1 #Change direction right
            else: #To slow down player
                if not self.wallJumpBoost:
                    if self.velx > 0: #Right
                        self.velx -= self.friction
                    elif self.velx < 0: #Left
                        self.velx += self.friction

        #Set max speeds
        if self.velx > self.max_velx:
            self.velx = self.max_velx
        if self.velx < -self.max_velx:
            self.velx = -self.max_velx

        #Updates velx position constantly
        self.rect.x += self.velx
        self.CheckHorizontalCollision(platforms) #Checks for horizontal collision

        #While sliding
        if self.sliding == True: 
            self.vely = 0.1 #Slide speed
            if self.SlideSide == "Left":
                self.velx = 1
                self.direction = -1 #Change direction left
            else:
                self.velx = -1
                self.direction = 1 #Change direction right

        if not self.onground:
            self.vely += Gravity #Constantly apply gravity constant to vely

        #Updates vely position constantly
        self.rect.y += self.vely
        self.CheckVerticalCollision(platforms) #Checks for vertical collision

        #Floor collision
        if self.rect.bottom >= floor_y: #Above the floor ground
            self.rect.bottom = floor_y #Set to floor ground level
            self.vely = 0 #Speed set to 0
            self.onground = True 
            self.JumpCounter = 0 #Resets jumps
        
        #Toggle friction back on
        if self.onground:
            self.wallJumpBoost = False

        if not self.onground and self.JumpCounter == 0: #Checks if player walks off platform
            self.JumpCounter = 1
        
        self.updateState() 
        self.update_animation()

    def slideJump(self): #Procedure to jump while on wall
        if self.sliding: #Checks player is on wall
            self.vely = jumpPower * 0.9 #Applies negative y velocity 
            if self.SlideSide == "Left": #Checks for side to apply x velocity
                self.velx = -5
            else:
                self.velx = 5
            
            self.wallJumpBoost = True #Enables velx velocity lock
            self.sliding = False #Resets sliding to false after jumping
        
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 1) #(Surface, Colour, Rect, Width) Draws player border
        screen.blit(self.image, self.rect)
