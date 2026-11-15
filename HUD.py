import pygame
pygame.init()

class HUD:
    def __init__(self, width, height, heartImg, coinImg, pauseImg):
        self.width = width #Screen width
        self.height = height #Screen height

        #HUD values
        self.lives = 3
        self.maxLives = 3
        self.currency = 0
        self.level = 1
        self.altitude = 0
        self.timer = 0

        #Images
        self.heartImg = pygame.transform.scale(heartImg, (32,32))
        self.coinImg = pygame.transform.scale(coinImg, (64,64))
        self.pauseImg = pygame.transform.scale(pauseImg, (50,50))

        #Fonts
        self.LargeFont = pygame.font.SysFont('ByteBounce', 72)
        self.MediumFont = pygame.font.SysFont('ByteBounce', 36)

    #Updates changing values
    def update(self, playerY, levelHeight):
        self.timer += 1/60 #Increases timer
        self.altitude = (levelHeight - playerY) // 50 #Increases altitude

    #Decreases live
    def lifeLost(self):
        if self.lives > 0:
            self.lives -= 1
    
    #Increments currency 
    def AddCoin(self):
        self.currency += 1

    #Checks if lives are gone
    def GameLostCheck(self):
        return self.lives <= 0
    
    #Formats time in (MM:SS:MSMS)
    def OrganiseTime(self):
        minutes = int(self.timer // 60) #Gives integer minute value
        seconds = int(self.timer % 60) #Gives remainder of minutes 
        mseconds = int((self.timer % 1) * 100) #Caculates decimal value for miliseconds
        return str(minutes) + ":" + str(seconds).zfill(2) + ":" + str(mseconds).zfill(2) #Returns all values as string
    
    #Checks for pause button event
    def checkPause(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN: 
            pauseRect = self.pauseImg.get_rect(topleft=(20,20)) #Pause image hitbox
            if pauseRect.collidepoint(event.pos): #Click event within pause image
                return True 
        return False
    
    def draw(self, screen):
        screen.blit(self.pauseImg, (20,20)) #Pause image (top left)

        screen.blit(self.coinImg, (13, 80)) #Coin image (top left)
        coinText = self.MediumFont.render(str(self.currency), True, (255, 255, 255)) #Displays currency value
        screen.blit(coinText, (73, 100)) #Draws text

        altitudeText = self.LargeFont.render((str(int(self.altitude)) + "M"), True, (255, 255, 255)) #Displays altitude value
        altitudeRect = altitudeText.get_rect(centerx = self.width // 2, top=20) #Creates rect for text positioning
        screen.blit(altitudeText, altitudeRect) #Draws altitude

        timeText = self.MediumFont.render(self.OrganiseTime(), True, (255, 255, 255)) #Displays time
        timeRect = timeText.get_rect(centerx=self.width // 2, top=80) #Creates rect for text positioning
        screen.blit(timeText, timeRect) #Draws time

        levelText = self.MediumFont.render("LEVEL " + str(self.level), True, (255, 255, 255)) #Displays level value
        levelRect = levelText.get_rect(right=self.width - 20, top=20) #Creates rect for text positioning
        screen.blit(levelText, levelRect) #Draws level text

        #Draws lives
        for i in range(self.lives): #3 hearts
            x = self.width - 48 - (i * 40) #Caculates position based on heart number 
            screen.blit(self.heartImg, (x, 60)) #Draws heart

    #     def resetHUD(self):
    #     
    #     //////////////////////////////////////////////////
    #     Resets all HUD values to default state
    #
    #     Purpose:
    #     This procedure can be used when restarting a level,
    #     starting a new game, or returning to the main menu
    #
    #     //////////////////////////////////////////////////
    #
    #     self.lives = self.maxLives
    #     self.currency = 0
    #     self.level = 1
    #     self.altitude = 0
    #     self.timer = 0