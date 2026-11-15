import pygame

class PauseMenu:
    def __init__(self, width, height, titleImg, resumeImg, exitImg, settingsImg):
        #Dimensions
        self.width = width
        self.height = height

        #title
        self.titleImg = pygame.transform.scale(titleImg, (540, 100))
        self.titlePOS = (width // 2 - self.titleImg.get_width() // 2, 60)

        #button properties
        buttonWidth = 330
        buttonHeight = 75
        buttonx = width // 2 - buttonWidth // 2

        #Overlay
        self.overlay = pygame.Surface((width, height))
        self.overlay.fill((0, 0, 0)) #Black
        self.overlay.set_alpha(153) #60% transparent 

        #resume game
        self.resumeImg = pygame.transform.scale(resumeImg, (buttonWidth, buttonHeight)) #Image scale
        self.resumePOS = (buttonx, 230) #Position
        self.resumeRect = self.resumeImg.get_rect(topleft=self.resumePOS) #Creates rect for events

        #exit game
        self.exitImg = pygame.transform.scale(exitImg, (buttonWidth, buttonHeight)) #Image scale
        self.exitPOS = (buttonx, 320) #Position
        self.exitRect = self.exitImg.get_rect(topleft=self.exitPOS) #Creates rect for events

        #settings
        self.settingsImg = pygame.transform.scale(settingsImg, (buttonWidth, buttonHeight)) #Image scale
        self.settingsPOS = (buttonx, 410) #Position
        self.settingsRect = self.settingsImg.get_rect(topleft=self.settingsPOS) #Creates rect for events

    #draw title and buttons
    def draw(self, screen):
        screen.blit(self.overlay, (0, 0)) #Overlay drawn first
        screen.blit(self.titleImg, self.titlePOS)
        screen.blit(self.resumeImg, self.resumePOS)
        screen.blit(self.exitImg, self.exitPOS)
        screen.blit(self.settingsImg, self.settingsPOS)

    #check for player event
    def HandleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN: #Mouse click event
            if self.resumeRect.collidepoint(event.pos):
                return "resume"
            elif self.exitRect.collidepoint(event.pos):
                return "exit"
            elif self.settingsRect.collidepoint(event.pos):
                return "settings"