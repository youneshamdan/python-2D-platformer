import pygame
from platform1 import Platform

class Level:
    def __init__(self, file, image, size, screenHeight):
        self.size = size #Size of each tile
        self.platforms = [] #List holding platforms for level

        self.layout = self.loadLayout(file) #Retrieves level grid from file

        #Calculate level dimensions from layout
        self.width = len(self.layout[0]) * size 
        self.height = len(self.layout) * size

        self.background = pygame.image.load(image).convert() #Loads background image of level
        self.background = pygame.transform.scale(self.background, (self.width, self.height)) #Scales the background image to grid

        self.platform_image = '' #Platform image for later

        self.cameraY = self.height - screenHeight  #Starts at bottom
        self.screenHeight = screenHeight

        #Camera movement
        self.cameraSpeed = 0.05
        self.cameraAcceleration = 0.004
        self.cameraMaxSpeed = 5 #Max camera speed
        self.CameraTrigger = screenHeight // 2 #When camera starts moving
        self.CameraStart = False #Activates camera move

    def loadLayout(self, file):
        grid = [] #Temp list for level grid
        with open(file, 'r') as f: #Opens level file in read
            for line in f:
                grid.append(line.strip()) #Adds each line of grid to grid list
        return grid
    
    #Sets screen size for level
    def SetScreenSize(self, width, height):
        self.width = width
        self.height = height
        
    #Set image used for platforms
    def SetImage(self, image):
        self.image = image
        self.SetPlatforms()
    
    #Create platforms from layout
    def SetPlatforms(self):
        self.platforms = [] #Platform list, clears before creating new ones

        for Rowindex, row in enumerate(self.layout): #Loop through each row in layout
            for Colindex, tile in enumerate(row): #Loop through each tile in current row
                if tile == 'X': #Checks if tile represents platform
                    x = Colindex * self.size #Calculates platform position based on index
                    y = Rowindex * self.size
                    platform = Platform(x, y, self.size, self.size, self.image) #Create new platform object
                    self.platforms.append(platform) #Add object to platform list

    def setDifficulty(self, maxSpeed, acceleration): #Changes based on settings
        self.cameraMaxSpeed = maxSpeed
        self.cameraAcceleration = acceleration

    def update(self, player):
        playerPos = player.rect.y - self.cameraY #Caculate player position 

        if playerPos > self.screenHeight:
            print("Player failed")

        if playerPos <= self.CameraTrigger: #Start moving camera when player is at trigger point
            self.CameraStart = True

        #Accelerate
        if self.CameraStart: #If moving
            if self.cameraSpeed < self.cameraMaxSpeed: #If under max speed
                self.cameraSpeed += self.cameraAcceleration #Increase speed

            #Move up
            self.cameraY -= self.cameraSpeed

            #Stop at top
            if self.cameraY < 0:
                self.cameraY = 0

    def draw(self, screen, player, enemies):
        #Background
        screen.blit(self.background, (0, -self.cameraY)) #Draw background with camera offset

        #Platforms
        for platform in self.platforms:
            screen.blit(platform.image, (platform.rect.x, platform.rect.y - self.cameraY)) #Draw all platforms with camera offset

        #Player
        screen.blit(player.image, (player.rect.x, player.rect.y - self.cameraY)) #Draw player with camera offset

        #Enemies
        for enemy in enemies: 
            screen.blit(enemy.image, (enemy.rect.x, enemy.rect.y - self.cameraY)) #Draw all enemies with camera offset

    #Gets bottom of level
    def getFloor(self):
        return self.height