import pygame

class Settings:
    def __init__(self, width, height, backgroundImg):
        self.width = width
        self.height = height

        self.backgroundImg = pygame.transform.scale(backgroundImg, (width, height)) #Background

        #Fonts
        self.TextFont = pygame.font.SysFont('ByteBounce', 30) #Font
        self.TitleFont = pygame.font.SysFont('ByteBounce', 50)

        #Button dimensions
        buttonWidth = 100
        buttonHeight = 30
        button_x = 100
        buttonSpacing = 40

        #Title
        self.difficultyText = self.TitleFont.render("DIFFICULTY", True, (255, 255, 255))

        #Easy Button
        self.easyRect = pygame.Rect(button_x, 150, buttonWidth, buttonHeight)
        self.easyText = self.TextFont.render("EASY", True, (255, 255, 255))

        #Medium Button
        self.mediumRect = pygame.Rect(button_x, 150 + buttonSpacing, buttonWidth, buttonHeight)
        self.mediumText = self.TextFont.render("MEDIUM", True, (255, 255, 255))

        #Hard Button
        self.HardRect = pygame.Rect(button_x, 150 + buttonSpacing * 2, buttonWidth, buttonHeight)
        self.HardText = self.TextFont.render("HARD", True, (255, 255, 255))

        #Button colors
        self.buttonColour = (216, 116, 20) #Gingerbread brown
        self.selectColour = (38, 225, 8) #Green
        self.hoverColour = (230, 130, 34) #Lighter gingerbread

        self.currentDifficulty = "medium" #Selected difficulty

        #////// VOLUME SLIDER ///////
        self.volumeTitle = self.TitleFont.render("VOLUME", True, (255, 255, 255))
        
        # Slider dimensions
        self.sliderX = 350
        self.sliderY = 160
        self.sliderWidth = 300
        self.sliderHeight = 8
        self.sliderFillWidth = 150  #Default 
        
        # Slider colors
        self.sliderColour = (100, 100, 100)
        self.barColour = (200, 200, 200)
        self.handleColour = (255, 255, 255)

        #Difficulty settings
        self.difficultySettings = {
            "easy": {"cameraMaxSpeed": 4, "cameraAcceleration": 0.001}, #Easy settings
            "medium": {"cameraMaxSpeed":  4.5, "cameraAcceleration": 0.002}, #Medium settings
            "hard": {"cameraMaxSpeed":  5, "cameraAcceleration": 0.004} #Hard settings
        }

    def getCamSettings(self):
        return self.difficultySettings[self.currentDifficulty] #get Current difficulty settings
    
    def getVolume(self):
        return int(self.sliderFillWidth / (self.sliderWidth / 100))
    
    def draw(self, screen):
        #Background
        screen.blit(self.backgroundImg, (0, 0))

        #Get mouse position for hover effect
        mousePOS = pygame.mouse.get_pos()

        #Easy button
        if self.currentDifficulty == "easy":
            pygame.draw.rect(screen, self.selectColour, self.easyRect) #Currently selected rect
        elif self.easyRect.collidepoint(mousePOS): 
            pygame.draw.rect(screen, self.hoverColour, self.easyRect) #Hovering over rect
        else:
            pygame.draw.rect(screen, self.buttonColour, self.easyRect) #Not hovering or selected (normal colour)
        easyTextPOS = (self.easyRect.centerx - self.easyText.get_width() // 2, #Text x
                       self.easyRect.centery - self.easyText.get_height() // 2) #Text y
        screen.blit(self.easyText, easyTextPOS)

        #Medium Button
        if self.currentDifficulty == "medium":
            pygame.draw.rect(screen, self.selectColour, self.mediumRect) #Currently selected rect
        elif self.mediumRect.collidepoint(mousePOS):
            pygame.draw.rect(screen, self.hoverColour, self.mediumRect) #Hovering over rect
        else: 
            pygame.draw.rect(screen, self.buttonColour, self.mediumRect) #Not hovering or selected (normal colour)
        mediumTextPOS = (self.mediumRect.centerx - self.mediumText.get_width() // 2, #Text x
                         self.mediumRect.centery - self.mediumText.get_height() // 2) #Text y
        screen.blit(self.mediumText, mediumTextPOS)

        #Hard Button
        if self.currentDifficulty == "hard":
            pygame.draw.rect(screen, self.selectColour, self.HardRect) #Currently selected rect
        elif self.HardRect.collidepoint(mousePOS):
            pygame.draw.rect(screen, self.hoverColour, self.HardRect) #Hovering over rect
        else:
            pygame.draw.rect(screen, self.buttonColour, self.HardRect) #Not hovering or selected (normal colour)
        hardTextPOS = (self.HardRect.centerx - self.HardText.get_width() // 2, #Text x
                       self.HardRect.centery - self.HardText.get_height() // 2) #Text y
        screen.blit(self.HardText, hardTextPOS)

        #Difficulty Title
        DiffTitlePOS = (self.HardRect.centerx - self.difficultyText.get_width() // 2, 80)
        screen.blit(self.difficultyText, DiffTitlePOS)

                #----VOLUME SLIDER----
        #Title
        screen.blit(self.volumeTitle, (self.sliderX, 80))

        #Bar background
        pygame.draw.rect(screen, self.barColour, 
                        (self.sliderX, self.sliderY, self.sliderWidth, self.sliderHeight), 
                        border_radius=4)

        #Filled portion
        pygame.draw.rect(screen, self.sliderColour, #filled part of slider represents current volume 
                        (self.sliderX, self.sliderY, self.sliderFillWidth, self.sliderHeight), 
                        border_radius=4)

        #Handle (circle)
        handleX = self.sliderX + self.sliderFillWidth #placed at the end of filled portion
        handleY = self.sliderY + self.sliderHeight // 2 #centers handle vertically on slider bar
        pygame.draw.circle(screen, self.handleColour, (handleX, handleY), 12) #Radius=12

        #Volume text
        volumeText = self.TextFont.render(f"{self.getVolume()}%", True, (255, 255, 255)) #Shows current volume as %
        screen.blit(volumeText, (self.sliderX + self.sliderWidth + 20, self.sliderY - 5))

        #Update slider if mouse is pressed
        if pygame.mouse.get_pressed()[0]: #Check if left mouse button is held down
            if mousePOS[0] <= self.sliderX + self.sliderWidth and mousePOS[0] >= self.sliderX:  #Checks if mouse x pos is in horizontal bounds of slider
                if mousePOS[1] <= self.sliderY + self.sliderHeight + 15 and mousePOS[1] >= self.sliderY - 15: #Checks if mouse y pos is in horizontal bounds of slider (15 padding)
                    self.sliderFillWidth = mousePOS[0] - self.sliderX #Sets filled width based on mouse x pos

    def HandleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.easyRect.collidepoint(event.pos): #Easy 
                self.currentDifficulty = "easy"
                return "difficultyChanged"
            elif self.mediumRect.collidepoint(event.pos): #Medium
                self.currentDifficulty = "medium"
                return "difficultyChanged"
            elif self.HardRect.collidepoint(event.pos): #Hard
                self.currentDifficulty = "hard"
                return "difficultyChanged"

        #Leave menu
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_ESCAPE:
                return "return"