import pygame

class Platform:
    def __init__(self,x,y,width,height,image): #Constructor holding platform attributed
        self.image = pygame.transform.scale(image, (width, height)) #Platform image (for different platforms in different levels)
        self.rect = self.image.get_rect() #Hitbox of platform
        self.rect.x = x #Screen pos x
        self.rect.y = y #Screen pos y

    def draw(self, screen): #Display on screen procedure
        screen.blit(self.image, self.rect) #Draws platform
        