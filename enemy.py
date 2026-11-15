import pygame
import math #Math library for advanced math 
import random #Library for random

class Enemy:
    def __init__(self, x, y, animations): #Constructor (attributes)
        self.animations = {} #Sprite sheet for state
        for state_name, sprites in animations.items(): #Takes the name of the state as well as the sprite sheet for all sprite sheets and frame count
            sheet = sprites["sheet"] #Sprite Sheet
            frames = sprites["frames"] #Number of frames
            self.animations[state_name] = self.cut_sprite(sheet, frames) #Splits sprite sheet correspondingly

        self.patrol_min = x - 100 #Sets left border for enemy 
        self.patrol_max = x + 100 #Sets right border for enemy
        self.patrol_timer = 0 #Tracks how long one patrol track has been playing
        self.state = "Run" #State of enemy
        self.image = self.animations[self.state][0] #Sets the initial frame to first sprite image
        self.rect = self.image.get_rect() #Hitbox of enemy
        self.current_sprite = 0 #Tracks the current frame of sprite animation

        self.rect.x = x #X pos
        self.rect.y = y #Y pos
        self.direction = 1 #Facing direction of enemy
        self.vision_distance = 200 #Maximum vision distance
        self.vision_angle = 90 #Maximum vision angle
        self.velx = 1.5 #Velocity of enemy
        self.vely = 0 #Velocity of enemy 
        self.onground = False #Checks for gravity application
        self.gravity = 1 #Gravity constant 
        self.chase_speed = 3 #Enemy speed when chasing
        self.jump_power = -18 #Jump strength
        self.jump_cooldown = 0 #Adds debounce between jumps

        #Vision 
        self.vision_range = 200  #How far enemy can see
        self.vision_angle = 60  #Vision cone angle
        self.chase_range = 300  #Max distance enemy can chase player
        self.chasing = False  #Changes based on if enemy can see player

    #Split sprite sheet into individual frames
    def cut_sprite(self, sheet, frame_count):
        sprite_frames = [] #List to hold sprite images separated
        sheet_split  = sheet.get_width()  // frame_count #The horizontal dimensions are divided by the amount of images in a sheet
        sheet_height = sheet.get_height() #The vertical dimension of the sprite sheet

        for i in range(frame_count): #Iterate through number of images in sprite sheet
            frame = sheet.subsurface(pygame.Rect(i * sheet_split, 0, sheet_split, sheet_height)).copy() #Creates rect of copied frame to save as separate image
            frame = pygame.transform.scale(frame, (60, 59)) #Scales the image to appropriate size
            sprite_frames.append(frame) #Add current i frame to list

        return sprite_frames #Returns list of frames
    
    def update(self, player, platforms, floor): #Handles states

        self.ApplyGravity() #Applies gravity
        self.rect.y += self.vely #Adds vely value onto player y pos
        self.CheckVerticalCollision(platforms, floor) #Constantly checks for vertical and floor collision

        if self.jump_cooldown > 0: #Decreases jump cooldown
            self.jump_cooldown -= 1

        if player and platforms:
            self.update_detection(player, platforms) #Call update detection procedure first

        if self.chasing and player: #When player is detected
            self.update_chase(player, platforms) #Call update chase procedure when player spotted
        else:
            if self.state in ["Idle", "Run"]: #Patrol if not chasing
                self.update_patrol() #Call update patrol procedure

        self.update_animation() #Handle animation (all states)

    def ApplyGravity(self): #Adds gravity onto vely if on ground
        if not self.onground:
            self.vely += self.gravity

    def jump(self):
        if self.onground and self.jump_cooldown == 0: 
            self.vely = self.jump_power #Add jump power value to vely
            self.onground = False 
            self.jump_cooldown = 60 #Set jump cooldown (1 second)

    def CheckVerticalCollision(self, platforms, floor): 

        self.onground = False

        for platform in platforms: #Iterates through all platforms
            if self.rect.colliderect(platform.rect): #Checks for enemy rect overriding platform rect
                if self.vely > 0: #When enemy is falling
                    if self.rect.bottom <= platform.rect.top + self.vely: #Checks top platform collision
                        self.rect.bottom = platform.rect.top #Sets enemy pos above platform
                        self.onground = True 
                        self.vely = 0
                    
                elif self.vely < 0: #When enemy is going up
                    if self.rect.top >= platform.rect.bottom + self.vely: #Checks bottom platform collision
                        self.rect.top = platform.rect.bottom #Sets enemy pos below platform 
                        self.vely = 0 #Stops enemy from moving

        #Floor collision
        if self.rect.bottom >= floor: 
            self.rect.bottom = floor
            self.onground = True
            self.vely = 0

    def checkHorizontalCollision(self, platforms):
        for platform in platforms: #Iterate through all platforms
            if self.rect.colliderect(platform.rect): #Checks for rect collision with platform
                if self.direction == 1:  #Moving right
                    self.rect.right = platform.rect.left
                elif self.direction == -1:  #Moving left
                    self.rect.left = platform.rect.right

    #Updates enemy states
    def update_patrol(self): 
            
        if self.patrol_timer >= 60: #One second
            self.patrol()  #New random patrol sequence
            self.patrol_timer = 0

        if self.state == "Run": #If running
            self.rect.x += self.direction * self.velx #Move the enemy 

            if self.rect.x < self.patrol_min: #Left border
                self.rect.x = self.patrol_min
                self.direction = 1  #Right direction
                self.patrol() #New patrol sequence
                self.patrol_timer = 0

            elif self.rect.x > self.patrol_max: #Right border
                self.rect.x = self.patrol_max
                self.direction = -1  #Left direction
                self.patrol()  #New patrol sequence
                self.patrol_timer = 0

        self.patrol_timer += 1 #Increment timer by one frame

    def update_animation(self):
        frames = self.animations[self.state] #Play corresponding sprite sheet
    
        self.image = frames[int(self.current_sprite)] #Set current image to current frame animation
        self.current_sprite += 0.3 #Increment sprite frame ever 3 loops
    
        if self.current_sprite >= len(frames): #Reset animation
            self.current_sprite = 0

        if self.direction == -1: #Flip image if going left
            self.image = pygame.transform.flip(self.image, True, False)
    
    def patrol(self): #Picks new patrol
        
        self.state = random.choice(["Idle", "Run"]) #Picks between moving or staying still

        if self.state == "Run": #When moving
            self.direction = random.choice([-1, 1]) #Random direction
            self.patrol_duration = random.uniform(30, 90) #Runs for 0.5s to 1.5s
        else: #When staying still
            self.direction = random.choice([-1, 1])
            self.patrol_duration = random.uniform(30, 90) #Stays still for 0.5s to 1.5s
        self.current_sprite = 0 #Resets animation

    def raycast(self, x1, y1, x2, y2, platforms): #Draws ray for LOS

        dx = x2 - x1 #Calculate x distance
        dy = y2 - y1 #Calculates y distance
        distance = math.hypot(dx, dy) #Finds hypotenuse distance
    
        if distance == 0: #No wall can be present if distance is 0
            return False
    
        #Normalize ray direction
        dx /= distance
        dy /= distance
    
        #Move along ray to check for wall collisions
        step_size = 5  #Check every 5 pixels
        steps = int(distance / step_size) #Checks up to distance of player (not past)
    
        for i in range(steps):
            #Current point along ray
            check_x = x1 + dx * i * step_size
            check_y = y1 + dy * i * step_size
        
            #Check if this point is inside any wall
            for platform in platforms: 
                if platform.rect.collidepoint(check_x, check_y):
                    return True  #Hit a wall
    
        return False #No wall hit

    def check_for_player(self, player, platforms): #Checks if player can be seen by enemy
        #Get positions from player and enemy
        enemy_x = self.rect.centerx 
        enemy_y = self.rect.centery
        player_x = player.rect.centerx
        player_y = player.rect.centery

        #Calculate distance and direction to player
        dx = player_x - enemy_x #Calculates distance between player and enemy (x)
        dy = player_y - enemy_y #Calculates distance between player and enemy (y)
        distance = math.hypot(dx, dy) #Finds hypotenuse distance to player

        if distance == 0: #Avoids division by 0
            return False

        #Normalize distances
        dx /= distance
        dy /= distance

        #Enemy facing direction 
        if self.direction == 1:
            enemy_angle = 0 #Face right if player is right
        else:
            enemy_angle = 180 #Face left if player is left

        enemy_facing_x = math.cos(math.radians(enemy_angle)) #Convert angle into direction vector (x)
        enemy_facing_y = math.sin(math.radians(enemy_angle)) #Convert angle into direction vector (y)

        #Dot product rule
        dot_product = enemy_facing_x * dx + enemy_facing_y * dy #Calculating dot product (between -1 and 1)
        vision_cone_bound = math.cos(math.radians(self.vision_angle / 2)) #calculates minimum dot product for the player to still be visible

        player_in_cone = dot_product >= vision_cone_bound #Boolean to check for player in angle range
        player_in_range = distance <= self.vision_range #Boolean to check for enemy sight range

        #Check line of sight
        wall_hit = self.raycast(enemy_x, enemy_y, player_x, player_y, platforms) #Returns False or True depending on if there are platforms between enemy and player pos
        LOS = not wall_hit #LOS active if wall_hit False
        return player_in_cone and player_in_range and LOS
    
    def update_detection(self, player, platforms):
        #Get player and enemy positions
        player_x = player.rect.centerx
        player_y = player.rect.centery
        enemy_x = self.rect.centerx
        enemy_y = self.rect.centery

        dx = player_x - enemy_x #Calculates distance between player and enemy (x)
        dy = player_y - enemy_y #Calculates distance between player and enemy (y)
        distance = math.hypot(dx, dy) #Finds hypotenuse distance to player

        wall_hit = self.raycast(enemy_x, enemy_y, player_x, player_y, platforms) #Check for wall
        LOS = not wall_hit #Line of sight

        if not self.chasing: 
            if self.check_for_player(player, platforms): #Check for player while not chasing
                self.chasing = True #Chase player if spotted
                self.state = "Run" #Run animation
        else: #Chasing
            if not LOS or distance > self.chase_range: #if wall hit or out of range
                self.chasing = False #Dont chase player
                self.patrol_timer = 0 #Reset patrol timer

    def update_chase(self, player, platforms):
        #Get player and enemy positions
        player_x = player.rect.centerx
        player_y = player.rect.centery
        enemy_y = self.rect.centery

        differenceY = enemy_y - player_y #Difference in height

        if differenceY > 50: #Calls jump function when above 50 px
            self.jump()

        ChaseBound = abs(self.rect.centerx - player_x) #Calculate player distance from enemy

        if ChaseBound > 10: #10px away
            if player_x < self.rect.centerx:
                self.direction = -1 #Player is on left of enemy
            else:
                self.direction = 1 #Player is on right of enemy

            if self.rect.centerx < player_x: #If left of player
                self.rect.x += self.chase_speed #Move right
            elif self.rect.centerx > player_x: #If right if player
                self.rect.x -= self.chase_speed #Move left
            self.state = "Run"
        else: #Within 10px
            self.state = "Idle"

        self.checkHorizontalCollision(platforms) #Check for collisions horizontally
    
#    def draw_vision_cone(self, screen):
#        #Get enemy position
#        enemy_x = self.rect.centerx
#        enemy_y = self.rect.centery
#
#        #Get angle based on direction
#        if self.direction == 1:
#            enemy_angle = 0 #Right
#        else:
#            enemy_angle = 180 #Left
#
#        cone = [(enemy_x, enemy_y)] #List of cone points
#        #Calculate the left and right edges of the cone
#        angle_left = enemy_angle - self.vision_angle / 2
#        angle_right = enemy_angle + self.vision_angle / 2
#
#        #Add points along arc
#        for i in range(20): #20 points for cone curve
#            current_angle = angle_left + (angle_right - angle_left) * i / 19 #Go from left edge to right edge
#
#            #Find point at edge of vision range
#            x = enemy_x + self.vision_range * math.cos(math.radians(current_angle))
#            y = enemy_y + self.vision_range * math.sin(math.radians(current_angle))
#            cone.append((x, y)) #Add points to list
#
#        if self.chasing:
#            colour = (255, 165, 0) #Orange
#        else:
#            colour = (0, 255, 0) #Green
#
#        #Draw vision cone
#        pygame.draw.polygon(screen, colour, cone, 2) #surface, color, points, width=2

#    def drawLOS(self, screen, player):
#        if self.chasing: #Only while chasing
#            pygame.draw.line( #LOS visual
#                screen, #Surface
#                (0, 255, 0), #Colour
#                (self.rect.centerx, self.rect.centery), #Start coordinate
#                (player.rect.centerx, player.rect.centery), #End coordinate
#                2 #Width
#            )

    #Draw enemy
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 1) #(Surface, Colour, Rect, Width) Draws enemy border
        screen.blit(self.image, self.rect)