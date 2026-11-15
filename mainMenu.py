import pygame

class MainMenu:
    def __init__(self, screenWidth, screenHeight, titleImg, startbuttonImg, leaderboardbuttonImg, settingsbuttonImg, backgroundImg):
        
        #Dimensions
        self.screenWidth = screenWidth 
        self.screenHeight = screenHeight

        #Background
        self.backgroundImg = backgroundImg  

        #Title
        self.titleImg = pygame.transform.scale(titleImg, (800, 136)) #Screen title
        self.titlePOS = (screenWidth // 2 - self.titleImg.get_width() // 2, 50) #Title position

        self.startbuttonImg = pygame.transform.scale(startbuttonImg, (330, 75)) #Image scale
        self.startbuttonPOS = (screenWidth // 2 - self.startbuttonImg.get_width() // 2, 250) #Position
        self.startbuttonRect = self.startbuttonImg.get_rect(topleft=self.startbuttonPOS) #Creates rect for events

        #leaderboard
        self.leaderboardbuttonImg = pygame.transform.scale(leaderboardbuttonImg, (330, 75)) #Image scale
        self.leaderboardbuttonPOS = (screenWidth // 2 - self.leaderboardbuttonImg.get_width() // 2, 340) #Position
        self.leaderboardbuttonRect = self.leaderboardbuttonImg.get_rect(topleft=self.leaderboardbuttonPOS) #Creates rect for events

        #Settings
        self.settingsButtonImg = pygame.transform.scale(settingsbuttonImg, (330, 75)) #Image scale
        self.settingsButtonPOS = (screenWidth // 2 - self.settingsButtonImg.get_width() // 2, 430) #Position
        self.settingsButtonRect = self.settingsButtonImg.get_rect(topleft=self.settingsButtonPOS) #Creates rect for events
 
    def draw(self, screen):
        screen.blit(self.backgroundImg, (0,0)) #Background
        screen.blit(self.titleImg, self.titlePOS) #Title
        screen.blit(self.startbuttonImg, self.startbuttonPOS) #Start button
        screen.blit(self.leaderboardbuttonImg, self.leaderboardbuttonPOS) #Leaderboard
        screen.blit(self.settingsButtonImg, self.settingsButtonPOS) #Settings

    def HandleEvent(self, event): 
        if event.type == pygame.MOUSEBUTTONDOWN: #Mouse click event
            if self.startbuttonRect.collidepoint(event.pos): #If start button clicked
                return "start game"
            elif self.leaderboardbuttonRect.collidepoint(event.pos): #If leaderboard button clicked
                return "leaderboard"
            elif self.settingsButtonRect.collidepoint(event.pos): #If settigns clicked
                return "settings"