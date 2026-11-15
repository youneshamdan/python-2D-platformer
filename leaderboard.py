import pygame

class Leaderboard:
    def  __init__(self, width, height, backgroundImg, titleImg, panelImg, goldMedal, silverMedal, bronzeMedal, number4, number5, number6, number7, rowBox, levelSelect):

        #Dimensions
        self.width = width
        self.height = height

        #Background
        self.backgroundImg = pygame.transform.scale(backgroundImg, (width, height))

        #Title
        self.titleImg = pygame.transform.scale(titleImg, (850, 90))
        self.titlePOS = (width // 2 - self.titleImg.get_width() // 2, 30)

        #Leaderboard panel
        self.panelImg = pygame.transform.scale(panelImg, (750, 500))
        self.panelPOS = (width // 2 - self.panelImg.get_width() // 2, 150)

        #Level selector
        self.levelSelect = pygame.transform.scale(levelSelect, (220, 40))
        self.levelSelectPOS = (self.panelPOS[0] + 95, self.panelPOS[1] + 20)

        #Font
        self.font = pygame.font.SysFont('ByteBounce', 50)

        #Medals
        medal_size = (40, 60)
        self.goldMedal = pygame.transform.scale(goldMedal, medal_size)
        self.silverMedal = pygame.transform.scale(silverMedal, medal_size)
        self.bronzeMedal = pygame.transform.scale(bronzeMedal, (37, 60))

        #Numbers
        number_size = (70, 70)
        self.number4 = pygame.transform.scale(number4, number_size)
        self.number5 = pygame.transform.scale(number5, number_size)
        self.number6 = pygame.transform.scale(number6, number_size)
        self.number7 = pygame.transform.scale(number7, number_size)

        #Row box
        self.rowBox = pygame.transform.scale(rowBox, (620, 50))

        #Positions
        self.medal_x = self.panelPOS[0] + 40
        self.number_x = self.panelPOS[0] + 25
        self.rowBox_x = self.panelPOS[0] + 100
        self.rowStart_y = self.panelPOS[1] + 60
        self.row_spacing = 58

    def draw(self, screen):
        #Background
        screen.blit(self.backgroundImg, (0, 0))

        #Title
        screen.blit(self.titleImg, self.titlePOS)

        #Panel
        screen.blit(self.panelImg, self.panelPOS)

        #Level selector
        screen.blit(self.levelSelect, self.levelSelectPOS)

        #Record held text
        recordText = self.font.render("RECORD HELD: ", True, (255, 255, 255))
        recordPOS = (self.levelSelectPOS[0] + 270, self.levelSelectPOS[1] + 3)
        screen.blit(recordText, recordPOS)

        #Row 1 (Gold medal)
        screen.blit(self.goldMedal, (self.medal_x, self.rowStart_y + 7))
        screen.blit(self.rowBox, (self.rowBox_x, self.rowStart_y + 10))

        #Row 2 (Silver medal)
        screen.blit(self.silverMedal, (self.medal_x, self.rowStart_y + self.row_spacing + 7))
        screen.blit(self.rowBox, (self.rowBox_x, self.rowStart_y + self.row_spacing + 10))

        #Row 3 (Bronze medal)
        screen.blit(self.bronzeMedal, (self.medal_x + 2, self.rowStart_y + self.row_spacing * 2 + 7))
        screen.blit(self.rowBox, (self.rowBox_x, self.rowStart_y + self.row_spacing * 2 + 10))

        #Row 4 (number 4)
        screen.blit(self.number4, (self.number_x, self.rowStart_y + self.row_spacing * 3))
        screen.blit(self.rowBox, (self.rowBox_x, self.rowStart_y + self.row_spacing * 3 + 10))

        #Row 5 (number 5)
        screen.blit(self.number5, (self.number_x, self.rowStart_y + self.row_spacing * 4))
        screen.blit(self.rowBox, (self.rowBox_x, self.rowStart_y + self.row_spacing * 4 + 10))

        #Row 6 (number 6)
        screen.blit(self.number6, (self.number_x, self.rowStart_y + self.row_spacing * 5))
        screen.blit(self.rowBox, (self.rowBox_x, self.rowStart_y + self.row_spacing * 5 + 10))

        #Row 7 (Number 7)
        screen.blit(self.number7, (self.number_x, self.rowStart_y + self.row_spacing * 6))
        screen.blit(self.rowBox, (self.rowBox_x, self.rowStart_y + self.row_spacing * 6 + 10))
